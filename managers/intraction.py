from managers.storage import StorageManager
from managers.actions import ActionManager, UnknownAction, StartAction


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


class InteractionManager(StorageManager):
    """
    Work of interaction manager:
        - expose and api for sending the data to the user
        - store the conversations
        - receive message from user, figure out what publisher it belongs
          to and pass it the message and wait for the response
    """

    def __init__(self, name):
        super().__init__(name)
        self.sessions = {}

    def get_session(self, session_key):
        """ session_key: <chat_id>"""
        session = self.sessions.get(session_key)
        if not session:
            session = {
                'security': {
                    "permission": Permissions.PERMISSION_DEFAULT,
                    "role": Roles.ROLE_DEFAULT
                },
                'action': {
                    'last_action': ActionSchema().dump(UnknownAction),
                    'context': None
                },
                'conversation': [],
                'subscriptions': {
                    'subscribed': [],
                    'mute': [],
                    'unsubscribed': [],
                }
            }
            self.sessions[session_key] = session
        return session

    def update_session_conversation(self, session_key, message_json):
        self.sessions[session_key]['conversation'].append(message_json)

    # def update_session_action(self, session_key, action):
    #     self.sessions[session_key]['action']['last_action'] = action

    def send_message(self, to, message, reply_markup):
        # sending message to user through bot will return a message instance, save this instance in the session
        pass

    def receive_message(self, update):
        """ update: update instance from telegram.update"""

        # TODO: remove this from here
        # from telegram.update import Update
        # update = Update()
        # from telegram.user import User

        message_instance = update.message
        text = message_instance.text
        chat_id = update.message.chat_id
        from_user = update.message.from_user
        session_key = '{}'.format(chat_id)
        session = self.get_session(session_key)

        # TODO: create MessageSchema and obtain the json for message_instance
        message_json = MessageSchema().dump(message_instance)
        self.update_session_conversation(session_key, message_json)

        publisher_callback, action = ActionManager.resolve_action(session, text)

        # TODO: make it async
        # this callback will trigger the concerned publisher and provide it with the action to act on.
        # responsibility of sending the response is up to the publisher
        publisher_callback(action)
