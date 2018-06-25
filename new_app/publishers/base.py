class PublisherBase:
    def __init__(self, name, subscribers=None, publisher_callback=None):
        self.name = name
        # self.registered = False

        if subscribers is None:
            self.subscribers = set()
        else:
            self.subscribers = set(subscribers)

        self.publisher_callback = publisher_callback

    def add_subscribers(self, subscribers):
        if not isinstance(subscribers, (list, tuple, set)):
            subscribers = [subscribers]
        # self.subscribers += subscribers
        for sub in subscribers:
            self.subscribers.add(sub)

    def publish(self, content):
        message, args, kwargs = self.process_content(content)
        for subs in self.subscribers:
            self.publisher_callback(subs, message, *args, **kwargs)

    def process_content(self, content):
        print("called base process_content")
        return content, (), {}

