from pymongo import MongoClient
from config import mongo_db_credentail

def mongo_connect():
    args = mongo_db_credentail
    mongo_client = MongoClient(args)
    return mongo_client

def get_client_db(db_name=''):
    mongo_client = mongo_connect()
    return mongo_client[str(db_name)]
