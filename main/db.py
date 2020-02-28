from flask import current_app as app

from flask_pymongo import PyMongo
from bson.json_util import dumps
from pprint import pprint
from bson.objectid import ObjectId
import urllib.parse
from apis import utils

class MongoDB():

    def __init__(self):
        self.utils = utils.Utils()
        self.config = self.utils.get_config()
        dbconfig = self.db_config()
        self.connect()
    
    def connect(self):
        self.mongo = PyMongo(app)
    
    def db_config(self):
        app.config["MONGO_DBNAME"] = self.config['DB_NAME']
        username = urllib.parse.quote_plus(self.config['MONGO_USER'])
        password = urllib.parse.quote_plus(self.config['MONGO_PASS'])
        mongo_uri = f"mongodb://{username}:{password}@localhost:27017/{self.config['DB_NAME']}?authSource={self.config['MONGO_AUTH_SOURCE']}"
        app.config["MONGO_URI"] = mongo_uri

    def find(self, collection, condition):
        if condition:
            results = self.mongo.db[collection].find(condition)
        else:
            results = self.mongo.db[collection].find()

        resp = dumps(results)
        # document = client.db.collection.find_one({'_id': ObjectId(post_id)})
        return resp
    
    def add(self, obj):
        """
        Takes data obj as input and returns the _id after saving
        """
        _id = self.mongo.db.collection.save(obj)

        return _id


    def update(self, _id, obj):
        """
        Updates the row based on _id
        """
        if _id:
            # Update record based on _id
            return _id
        else:
            return '_id is required'