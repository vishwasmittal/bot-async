import uuid

from .context_manager import ContextManager


class Action(object):
    def __init__(self, trigger, kind, callback=None):
        self.id = uuid.uuid4()

        if kind.upper() not in ['C', 'M']:
            raise TypeError("'type' should be one of ['C', 'M']")

        self.trigger = trigger
        # self.complex_trigger = complex_trigger
        self.kind = kind.upper()
        self.next_action_ids = set()
        self.next_actions = set()
        self.callback = callback or self.none_callback

        ContextManager.add_actions(self)

    def __repr__(self):
        return "Action(id={}, trigger={}, kind={})".format(self.id, self.trigger, self.kind)

    def get_id(self):
        return self.id

    def get_next_actions(self):
        """
        :return: a set containing all the actions that can be performed in the next step
        """
        return self.next_actions

    def add_actions(self, actions):
        _actions = []
        if not isinstance(actions, (list, tuple)):
            _actions.append(actions)

        for act in _actions:
            self.next_actions.add(act)
            self.next_action_ids.add(act.id)

    @staticmethod
    def none_callback(*args, **kwargs):
        return None

    # def export_action(self):
            #     # self.handler = json.dumps
            #     # action_dict = dict()
            #     # # print(self.next_actions)
            #     # print(self)
            #     # for a in self.next_actions:
            #     #     print(a)
            #     #     print(a.next_actions)
            #     action_dict = {
            #         'text': self.trigger,
            #         'kind': self.kind,
            #         'handler': {
            #             'module': self.callback.__module__,
            #             'name': self.callback.__name__
            #         },
            #         'next_actions': [next_action.export_action() for next_action in self.next_actions]
            #     }
            #     return action_dict
            #
            # @staticmethod
            # def is_next_actions_correct(next_actions):
            #     if type(next_actions) == list:
            #         for action in next_actions:
            #             # if isinstance(action, Action):
            #             if not type(action) == Action:
            #                 return False
            #         return True
            #     else:
            #         return False
            #
            # @staticmethod
            # def import_action(action_dict):
            #     if type(action_dict) is not dict:
            #         raise TypeError("'action_dict' must be a dict")
            #     else:
            #         next_actions = [Action.import_action(action) for action in action_dict.get('next_actions', [])]
            #         action = Action(action_dict['trigger'],
            #                         action_dict.get('type') or 'M',
            #                         handler=Action.get_handler(action_dict.get('handler', None)))
            #         action.add_actions(next_actions)
            #         return action
            #
            # @staticmethod
            # def get_handler(handler):
            #     """
            #     To obtain proper handler for the action
            #     :param None/function/dict handler:
            #         Returns handler if it is None or a function.
            #         If dict is provided, it loads the function from the `module` and `name` of function provided
            #     :return: None or function
            #     """
            #     if handler is None or type(handler) == function:
            #         func = handler
            #     elif type(handler) == dict:
            #         try:
            #             module = __import__(handler['module'])
            #             func = getattr(module, handler['name'])
            #         except Exception as e:
            #             print(e)
            #             func = None
            #     else:
            #         func = None
            #
            #     return func
