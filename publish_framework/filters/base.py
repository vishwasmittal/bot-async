class Filter:
    """ Base class for all the filters to the publishers"""

    def __init__(self):
        pass

    def execute(self, content):
        return self.filter(content)

    def filter(self, content):
        """
        Method that processes the content
        :param content:
        :return: (bool:proceed, content)
            proceed: indicated if the data is fit to proceed further (to be operated on by next filter or to publish)
        """
        return True, content
