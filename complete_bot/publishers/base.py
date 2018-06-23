class PublisherBase:
    def __init__(self, name, subscribers=None):
        self.name = name
        # self.registered = False

        if subscribers is None:
            self.subscribers = list()
        elif not isinstance(subscribers, (list, tuple)):
            self.subscribers = [subscribers]
        else:
            self.subscribers = subscribers

        self.publisher_callback = None

    def add_subscribers(self, subscribers):
        if not isinstance(subscribers, (list, tuple)):
            subscribers = [subscribers]
        self.subscribers += subscribers

        # def register_as_publisher(self):
        # self.registered = True
        # return self.registered

    def publish(self, content):
        message, args, kwargs = self.process_content(content)
        for subs in self.subscribers:
            self.publisher_callback(subs, message, *args, **kwargs)

    def process_content(self, content):
        print("called base process_content")
        return content, (), {}
