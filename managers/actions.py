from managers.storage import StorageManager
from actions_framework.actions import Action

StartAction = Action('start', 'C')
UnknownAction = Action('unknown', 'M', callback=Action.unknown_callback)
UnknownAction.add_actions(StartAction)


class ActionManager(StorageManager):
    def __init__(self, name='ActionManager'):
        self.actions = list()
        super().__init__(name=name)
        self.publisher_callbacks = {}

    def register_publisher(self, name, callback):
        """ Name of publisher, method from publisher to call whenever there is some action for it"""
        publisher_action = Action(name, 'C')
        self.publisher_callbacks[name] = callback
        return publisher_action

    # def register_action(self, action):
    #     pass

    def resolve_action(self, session, message):
        """
        This session will use the context in session['action'] to get the next publisher callback. For action, if there

        """

        return publisher_callback, action


ActionManager = ActionManager()
