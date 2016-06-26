import MongoDBUtil
import pymongo

db = MongoDBUtil.get_db()
personal_signs = db.personal_signs


def find_personal_sign_by_user_id(user_id):
    return personal_signs.find_one({'user_id': int(user_id)})


def save_or_update_personal_sign(user_id, sign_content):
    personal_sign = find_personal_sign_by_user_id(user_id)
    if personal_sign is None:
        personal_signs.insert_one({"user_id": int(user_id), "sign_content": sign_content})
    else:
        personal_signs.update({'user_id': int(user_id)}, {'$set': {'sign_content': sign_content}})
