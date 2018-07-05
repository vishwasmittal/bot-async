from marshmallow import fields, Schema, post_load


class InputMessageContent:
    def __init__(self, message_text):
        self.message_text = message_text


class InputTextMessageContentSchema(Schema):
    message_text = fields.Str()

    @post_load
    def return_objec(self, data):
        return InputMessageContent(**data)


class InlineQueryResultArticle:
    def __init__(self, type, id, title, input_message_content):
        self.type = type
        self.id = id
        self.title = title
        self.input_message_content = input_message_content


class InlineQueryResultArticleSchema(Schema):
    type = fields.Str()
    id = fields.Str()
    title = fields.Str()
    input_message_content = fields.Nested(InputTextMessageContentSchema)

    @post_load
    def return_objec(self, data):
        return InlineQueryResultArticle(**data)


class InlineQuery:
    def __init__(self, inline_query_id, results):
        self.inline_query_id = inline_query_id
        self.results = results


class InlineQuerySchema(Schema):
    inline_query_id = fields.Str(required=True)
    results = fields.Nested(InlineQueryResultArticleSchema, many=True)

    @post_load
    def return_objec(self, data):
        return InlineQuery(**data)
