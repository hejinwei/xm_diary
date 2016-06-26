import MongoDBUtil
import pymongo

db = MongoDBUtil.get_db()
diary_statistics = db.diary_statistics


def find_statistic_by_diary_id(diary_id):
    return diary_statistics.find_one({'diary_id': int(diary_id)})


def insert_or_update_view_number(diary_id, user_id):
    statistic = find_statistic_by_diary_id(diary_id)
    if statistic is None:
        diary_statistics.insert_one({"diary_id": int(diary_id), "user_id": int(user_id), "view_number": 1})
    else:
        diary_statistics.update({"diary_id": int(diary_id), "user_id": int(user_id)}, {'$inc': {'view_number': 1}})


def find_hot_top(user_id, limit_number):
    results = diary_statistics.find({'user_id': int(user_id)}).sort('view_number', pymongo.DESCENDING).limit(
        limit_number)
    return results
