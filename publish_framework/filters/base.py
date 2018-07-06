class Filter:
    """ Base class for all the filters to the publishers"""

    def __init__(self):
        pass

    def execute(self, content, to):
        return self.filter(content, to)

    async def filter(self, content, to):
        """

        Method that processes the content
        :param to: list of recipients of this content
        :param content:
        :return: (bool:proceed, content, to)
            proceed: indicated if the data is fit to proceed further (to be operated on by next filter or to publish)
            to: filtered list of recipients
        """
        return True, content, to
