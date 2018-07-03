from telegram import ReplyKeyboardMarkup

from managers.storage import StorageManager
from managers.actions import ActionManager, UnknownAction, StartAction
from schema.telegram.message import MessageSchema
from bot_interactor import BotApp


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

    :param actions: list of actions that each key represent
    :param row_size: no. of keys in a single row
    Layout: list of lists specifying the position of each key (with given action) on the keyboard
    """
    layout = []
    for i in range(0, len(triggers), row_size):
        layout.append([triggers for triggers in triggers[i:i + row_size]])
    return layout


class InteractionManager(StorageManager):
    """
    Work of interaction manager:
        - expose and api for sending the data to the user
        - store the conversations
        - receive message from user, figure out what publisher it belongs
          to and pass it the message and wait for the response
    """

    def __init__(self):
        self.name = "interaction_manager"
        super().__init__(self.name)
        self.sessions = {}
        BotApp.add_receiver_callback(self.receive_message)

    def get_session(self, session_key):
        """ session_key: <chat_id>"""
        session = self.sessions.get(session_key)
        # print('session is {}'.format(session))
        if not session:
            print("creating new session")
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

    def update_session_conversation(self, session_key, message_json):
        self.sessions[session_key]['conversation'].append(message_json)

    # def update_session_action(self, session_key, action):
    #     self.sessions[session_key]['action']['last_action'] = action

    def send_message(self, to, message, next_actions):
        if next_actions:
            keyboard = ReplyKeyboardMarkup(keyboard_layout(next_actions))
        else:
            keyboard = None
        if not isinstance(to, (tuple, list)):
            to = [to]
        for t in to:
            result = BotApp.send_message(t, message, keyboard)
            message_json = MessageSchema().dump(result)
            self.update_session_conversation(session_key=t, message_json=message_json)

    def receive_message(self, update):
        """ update: update instance from telegram.update"""

        message_instance = update.message
        text = message_instance.text
        chat_id = message_instance.chat_id
        from_user = message_instance.from_user
        session_key = chat_id
        session = self.get_session(session_key)

        message_json = MessageSchema().dump(message_instance)
        self.update_session_conversation(session_key, message_json)

        publisher_callback, action = ActionManager.resolve_action(session, text)

        if publisher_callback is None:
            return self.send_message(to=chat_id, message=action.callback(), next_actions=action.next_action_list())

        # TODO: make it async
        # this callback will trigger the concerned publisher and provide it with the action to act on.
        # responsibility of sending the response is up to the publisher
        publisher_callback(session, action)


InteractionManager = InteractionManager()
