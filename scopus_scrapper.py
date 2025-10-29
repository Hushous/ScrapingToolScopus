from ScopusScrapus import ScopusSearchQuery
from os import getenv
from dotenv import load_dotenv

load_dotenv()

key = getenv('KEY', "Key does not exist")
query_str = getenv('QUERYSTRING', "QueryString not existing")
date_str = getenv('DATESTRING', "DateString not existing")

params = {'query':query_str, 'date':date_str}

ssq = ScopusSearchQuery(key, params)

defaultParams = {'count':250,
    'view':'COMPLETE'}

try:
    for paper in ssq:
        print(str(paper))
except Exception as e:
    print(e)