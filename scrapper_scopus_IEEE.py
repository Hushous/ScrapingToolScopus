import pandas as pd
import requests
import os
from dotenv import load_dotenv

load_dotenv()

ids = pd.read_csv("scopus_ids_IEEE_Explore", sep=';', encoding='utf-8')

API_KEY = os.getenv("KEY")

for item in ids.index:
    try:
        SCOPUS_ID = ids["identifier"][item]

        response = requests.get(f"https://api.elsevier.com/content/abstract/scopus_id/{SCOPUS_ID}", headers={"Accept": "application/json"}, params={"apiKey":API_KEY})
        json_resp = response.json()

        core = json_resp.get("abstracts-retrieval-response", {}).get("coredata", {})

        title = core.get("dc:title") or None
        cover_date = core.get("prism:coverDate") or None
        cited_count = int(core.get("citedby-count", 0)) if core.get("citedby-count") else None
        subtype_description = core.get("subtypeDescription") or None
        open_access_flag = True if core.get("openaccessFlag") == "true" else False

        authors = ", ".join(
            f"{a['preferred-name'].get('ce:given-name', '')} {a['preferred-name'].get('ce:surname', '')}".strip()
            for a in json_resp.get('abstracts-retrieval-response', {}).get('authors', {}).get('author', [])
        ) or None

        ids.loc[item, "title"] = title
        ids.loc[item, "coverDate"] = cover_date
        ids.loc[item, "citedCount"] = cited_count
        ids.loc[item, "subtypeDescription"] = subtype_description
        ids.loc[item, "openaccessFlag"] = open_access_flag
        ids.loc[item, "authors"] = authors
        ids = ids[[c for c in ids.columns if c != "used"] + ["used"]] if "used" in ids.columns else ids
        print(f"Adding {SCOPUS_ID} successful")

    except Exception as err:
        print(err)
        continue

if ids is not None:
    ids.to_csv("ieee_list", sep=';', encoding='utf-8', index=False, header=True)