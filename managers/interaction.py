import time
import asyncio
import uuid

from app.schema.telegram.keyboard_button import KeyboardButton
from app.schema.telegram.reply_keyboard_markup import ReplyKeyboardMarkup

from managers.storage import StorageManager
from managers.actions import ActionManager, UnknownAction, StartAction
from app.schema.telegram.message import MessageSchema

# TODO: remove this and plug the send_message api using some kind of callback
# from bot_interactor import BotApp
from app.methods.telegram.repliers import sendMessage, update_inline_results


class Roles:
    ROLE_ADMIN = 'admin'
    ROLE_USER = 'user'

    ROLE_DEFAULT = ROLE_USER


class Permissions:
    PERMISSION_READ = "read"
    PERMISSION_ACT = {
        "ALL": "all",
        "TRADE": "trade",
        "NON_TRADE": "non_trade",
    }

    PERMISSION_DEFAULT = [
        PERMISSION_READ,
        PERMISSION_ACT['NON_TRADE']
    ]


def keyboard_layout(triggers, row_size=3):
    """
    Returns the layout for the keyboard

    :param triggers: list of actions that each key represent
    :param row_size: no. of keys in a single row
    Layout: list of lists specifying the position of each key (with given action) on the keyboard
    """
    layout = []
    for i in range(0, len(triggers), row_size):
        layout.append([KeyboardButton(triggers) for triggers in triggers[i:i + row_size]])
    return layout


class InteractionManager(StorageManager):
    """
    Work of interaction manager:
        - expose and api for sending the data to the user
        - store the conversations
        - receive message from user, figure out what publisher it belongs
          to and pass it the message and wait for the response
    """

    def __init__(self, name):
        self.id = uuid.uuid4()
        super().__init__(name)
        self.sessions = {}
        # BotApp.add_receiver_callback(self.receive_message)

    async def get_session(self, session_key):
        """ session_key: <chat_id>"""
        session = self.sessions.get(session_key)
        # print('session is {}'.format(session))
        if not session:
            # print("creating new session")
            session = {
                'chat_id': session_key,
                'security': {
                    "permission": Permissions.PERMISSION_DEFAULT,
                    "role": Roles.ROLE_DEFAULT
                },
                'action': {
                    # 'last_action': ActionSchema().dump(UnknownAction),
                    'last_action': UnknownAction,
                    'context': 'unknown'
                },
                'conversation': [],
                'framework_data': {},
            }
            self.sessions[session_key] = session
        # print(self.sessions)
        return session

    async def update_session_conversation(self, session_key, message_json):
        self.sessions[session_key]['conversation'].append(message_json)

    async def send_message(self, to, message, next_actions):
        print('interaction send_message')
        if next_actions:
            update_inline_results(next_actions)
            # if next_actions:
            #     keyboard = keyboard_layout(next_actions)
            # else:
            #     keyboard = None
            layout = keyboard_layout(next_actions)
            reply_keyboard = ReplyKeyboardMarkup(layout, one_time_keyboard=False)
            print("keyboard: {}".format(reply_keyboard))
        else:
            reply_keyboard = None
        if not isinstance(to, (tuple, list)):
            to = [to]
        for t in to:
            send_message = asyncio.coroutine(sendMessage)
            result = await send_message(t, message, reply_keyboard)
            print(result)
            message_json = MessageSchema().dump(result)
            await self.update_session_conversation(session_key=t, message_json=message_json)

        print("exiting from send message")

    async def receive_message(self, update):
        """ update: update instance from telegram.update"""

        message_instance = update.message
        text = message_instance.text
        chat_id = message_instance.chat_id
        from_user = message_instance.from_user
        session_key = chat_id
        session = await self.get_session(session_key)

        message_json = MessageSchema().dump(message_instance)
        await self.update_session_conversation(session_key, message_json)

        action_resolver_coro = asyncio.coroutine(ActionManager.resolve_action)
        service_callback, action = await action_resolver_coro(session, text)

        start = time.time()

        if service_callback is None:
            await self.send_message(to=chat_id, message=action.callback(),
                                    next_actions=action.next_action_list())
        else:
            service_coro = asyncio.coroutine(service_callback)
            await service_coro(session, action)

        end = time.time()
        print("Time taken to complete job: {}".format(end - start))


InteractionManager = InteractionManager("interaction_manager")
