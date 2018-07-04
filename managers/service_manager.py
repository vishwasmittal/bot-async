"""
This module contains a parent class for the managers of all the frameworks that are to be inserted in the system
"""

from managers.storage import StorageManager
from managers.actions import ActionManager
from managers.interaction import InteractionManager
from actions_framework.actions import Action


class BaseServiceManager(StorageManager):
    def __init__(self, name):
        super().__init__(name)

        self.main_action = ActionManager.register_service(self.name, self.incoming_action_callback)

    def incoming_action_callback(self, session, action):
        """ What to do when an action is transferred to this manager"""
        raise NotImplementedError("incoming_action_callback() not implemented")

    def send_message(self, to, message, next_actions=None):
        """ Send message to the user """
        InteractionManager.send_message(to=to, message=message, next_actions=next_actions)

    def register_action(self, action):
        """ Register actions for the service """
        self.main_action.add_actions(action)
