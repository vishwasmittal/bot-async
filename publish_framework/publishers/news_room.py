from publish_framework.publishers.base import Publisher


class NewsPublisher(Publisher):
    def __init__(self, name):
        super().__init__(name)


NewsPublisher = NewsPublisher('news-room')
