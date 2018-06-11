import uuid


class Action(object):
    def __init__(self, trigger, kind='M', handler=None, next_actions=None, complex_trigger=False, ):
        self._id = uuid.uuid4()

        if kind.upper() not in ['C', 'M']:
            raise TypeError("'type' should be one of ['C', 'M']")
        # elif not Action.is_next_actions_correct(next_actions):
        #     raise TypeError("next_actions must a list of :class: Action")

        self.trigger = trigger
        self.complex_trigger = complex_trigger
        self.kind = kind.upper()
        self.next_actions = next_actions or []
        self.handler = handler

    def __repr__(self):
        return "Action(id={}, trigger={}, kind={})".format(self._id, self.trigger, self.kind)

    def get_id(self):
        return self._id

    def can_be_triggered(self, trigger, kind):
        if not self.complex_trigger:
            return self.trigger == trigger and self.kind == kind or self.kind == 'M'
        else:
            # TODO: add functions and use them to trigger the actions
            return True

    def get_next_actions(self):
        return self.next_actions

    def add_action(self, action):
        # _actions = []
        # if not isinstance(action, (list, tuple) ):
        #     _actions.append(action)
        #
        # #
        if not isinstance(action, Action):
            raise TypeError("action must an instance of :class: Action")

        self.next_actions.append(action)

    def add_actions(self, actions):
        if not Action.is_next_actions_correct(actions):
            raise TypeError("actions must a list of :class: Action")

            # for action in actions:
            # self.next_actions.append(action)
        self.next_actions += actions

    def export_action(self):
        # self.handler = json.dumps
        # action_dict = dict()
        # # print(self.next_actions)
        # print(self)
        # for a in self.next_actions:
        #     print(a)
        #     print(a.next_actions)
        action_dict = {
            'text': self.trigger,
            'kind': self.kind,
            'handler': {
                'module': self.handler.__module__,
                'name': self.handler.__name__
            },
            'next_actions': [next_action.export_action() for next_action in self.next_actions]
        }
        return action_dict

    @staticmethod
    def is_next_actions_correct(next_actions):
        if type(next_actions) == list:
            for action in next_actions:
                # if isinstance(action, Action):
                if not type(action) == Action:
                    return False
            return True
        else:
            return False

    @staticmethod
    def import_action(action_dict):
        if type(action_dict) is not dict:
            raise TypeError("'action_dict' must be a dict")
        else:
            next_actions = [Action.import_action(action) for action in action_dict.get('next_actions', [])]
            action = Action(action_dict['trigger'],
                            action_dict.get('type') or 'M',
                            handler=Action.get_handler(action_dict.get('handler', None)))
            action.add_actions(next_actions)
            return action

    @staticmethod
    def get_handler(handler):
        """
        To obtain proper handler for the action
        :param None/function/dict handler:
            Returns handler if it is None or a function.
            If dict is provided, it loads the function from the `module` and `name` of function provided
        :return: None or function
        """
        if handler is None or type(handler) == function:
            func = handler
        elif type(handler) == dict:
            try:
                module = __import__(handler['module'])
                func = getattr(module, handler['name'])
            except Exception as e:
                print(e)
                func = None
        else:
            func = None

        return func

# if __name__ == "__main__":
#     # action_dict = {
#     #     'trigger': 'start',
#     #     'type': 'C',
#     #     'next_actions': [
#     #         {
#     #             'trigger': 'news',
#     #             'type': 'C'
#     #         },
#     #         {
#     #             'trigger': 'unsubscribe',
#     #             'type': 'C',
#     #         },
#     #         {
#     #             'trigger': 'trade',
#     #             'type': 'C',
#     #             'next_actions': [
#     #                 {
#     #                     'trigger': 'reliance',
#     #                     # 'type': 'M'
#     #                 },
#     #                 {
#     #                     'trigger': 'Adani',
#     #                     # 'type': 'M'
#     #                 },
#     #                 {
#     #                     'trigger': 'PNB',
#     #                     # 'type': 'M'
#     #                 },
#     #             ]
#     #         },
#     #     ]
#     # }
#     # action = Action.import_action(action_dict)
#     # print(json.dumps(action.export_action(), indent=4))
#     print("__main__ bot_action")
#     pass
