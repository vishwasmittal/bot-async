from managers.storage import StorageManager
from actions_framework.actions import Action

StartAction = Action('start', 'C', Action.start_callback)
UnknownAction = Action('unknown', 'C', callback=Action.unknown_callback)
UnknownAction.add_actions(StartAction)


class ActionManager(StorageManager):
    def __init__(self, name='ActionManager'):
        self.actions = list()
        super().__init__(name=name)
        self.publisher_callbacks = {
            'unknown': None,
            'start': None,
        }

    def register_publisher(self, name, callback):
        """ Name of publisher, method from publisher to call whenever there is some action for it"""
        publisher_action = Action(name, 'C')
        self.publisher_callbacks[name] = callback
        StartAction.add_actions(publisher_action)
        return publisher_action

    def resolve_action(self, session, message):
        """
        This session will use the context in session['action'] to get the next publisher callback. For action, if there

        """
        context = session['action']['context']
        last_action = session['action']['last_action']
        publisher_callback = self.publisher_callbacks[context]

        next_actions = last_action.get_next_actions()

        for action in next_actions:
            if action.check_trigger(message):
                if context == 'start' or context == 'unknown':  # assigning the context to framework name, assuming
                    # that the options after start represent frameworks' names
                    session['action']['context'] = action.trigger
                return publisher_callback, action

        if StartAction.check_trigger(message):
            session['action']['context'] = 'start'
            return None, StartAction

        session['action']['context'] = 'unknown'
        return publisher_callback, UnknownAction


ActionManager = ActionManager()
