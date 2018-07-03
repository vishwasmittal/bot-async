from managers.service_manager import BaseServiceManager


class PublisherManager(BaseServiceManager):
    def incoming_action_callback(self, session, action):
        message = action.callback(session)
        self.send_message(session.get('chat_id'), message, action.next_action_list)
