from new_app.storage import StorageManager
from new_app.action import Action, UnknownAction


class Session:
    def __init__(self, chat_id, user_id):
        self.user_id = user_id
        self.chat_id = chat_id
        self.data = Session.get_empty_data(chat_id=chat_id, user_id=user_id)

    @property
    def key(self):
        return Session.get_key(self.chat_id, self.user_id)

    @staticmethod
    def get_key(chat_id, user_id):
        return '{}:{}'.format(chat_id, user_id)

    @staticmethod
    def get_empty_data(chat_id, user_id):
        return {
            'user_id': user_id,
            'chat_id': chat_id,
            'action': {
                'last_action': UnknownAction,
                'data': {}
            },  # user will start interacting with the `start` command
            'subscriptions': set()
        }


class SessionManager:
    def __init__(self):
        if 'sessions' not in StorageManager.store:
            StorageManager.store['sessions'] = {}
        self.session_store = StorageManager.store['sessions']

    def add_session(self, chat_id, user_id):
        session = Session(chat_id=chat_id, user_id=user_id)
        self.session_store[session.key] = session
        return session

    def get_or_create(self, chat_id, user_id):
        """ Return the session instance for these params """
        key = Session.get_key(chat_id=chat_id, user_id=user_id)
        if key in self.session_store:
            return self.session_store[key]
        else:
            return self.add_session(chat_id=chat_id, user_id=user_id)


SessionManager = SessionManager()  # session manager is Singleton
