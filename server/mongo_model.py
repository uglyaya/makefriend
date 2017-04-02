# coding=utf-8
import datetime
from bson import ObjectId
from mongothon import Schema, create_model
from pymongo import MongoClient
from makefriend.settings import MONGO_CONFIG


def get_mongo_conf(conf=None):
    _conf = conf or MONGO_CONFIG
    _h1, _h2 = _conf.get('CONN_ADDR1'), _conf.get('CONN_ADDR2')
    _mg_user, _mg_pass = _conf.get('username'), _conf.get('password')

    _host_list = []
    if _h1:
        _host_list.append(_h1)
    if _h2:
        _host_list.append(_h2)

    if _host_list:
        mongo = MongoClient(_host_list, replicaSet=_conf.get('REPLICAT_SET'))
        if _mg_user and _mg_pass:
            mongo.admin.authenticate(_mg_user, _mg_pass)
    else:
        mongo = MongoClient('127.0.0.1', 27017, connect=False, socketKeepAlive=True)
    return mongo


mongo = get_mongo_conf(MONGO_CONFIG)
db = mongo[MONGO_CONFIG['database']]

user_schema = Schema({
    'name': {'type': basestring},
    'seekingGender': {'type': basestring},
    'seekingAgeFrom': {'type': int},
    'seekingAgeTo': {'type': int},
    'rating': {'type': int},
    'sex': {'type': basestring},
    'location': {'type': dict},
    'socialInfo': {'type': dict},
    'interests': {'type': dict},
    "photos": {'type': list},
    "firstName": {'type': basestring},
    'fullYears': {'type': int},  # 年龄
    "birthday": {'type': basestring},
    "is_robot": {'type': bool},  # 是否是机器人
})

MUser = create_model(user_schema, db.user, "MUser")


def get_user_list(country_code, sex=None):
    _db = mongo['date_crawler']
    query = {'location.countryCode': country_code, 'photos': {'$exists': True}}
    if sex:
        query['sex'] = sex
    return _db.meetville_profiles.find(query).sort([('rating', -1), ]).limit(10)


def get_distinct_city_name(country_code):
    _db = mongo['date_crawler']
    return _db.meetville_profiles.distinct('location.cityName', {'location.countryCode': country_code})


if __name__ == '__main__':
    for user in get_user_list('US', 'female'):
        for photo in user.get('photos'):
            print photo['path']
