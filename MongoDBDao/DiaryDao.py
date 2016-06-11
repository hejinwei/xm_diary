import MongoDBUtil
import pymongo

db = MongoDBUtil.get_db()
diaries = db.diaries


def find_diaries(user_id, page_num, page_size):
    skip_number = (page_num - 1) * page_size
    results = diaries.find({'user_id': int(user_id), 'delete_status': 0}).sort('date', pymongo.DESCENDING).skip(
            skip_number).limit(page_size)
    return results


def find_diaries_by_type(user_id, type, page_num, page_size):
    skip_number = (page_num - 1) * page_size
    results = diaries.find({'user_id': int(user_id), 'type': type, 'delete_status': 0}).sort('date',
                                                                                                 pymongo.DESCENDING).skip(
        skip_number).limit(page_size)
    return results


def find_diaries_count(user_id):
    return diaries.find({'user_id': int(user_id), 'delete_status': 0}).count()


def find_diaries_count_by_type(user_id, type):
    return diaries.find({'user_id': int(user_id), 'delete_status': 0, 'type': type}).count()


def insert_one_diary(diary_id, user_id, title, weather, type, date, content, private):
    diaries.insert_one({"id": diary_id, "user_id": user_id, "title": title,
                        "weather": weather, "type": type, "date": date, "content": content, "private": private,
                        "delete_status": 0})


def find_diary_by_id(diary_id):
    return diaries.find_one({'id': diary_id})


def delete_diary_by_id(diary_id):
    return diaries.update({'id': diary_id}, {'$set': {'delete_status': 1}})


def update_diary_id(diary_id, title, weather, type, date, content, private):
    diaries.update({'id': diary_id}, {'$set': {'title': title, 'weather': weather, 'type': type, 'date': date,
                                               'content': content, 'private': private}})
