from new_app.publishers.base import PublisherBase


class NewsPublisher(PublisherBase):
    def __init__(self, subscribers=None, publisher_callback=None):
        super().__init__(name="News-Room", subscribers=subscribers, publisher_callback=publisher_callback)

    def process_content(self, content):
        return str(content[0].items[0].link), (), {}


NewsPublisher = NewsPublisher()     # singleton class
