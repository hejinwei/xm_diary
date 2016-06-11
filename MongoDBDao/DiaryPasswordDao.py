import MongoDBUtil

db = MongoDBUtil.get_db()
diary_passwords = db.diary_passwords


def insert_or_update(diary_id, diary_password):
    diary_password_obj = diary_passwords.find_one({'diary_id': diary_id})
    if diary_password_obj is None:
        diary_passwords.insert_one({'diary_id': diary_id, 'diary_password': diary_password})
    else:
        diary_passwords.update({'diary_id': diary_id}, {'$set': {'diary_password': diary_password}})


def find_by_diary_id(diary_id):
    diary_password_obj = diary_passwords.find_one({'diary_id': diary_id})
    return diary_password_obj
