import pandas as pd
import requests
import os
from dotenv import load_dotenv

load_dotenv()

titles_and_first_author = pd.read_csv("list_of_titles", sep=';', encoding='utf-8')

API_KEY = os.getenv("KEY")

titles_and_first_author = titles_and_first_author.drop(columns=["dc:creator"])
titles_and_first_author = titles_and_first_author.rename(columns={"dc:identifier":"identifier","dc:title":"title","prism:coverDate":"coverDate","citedby-count":"citedCount"})

for item in titles_and_first_author.index:
    try:
        SCOPUS_ID = titles_and_first_author["identifier"][item]

        response = requests.get(f"https://api.elsevier.com/content/abstract/scopus_id/{SCOPUS_ID}", headers={"Accept": "application/json"}, params={"apiKey":API_KEY})
        json_resp = response.json()

        authors = ", ".join(
            f"{a['preferred-name'].get('ce:given-name', '')} {a['preferred-name'].get('ce:surname', '')}".strip()
            for a in json_resp.get('abstracts-retrieval-response', {}).get('authors', {}).get('author', [])
        ) or None

        titles_and_first_author.loc[item, "authors"] = authors
        print(f"Adding {SCOPUS_ID} successful")

    except Exception as err:
        print(err)
        continue
        #BUG WITH AMBIGIOUS DATAFRAME maybe use len(df)

if titles_and_first_author is not None:
    titles_and_first_author.to_csv("list_of_authors", sep=';', encoding='utf-8', index=False, header=True)
