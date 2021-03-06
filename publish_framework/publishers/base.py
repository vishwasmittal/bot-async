import asyncio

from actions_framework.actions import Action
from publish_framework.filters.base import Filter
from publish_framework.manager import PublisherManager
from managers.storage import StorageManager


class Publisher(StorageManager):
    """
    Summary line
    ------------
        Base Class for all the publishers
    """

    # Subscription state for a user
    STATE_ACTIVE = 'A'
    STATE_UNSUBSCRIBED = 'U'

    def __init__(self, name):
        super().__init__(name)
        self.name = name
        self.subscribers = {}
        self.filters = list()

        self.subscribe_action = Action(name, 'M', self.add_sub)
        self.unsubscribe_action = Action(name, 'M', self.remove_sub)

        PublisherManager.register_publisher(name, self.subscribe_action, self.unsubscribe_action,
                                            self.check_subscriber_status)

    def check_subscriber_status(self, user_key):
        """ user_key = session['chat_id]

        :returns: True if already subscribed or False if not subscribed or unsubscribed
        """
        # print("check_subscriber_status: ", user_key, "and self.subscribers: ", self.subscribers)
        if user_key not in self.subscribers or self.subscribers[user_key]['state'] == self.STATE_UNSUBSCRIBED:
            return False
        return True

    def add_sub(self, session, *args, **kwargs):
        self.subscribers[session['chat_id']] = {
            'state': self.STATE_ACTIVE
        }
        return "You have been subscribed to {}".format(self.name)

    def remove_sub(self, session, *args, **kwargs):
        self.subscribers[session['chat_id']] = {
            'state': self.STATE_UNSUBSCRIBED
        }
        return "You have been removed from {}".format(self.name)

    def add_filter(self, content_filter):
        """
        Add the filters. Filters will be executed in the order in which they are added
        :param content_filter: And object of class:filters.base.Filter or a method
                            accepting the content to be filtered.
        :return: nothing
        """
        if isinstance(content_filter, Filter):
            self.filters.append(content_filter.execute)
        else:
            self.filters.append(content_filter)

    async def filter_content(self, content, to):
        """
        Returns the filtered content after calling all the filtered in the sequence they are added
        :param content: content to be filtered
        :return: (bool: proceed, filtered_content)
            proceed: tells whether to proceed with this content or not
            filtered_content: result after filtering
        """
        proceed = True
        filtered_content = content
        for filter in self.filters:
            filter_coro = asyncio.coroutine(filter)
            proceed, filtered_content = await filter_coro(filtered_content, to)
            if not proceed:
                break

        return proceed, filtered_content, to

    async def publish(self, content):
        """  Call this function and pass the content to send it to all the subscribed users """
        to = [key for key in self.subscribers.keys() if self.subscribers[key]['state'] == self.STATE_ACTIVE]
        filter_coro = asyncio.coroutine(self.filter_content)
        proceed, filtered_content, to = await filter_coro(content, to)
        if proceed:
            await PublisherManager.send_message(to=to, message=filtered_content)
