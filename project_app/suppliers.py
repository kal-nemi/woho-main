from pymongo import MongoClient
import pandas as pd

import re

def get_db_handle(db_name, host, port):
    client = MongoClient(host=host,
                         port=int(port),
                         )
    db_handle = client[db_name]
    return db_handle, client

def get_collection_handle(db_handle, collection_name):
    return db_handle[collection_name]

# def read_data(keyword):

#     # todo:
#     # Connection to server. You will need to change this to your server.
#     db_handle, mongo_client = get_db_handle('scm',
#                                             '',
#                                             27017, )
#     suppliers_collection_handle = get_collection_handle(db_handle, 'supplier_data')
#     suppliers = suppliers_collection_handle.find()

#     df = pd.DataFrame(list(suppliers))
    
#     a = df[df['profile'].str.contains(re.escape(keyword), na=False, case=False)].to_dict('results')
#     return a

def read_data_csv(keyword):
    """"
    Description: This function is designed to read a csv file  and perform a search on profile column.
    Input: Keyword can be a list of keyword or a sigle word on which search is to be performed
    Output: returns the result of search in list format
    """
    if type(keyword) == list:   #if keyword is list
        pattern=keyword[0]
        for keyword in keyword[1:]:
            pattern=pattern+'|'+keyword
        df = pd.read_csv('supplier_data.csv')   #reading a file
        results = df[df['profile'].str.contains(pattern, na=False, case=False)].to_dict('results') #keyword search
    else:   #if keyword is a string
        pattern=keyword
        df = pd.read_csv('supplier_data.csv')   #reading a file
        results = df[df['profile'].str.contains(re.escape(pattern), na=False, case=False)].to_dict('results') #keyword search
    return results  #returning results





    



