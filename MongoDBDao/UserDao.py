import MongoDBUtil

db = MongoDBUtil.get_db()
users = db.users


def find_user(username):
    user = users.find_one({"username": username})
    return user


def find_user_by_user_id(user_id):
    user = users.find_one({"user_id": int(user_id)})
    return user
