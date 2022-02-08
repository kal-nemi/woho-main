from pymongo import MongoClient
import re
import pandas as pd

# def get_db_handle(db_name, host, port):
    
#     db_handle = client[db_name]
#     return db_handle, client

# def get_collection_handle(db_handle, collection_name):
#     return db_handle[collection_name]\

# client = MongoClient('mongodb+srv://vishal:Augmentr2020@cluster0.om3sd.mongodb.net/test')\

# db_handle, mongo_client = get_db_handle('knowledge_graph',
#                                         # 'mongodb+srv://admin:admin@cluster0.zotwq.mongodb.net/db_swansea?retryWrites=true&w=majority',
#                                         'mongodb+srv://vishal:Augmentr2020@cluster0.om3sd.mongodb.net/test',
#                                         # 'mongodb+srv://vishal:*****@cluster0.om3sd.mongodb.net/test?authSource=admin&replicaSet=atlas-3pfyvp-shard-0&readPreference=primary&appname=MongoDB%20Compass&ssl=true',
#                                         27017,)
# expertise_collection_handle = get_collection_handle(db_handle, 'api_basic_areasofexpertise')