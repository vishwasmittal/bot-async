from managers.service_manager import BaseServiceManager


class HealthManager(BaseServiceManager):
    """
    NOTE: Make this a singleton class

    The Manager is automatically registered with the bot as soon as its instance is defined
    """

    def __init__(self, service_name):
        super().__init__(service_name)

    async def incoming_action_callback(self, session, action):
        message = action.invoke_callback(session=session)
        await self.send_message(session.get('chat_id'), message, action.next_action_list())


HealthManager = HealthManager('health')
