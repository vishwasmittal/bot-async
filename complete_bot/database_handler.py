import pymongo

client = pymongo.MongoClient()


class DBHandler:
    def __init__(self, db_name):
        self.db = client[db_name]
        # self.bot_collection = self.db[collection_name]

    def insert(self, documents, collection):
        if not isinstance(documents, (list, tuple)):
            _documents = [documents]
        else:
            _documents = documents
        col_instance = self.db[collection]
        return col_instance.insert_many(_documents)


class BotDBHandler(DBHandler):
    def __init__(self, db_name='telegram_bot'):
        super().__init__(db_name)

    def save_conversation(self, messages):
        CHAT_COLLECTION = 'conversations'
        self.insert(messages, CHAT_COLLECTION)

    save_chat = save_conversation

    def add_publishers(self, publisher):
        PUB_COLLECTION = "publishers"
        self.insert(publisher, PUB_COLLECTION)


class NewsDBHandler(DBHandler):
    def __init__(self, db_name='news_room'):
        super().__init__(db_name)

    def insert_news(self, news):
        NEWS_COLLECTION = 'news'
        self.insert(news, NEWS_COLLECTION)
