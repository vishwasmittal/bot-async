from publish_framework.filters.base import Filter


class Publisher:
    STATE_ACTIVE = 'A'
    STATE_MUTE = 'M'
    STATE_UNSUBSCRIBED = 'U'

    def __init__(self, name):
        self.name = name
        self.subscribers = {}
        self.filters = list()

    def add_sub(self, user_key):
        self.subscribers[user_key] = {
            'state': self.STATE_ACTIVE
        }

    def mute_sub(self, user_key):
        self.subscribers[user_key] = {
            'state': self.STATE_MUTE
        }

    def remove_sub(self, user_key):
        self.subscribers[user_key] = {
            'state': self.STATE_UNSUBSCRIBED
        }

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
        # TODO: to call a method that can publish the content
