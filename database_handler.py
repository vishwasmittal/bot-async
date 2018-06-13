import pymongo

client = pymongo.MongoClient()
db = client.telegram_bot
bot_collection = db.chats


# making a function to store the data in the collections
def store_doc(message):
    if not isinstance(message, (list, tuple)):
        _message = [message]
    else:
        _message = message
    return bot_collection.insert_many(_message)
