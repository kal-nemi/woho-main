import pandas as pd
import re


def companies_data(keyword):
    df = pd.read_excel(r'cohort_data.xlsx')
    df = df.filter(['Company Name', 'Industry'])
    a = df[df['Industry'].str.contains(re.escape(keyword), na=False, case=False)].to_dict('results')
    # print(a)
    return a

# print(companies_data("AI"))
# company = df.to_dict(orient="index")
# # print(company)
# companies= []
# for i in company:
#     all = company[i]
#     companies.append({all['Company Name'] : all['Industry'].split('/')})
