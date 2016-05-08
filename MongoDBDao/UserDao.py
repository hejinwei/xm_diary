import MongoDBUtil

db = MongoDBUtil.get_db()
users = db.users


def find_user(username):
    user = users.find_one({"username": username})
    return user
