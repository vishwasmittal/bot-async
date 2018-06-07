from datetime import datetime
from marshmallow import Schema, fields, pre_load, post_load
from .user import UserSchema
from .chat import ChatSchema
from .message_entity import MessageEntitySchema

__all__ = ['Message', 'MessageSchema']


class Message:
    def __init__(self, message_id, date, chat, message_from, text=None, entities=None):
        self.message_id = message_id
        self.date = date
        self.chat = chat
        self.message_from = message_from
        self.text = text
        self.entities = entities


class MessageSchema(Schema):
    message_id = fields.Int()
    date = fields.Int()  # timestamp
    chat = fields.Nested(ChatSchema)
    text = fields.Str(required=False)
    message_from = fields.Nested(nested=UserSchema, data_key="from", attribute="message_from", required=False)
    entities = fields.Nested(MessageEntitySchema, many=True, required=False)

    # forward_from
    # forward_from_chat
    # forward_from_message_id
    # forward_signature
    # forward_date
    # reply_to_message
    # edit_date
    # media_group_id
    # author_signature
    # caption_entities
    # autio
    # document
    # game
    # photo
    # sticker
    # video
    # voice
    # video_note
    # caption
    # contact
    # location
    # venue
    # new_chat_members
    # left_chat_member
    # new_chat_title
    # new_chat_title
    # new_chat_photo
    # group_chat_created
    # supergroup_chat_created
    # channel_chat_created
    # migrate_to_chat_id
    # migrate_from_chat_id
    # pinned_message
    # invoice
    # successful_payment
    # connected_website

    # @pre_load
    # def get_valid_datetime(self, data):
    #     date = data['date']
    #     # TODO: remove this
    #     import json; print('printing data from  MessageSchema\n', json.dumps(data, indent=4))
    #     data['date'] = datetime.fromtimestamp(date).isoformat()
    #     return data

    @post_load
    def get_object(self, data):
        return Message(**data)
