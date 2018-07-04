import uuid


# from managers.actions import ActionManager


class Action(object):
    ACTION_KINDS = ['C', 'M', 'I']

    def __init__(self, trigger, kind, callback=None, id=None, callback_args=None, **callback_kwargs):
        self.id = id or uuid.uuid4()

        if kind.upper() not in self.ACTION_KINDS:
            raise TypeError("'type' should be one of {}".format(self.ACTION_KINDS))

        self.trigger = trigger
        # self.complex_trigger = complex_trigger
        self.kind = kind.upper()
        # self.next_action_ids = set()
        self.next_actions = list()
        self.callback = callback or self.none_callback
        self.callback_args = callback_args or ()
        self.callback_kwargs = callback_kwargs
        self.input = None

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
        # _actions = []
        if not isinstance(actions, (list, tuple, set)):
            # _actions.append(actions)
            actions = [actions]

        for act in actions:
            self.next_actions.append(act)
            # self.next_action_ids.add(act.id)

    def add_input(self, user_input):
        if self.kind == 'I':
            self.input = user_input
        raise AttributeError("Action of kind {} can't have input".format(self.kind))

    def get_input(self):
        if self.kind == 'I':
            return self.input
        raise AttributeError("Action of kind {} can't have input".format(self.kind))

    def check_trigger(self, trigger):
        if self.kind == 'I':
            self.input = trigger
            return True
        elif self.kind == 'M' and self.trigger == trigger:
            return True
        elif self.kind == 'C' and self.trigger == trigger.strip().replace('/', ''):
            return True

        return False

    def invoke_callback(self, *args, **kwargs):
        return self.callback(*args, *self.callback_args, input=self.input, **kwargs, **self.callback_kwargs)

    def clear_next_actions(self):
        self.next_actions.clear()

    @property
    def qualified_name(self):
        return '/{}'.format(self.trigger) if self.kind == 'C' else self.trigger if self.kind == 'M' else None

    def next_action_list(self):
        return [action.qualified_name for action in self.next_actions if action.qualified_name is not None]

    @staticmethod
    def none_callback(*args, **kwargs):
        return None

    @staticmethod
    def start_callback(*args, **kwargs):
        return "Welcome to my humble home :)"

    @staticmethod
    def unknown_callback(*args, **kwargs):
        return "Unknown action"

    @staticmethod
    def abort_callback(*args, **kwargs):
        return "Action aborted!"

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

# StartAction = Action('start', 'C', Action.start_callback)
# UnknownAction = Action('unknown', 'M', callback=Action.unknown_callback)
# UnknownAction.add_actions(StartAction)
#
# print(UnknownAction.next_action_list())
