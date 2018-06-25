class StorageManager:
    """
    The store house for the application data.
    Data for a particular session (user:chat) is stored in self.context
    All the subscribers can store their data for a particular session here.
    This can be used to model the interactions with the database when the application scales.
    """

    def __init__(self):
        self.store = {}
        # self.context = {}

        # self.actions = {}
        # self.start_action = None  # Action('start', 'C')

    # def resolve(self, update):
    #     user_id = update.message.message_from.id
    #     chat_id = update.message.chat_id
    #     key = '{}:{}'.format(user_id, chat_id)
    #     if key not in self.store:
    #         self.store[key] = {
    #             'user_id': user_id,
    #             'chat_id': chat_id,
    #             'subscriptions': {},
    #             'last_action': None
    #         }
    #     return self.store[key]

    # def add_actions(self, action):
    #     # if not isinstance(action, Action):
    #     #     raise TypeError('`action` must be an instance of class:Action')
    #     self.actions[action.id] = action
    #
    # def add_parent_action(self, action):
    #     """ Add `action` as a child of Start Action """
    #     self.start_action.add_actions(action)


StorageManager = StorageManager()  # ContextManager is a singleton
# contextManager = ContextManager  # synonyms for ContextManager
# context_manager = ContextManager
