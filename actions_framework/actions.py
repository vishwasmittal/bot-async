import asyncio
import uuid


# from managers.actions import ActionManager


class Action(object):
    # for slash command, simple message or input type respectively
    ACTION_KINDS = ['C', 'M', 'I']

    def __init__(self, trigger, kind, callback=None, id=None, *callback_args, **callback_kwargs):
        """
        Summary line
        -----------
        Extended description of function.

        Parameters
        ----------
        trigger : str
            Text that represent this action
        kind : str
            C: slash command, M: simple message or I: custom input from user
        callback : function
            Callback function to be invoked when this action is taken
        id : str
            special id for the action
        callback_args : args
            args to be passed to the callback function when invoking it
        callback_kwargs : kwargs
            kwargs to be passed to the callback function when invoking it

        Returns
        -------

        """

        self.id = id or str(uuid.uuid4())

        if kind.upper() not in self.ACTION_KINDS:
            raise TypeError("'type' should be one of {}".format(self.ACTION_KINDS))

        self.trigger = trigger
        self.kind = kind.upper()
        self.next_actions = list()
        self.callback = callback or self.none_callback
        self.callback_args = callback_args or ()
        self.callback_kwargs = callback_kwargs

        # only for 'I' kind actions
        self.input = None

    def __repr__(self):
        return "Action(id={}, trigger={}, kind={})".format(self.id, self.trigger, self.kind)

    def get_id(self):
        """ return self.id """
        return self.id

    def get_next_actions(self):
        """ returns the list containing all the actions next in the line """
        return self.next_actions

    def add_actions(self, actions):
        """ Append `actions` to the of next_actions """
        if not isinstance(actions, (list, tuple, set)):
            actions = [actions]

        for act in actions:
            self.next_actions.append(act)

    def add_input(self, user_input):
        if self.kind == 'I':
            self.input = user_input
        raise AttributeError("Action of kind {} can't have input".format(self.kind))

    def get_input(self):
        if self.kind == 'I':
            return self.input
        raise AttributeError("Action of kind {} can't have input".format(self.kind))

    def check_trigger(self, trigger):
        """ Checks if the given trigger can invoke the action or not """
        if self.kind == 'I':
            # if this is an input action, it can be invoked.
            # TODO: add regular expressions for filtering between multiple input actions
            self.input = trigger
            return True
        elif self.kind == 'M' and self.trigger == trigger:
            return True
        elif self.kind == 'C' and self.trigger == trigger.strip().replace('/', ''):
            return True

        return False

    async def invoke_callback(self, *args, **kwargs):
        """
        Coroutine

        Invokes the callback passes the inputs, args and kwargs along with the previously provided args and kwargs
        """
        callback_coro = asyncio.coroutine(self.callback)
        return await callback_coro(*args, *self.callback_args, input=self.input, **kwargs, **self.callback_kwargs)

    def clear_next_actions(self):
        self.next_actions.clear()

    @property
    def qualified_name(self):
        """
        Provides the qualified name for the action

        :C: name = trigger as Slash Command
        :M: name = Trigger
        :I: name = None
        """
        return '/{}'.format(self.trigger) if self.kind == 'C' else self.trigger if self.kind == 'M' else None

    def next_action_list(self):
        """ returns the list of next actions that can be presented as keyboard buttons """
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
