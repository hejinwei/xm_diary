import pymongo


def get_db():
    client = pymongo.MongoClient("localhost")
    db = client.diary
    return db