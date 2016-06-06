import MongoDBUtil

db = MongoDBUtil.get_db()
ids = db.ids


def find_and_modify(name):
    new_id = ids.find_and_modify(update={"$inc": {'id': 1}}, query={"name": name}, upsert=True)
    return new_id
