
import pymongo
import pandas as pd

from decouple import config


import re
# admin = config('DB_ADMIN')
# passwd = config('DB_PASS')
# cluster_url = config('CLUSTER_URL')


# conn = pymongo.MongoClient(f'mongodb+srv://{admin}:{passwd}@{cluster_url}',ssl=True,ssl_cert_reqs=ssl.CERT_NONE)

# db = conn['scrape_data']
# cs = db['tenders']
# print(cs)

# df_casestudies = pd.DataFrame(cs.find())
# # df_casestudies = df_casestudies.drop(columns=['_id'], inplace=True)

# print(df_casestudies)
# # tenders = {}
# sumry = df_casestudies['title'].tolist()
# # tender {
# #       title : df_casestudies['title'].tolist()
# # 
# # }
# # 
# print(sumry)

def clean_contact_value(results):
    # cleaning tender value 
    for tender in results:
        # convert contract to string if its in float and perform cleaning on contract value
        if type(tender['contract_value'])==float:
            tender['contract_value']=str(tender['contract_value'])
        fun = lambda i: i.rsplit('£', 1)[-1]
        temp = fun(tender['contract_value']).replace('NA','0').replace('nan','0').replace(',','')
        #convert all contract values to float after cleaning
        tender['contract_value']=float(temp)
        
    return results

def read_data_csv2(keyword):
    """"
    Description: This function is designed to read a csv file  and perform a keyword search on profile column.
    Input: Keyword is the word on which search is to be performed
    Output: returns the result of of search in list format
    """
    df = pd.read_csv('tenders.csv')   #reading a file
    # contractValue_frm_tender(df)
    results = df[df['summary'].str.contains(re.escape(keyword), na=False, case=False)].to_dict('results') #keyword search

    results=clean_contact_value(results)

    return results  #returning results
