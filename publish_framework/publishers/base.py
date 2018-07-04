from actions_framework.actions import Action
from publish_framework.filters.base import Filter
from publish_framework.manager import PublisherManager


class Publisher:
    STATE_ACTIVE = 'A'
    STATE_UNSUBSCRIBED = 'U'

    def __init__(self, name):
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
        print("check_subscriber_status: ", user_key, "and self.subscribers: ", self.subscribers)
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

    def filter_content(self, content):
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
            proceed, filtered_content = filter(filtered_content)
            if not proceed:
                break

        return proceed, filtered_content

    def publish(self, content):
        proceed, filtered_content = self.filter_content(content)
        if proceed:
            to = [key for key in self.subscribers.keys() if self.subscribers[key]['state'] == self.STATE_ACTIVE]
            PublisherManager.send_message(to=to, message=filtered_content)

            # TODO: to call a method that can publish the content
