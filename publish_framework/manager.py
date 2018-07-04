from managers.service_manager import BaseServiceManager
from managers.actions import StartAction
from actions_framework.actions import Action

AbortAction = Action('abort', 'C', Action.abort_callback)
AbortAction.add_actions(StartAction)


class PublisherManager(BaseServiceManager):
    def __init__(self, name):
        super(PublisherManager, self).__init__(name)
        """
        self.main_action defines the parent action for this service
        self.users['subscribed'] defines users who are subscribed to this service
        self.users['unsubscribed'] defines those who have unsubscribed
        self.send_message(to, message, next_actions) sends message to others

        """

        self.publishers = {}

        self.action_subscribe = Action('subscribe', 'C', self.subscribe_callback)
        self.action_unsubscribe = Action('unsubscribe', 'C', self.unsubscribe_callback)

        self.main_action.add_actions([self.action_subscribe, self.action_unsubscribe, AbortAction])

    def subscribe_callback(self, session, *args, **kwargs):
        user_key = session['chat_id']
        self.action_subscribe.clear_next_actions()
        for publisher in self.publishers:
            if not self.publishers[publisher]['status_check_callback'](user_key):
                # if user is not subscribed to this publisher
                subs_action = self.publishers[publisher]['subscribe_action']
                subs_action.clear_next_actions()
                subs_action.add_actions([self.action_subscribe, self.action_unsubscribe, AbortAction])
                self.action_subscribe.add_actions(subs_action)

        self.action_subscribe.add_actions(AbortAction)

        return "Choose from the options"

    def unsubscribe_callback(self, session, *args, **kwargs):
        user_key = session['chat_id']
        self.action_unsubscribe.clear_next_actions()
        for publisher in self.publishers:
            if self.publishers[publisher]['status_check_callback'](user_key):
                # if user is not subscribed to this publisher
                unsubs_action = self.publishers[publisher]['unsubscribe_action']
                unsubs_action.clear_next_actions()
                unsubs_action.add_actions([self.action_subscribe, self.action_unsubscribe, AbortAction])
                self.action_unsubscribe.add_actions(unsubs_action)

        self.action_unsubscribe.add_actions(AbortAction)
        return "Choose from the options"

    def incoming_action_callback(self, session, action):
        message = action.callback(session)
        self.send_message(session.get('chat_id'), message, action.next_action_list())

    def register_publisher(self, name, subscribe_action, unsubscribe_action, status_check_callback):
        self.publishers[name] = {
            'subscribe_action': subscribe_action,
            'unsubscribe_action': unsubscribe_action,
            'status_check_callback': status_check_callback,
        }


PublisherManager = PublisherManager('publisher')
