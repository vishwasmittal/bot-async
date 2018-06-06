__all__ = ['send_response']


def send_response(validated_update):
    """
    Send response to the user for the message in a webhook request
    :param validated_update: telegram.schema.Update object for the webhook request
    :return: Nothing
    """

    # extract the query from the Update object
    # obtain result for this query object
    # serialize this result into the send_message format
    # use telegram methods to send the message

    from app.schema.query_resolver import Query
    query = Query.get_query_from_update(validated_update)

    # get the result for this query




    pass
