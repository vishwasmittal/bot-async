from .base import PublisherBase


class NewsPublisher(PublisherBase):
    def __init__(self, subscribers=None):
        subscribers = [563546980]
        super().__init__(name="News-Room", subscribers=subscribers)

    def process_content(self, content):
        # self.publish(message)
        print("called news_publisher process_content")
        print(type(content))
        print(content[0].items[0].link)
        return str(content[0].items[0].link), (), {}



