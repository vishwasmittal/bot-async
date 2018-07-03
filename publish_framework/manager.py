from managers.service_manager import BaseServiceManager


class PublisherManager(BaseServiceManager):
    def __init__(self, name):
        super(PublisherManager, self).__init__(name)
        """
        self.main_action defines the parent action for this service
        self.users['subscribed'] defines users who are subscribed to this service
        self.users['unsubscribed'] defines those who have unsubscribed
        self.send_message(to, message, next_actions) sends message to others

        """

    def incoming_action_callback(self, session, action):
        message = action.callback(session)
        self.send_message(session.get('chat_id'), message, action.next_action_list())


PublisherManager = PublisherManager('publisher')
