from app.schema.response import ResponseSchema


def get_response(query):
    """
    Fetch a response from the appropriate backend for this query

    :param query: <class 'schema.query_resolver.Query'> object

    :return: A <class 'schema.response.Response'> object
    """
    response_dict = {
        "text": query.text,  # + " -- response",
        "actions": [
            "/start",
            "https://google.com",
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
    print("response_dict: ", response_dict)
    response = ResponseSchema().load(response_dict)
    return response


START_KEYBOARD_ACTIONS = [
    '/news',
    '/trade',
    '/unsubscribe',
]

TRADE_KEYBOARD_ACTIONS = [
    # list of companies
    'ADANI',
    'Reliance',
    'Falana',
    'Dimka',
    'Lorem',
    'Ipsum',
    'dolor',
    'sit',
    'amet',
    '/abort',
    '/unsubscribe'
]



