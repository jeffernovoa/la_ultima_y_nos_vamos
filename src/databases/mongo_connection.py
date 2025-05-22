from pymongo import MongoClient

class MongoConnection:
    def __init__(self, uri="mongodb://localhost:27017", db_name="votacion_db"):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]

    def get_collection(self, name):
        return self.db[name]
