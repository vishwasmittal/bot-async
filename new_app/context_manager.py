# from telegram.update import Update
from .action import Action


class ContextManager:
    """
    The store house for the application data.
    Data for a particular session (user:chat) is stored in self.contxt
    All the subscribers can store their data for a particular session here.
    This can be used to model the interactions with the database when the application scales.
    """

    def __init__(self):
        self.context = {}
        self.actions = {}
        self.start_action = Action('start', 'C')

    def resolve(self, update):
        user_id = update.message.message_from.id
        chat_id = update.message.chat_id
        key = '{}:{}'.format(user_id, chat_id)
        if key not in self.context:
            self.context[key] = {
                'user_id': user_id,
                'chat_id': chat_id,
                'subscriptions': {},
                'last_action': self.start_action.id
            }
        return self.context[key]

    def add_actions(self, action):
        if not isinstance(action, Action):
            raise TypeError('`action` must be an instance of class:Action')
        self.actions[action.id] = action

    def add_parent_action(self, action):
        """ Add `action` as a child of Start Action """
        self.start_action.add_actions(action)


ContextManager = ContextManager()  # ContextManager is a singleton
# contextManager = ContextManager  # synonyms for ContextManager
# context_manager = ContextManager
