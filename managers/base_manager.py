"""
This module contains a parent class for the managers of all the frameworks that are to be inserted in the system
"""

from managers.storage import StorageManager
from managers.actions import ActionManager
from actions_framework.actions import Action


class FrameworkManager(StorageManager):
    def __init__(self, name):
        super().__init__(name)

        self.main_action = ActionManager.register_publisher(self.main_action, self.incoming_action_callback)

    def incoming_action_callback(self, session, action):
        raise NotImplementedError("incoming_action_callback() not implemented")

