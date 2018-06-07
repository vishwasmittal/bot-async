from app.schema.response import ResponseSchema


def get_response(query):
    response_dict = {
        "text": query.text + " -- response",
        "actions": [
            "action 1",
            "action 2",
            "action 3"
        ]
    }

    return ResponseSchema().load(response_dict)
