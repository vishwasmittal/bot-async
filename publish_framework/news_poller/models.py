"""
Summary line
-----------
    Defines the class models and Marshmallow schemas for RSS news articles
"""

import datetime
from pprint import pprint
from marshmallow import Schema, fields, pre_load, post_load, pre_dump


class NewsItem(object):
    def __init__(self, title, summary, pub_date=datetime.datetime.now(), link="http://bl.ah", category=None,
                 source=None):
        self.source = source
        self.title = title
        self.summary = summary
        self.category = category
        self.pub_date = pub_date
        self.link = link


class RSS(object):
    def __init__(self, title, items, language='en', link="http://bit.ly", subtitle="fast_news"):
        self.language = language
        self.title = title
        self.link = link
        self.subtitle = subtitle
        self.items = items


class RSSSchema(Schema):
    language = fields.Str(data_key='language')
    title = fields.Str(data_key='title')
    link = fields.Url(data_key='link')
    subtitle = fields.Str(data_key='subtitle')
    items = fields.Nested('NewsItemSchema', exclude=('source',), many=True, data_key='entries')

    @pre_load
    def get_corr_data(self, data):
        corr_data = data['feed']
        corr_data['entries'] = data['entries']
        return corr_data

    @post_load
    def make_feed(self, data):
        return RSS(**data)


class NewsItemSchema(Schema):
    title = fields.Str(data_key='title')
    summary = fields.Str(data_key='summary')
    category = fields.Str(required=False, data_key='category')
    # pub_date = fields.DateTime(format='rfc822', data_key='published')
    link = fields.Url(data_key='link')

    @post_load
    def make_feed(self, data):
        return NewsItem(**data)

    # @pre_dump
    # def get_date_format(self, data):
    #     print(data['published'])
    #     return


# if __name__ == "__main__":
#     rSch = RSSSchema().loads(open('sample_json_feed.json').read())
#     pprint(RSSSchema().dumps(rSch, indent=4))
#     # print(RSSSchema().dumps(rSch, indent=4))
