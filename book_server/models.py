from pprint import pprint
from django.db import models

# Create your models here.
from makefriend.settings import MONGO_CONFIG
from server.mongo_model import mongo

db = mongo['date_crawler']
c_story_detail = db['story_detail']
c_story_list = db['unpacked_story']


def get_story_detail_by_id(object_id):
    story_detail = c_story_detail.find_one({'objectId': object_id})
    return story_detail


category_list = [
    "Sci-Fi",
    "Romance",
    "Drama",
    "Horror",
    "Fantasy",
    "Mystery",
    "Paranormal",
    "Thriller",
    "Comedy",
    'Hotest',
]


def get_story_list_by_category(category, limit=50):
    if category != 'Hotest':
        return c_story_list.find({'genre': category}).limit(50)
    elif category == 'All':
        return c_story_list.find({}).limit(50)
    else:
        return c_story_list.find().sort([('commentCount', -1), ]).limit(50)


if __name__ == '__main__':
    # print get_story_detail_by_id('EVj8HObCmo')
    #
    # for item in get_story_detail_by_id('EVj8HObCmo')['results']:
    #     pprint(item)
    #     print item['isTypingIntroDuration']
    #     print item['sender']['name']
    #     print item['text']
    #     print item['ordinalInStory']
    #     print '\n'

    for book in get_story_list_by_category('Hotest'):
        # print book['genre']
        print book['title']
        print book['objectId']
        pprint(book)
        break

    # for book in get_story_list_by_category('Hotest'):
    #     # print book['title']
    #     # print book['commentCount']
    #     print book['objectId']
    #     story_detail = get_story_detail_by_id(book['objectId'])
    #     results = story_detail['results']
    #     for result in results:
    #         try:
    #             result['text']
    #         except:
    #             pprint(result)
