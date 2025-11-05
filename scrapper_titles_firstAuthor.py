from ScopusScrapus import ScopusSearchQuery
from os import getenv
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

key = getenv('KEY', "Key does not exist")
query_str = getenv('QUERYSTRING', "QueryString not existing")

params = {'query':query_str,
          'count':25,
          'view':'STANDARD'}

ssq = ScopusSearchQuery(key, params)

records = []

try:
    for paper in ssq:
        records.append(paper)  # each paper is usually a dict
except Exception as e:
    print("Error while fetching Scopus results:", e)

papers = pd.DataFrame()

# convert to DataFrame
if records:
    papers = pd.DataFrame(records)
    print("Retrieved", len(papers), "papers")
    reduced_df = papers[["dc:identifier","dc:title","dc:creator","prism:coverDate","citedby-count","subtypeDescription","openaccessFlag"]]
    print(reduced_df.head())
    reduced_df.to_csv("list_of_titles", sep=';', encoding='utf-8', index=False, header=True)
else:
    print("No papers found")

