class Filter:
    """ Base class for all the filters to the publishers """

    def __init__(self):
        pass

    async def execute(self, content, to):
        """
        Coroutine

        executes the filter
        """
        return await self.filter(content, to)

    async def filter(self, content, to):
        """
        Summary line
        ------------
        Coroutine

            Method to process the content. Override in the child class to apply complex filters

        Parameters
        ----------
        content: str
            content to be filtered
        to: list
            list of recipients of this content

        Returns
        -------
        tuple (bool, str, list)
            :Proceed: indicates if the data is fit for further processing (feed to next filter or publish)
            :filtered_content: filtered content
            :to: filtered list of recipients who can receive this content
        """

        return True, content, to
