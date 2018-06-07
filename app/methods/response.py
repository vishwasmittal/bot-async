from app.schema.response import ResponseSchema


def get_response(query):
    """
    Fetch a response from the appropriate backend for this query

    :param query: <class 'schema.query_resolver.Query'> object

    :return: A <class 'schema.response.Response'> object
    """
    response_dict = {
        "text": query.text + " -- response",
        "actions": [
            "action 1",
            "action 2",
            "action 3",
            "action 4",
            "action 5",
            "action 6",
            "action 7",
            "action 8",
            "action 9",
            "action 10",
        ]
    }

    return ResponseSchema().load(response_dict)
