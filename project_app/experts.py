from pymongo import MongoClient
import re
import pandas as pd


def get_db_handle(db_name, host, port):
    client = MongoClient(host=host,
                         port=int(port),
                         )
    db_handle = client[db_name]
    return db_handle, client


def get_collection_handle(db_handle, collection_name):
    return db_handle[collection_name]


# todo:
# Connection to server. You will need to change this to your server.
db_handle, mongo_client = get_db_handle('db_swansea',
                                        'mongodb+srv://admin:admin@cluster0.zotwq.mongodb.net/db_swansea?retryWrites=true&w=majority',
                                        27017,)
expertise_collection_handle = get_collection_handle(db_handle, 'api_basic_areasofexpertise')
# research_highlights_collection_handle = get_collection_handle(db_handle, 'api_basic_researchhighlights')
professors_collection_handle = get_collection_handle(db_handle, 'api_basic_professors')

profs = professors_collection_handle.find()
expertise = expertise_collection_handle.find()
# research = research_highlights_collection_handle.find()

profs = pd.DataFrame(list(profs))
expertise = pd.DataFrame(list(expertise))
# research = pd.DataFrame(list(research))

profs.drop(columns=['_id', 'id'], inplace=True)
expertise.drop(columns=['_id', 'id'], inplace=True)

df_joined = profs.merge(expertise, how='left', on='created_ID', suffixes=('_prof', '_expertise'))


def get_experts(keyword):
    return df_joined[df_joined['area'].str.contains(re.escape(keyword), na=False, case=False)].to_dict('records')
