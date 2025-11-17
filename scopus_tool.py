import pandas as pd
from ScopusScrapus import ScopusSearchQuery
import requests


'''
scrapes scopus for papers using a search string and creating a dataframe from it
'''
def scrape_by_search_string(key: str, params: dict, file_name: str):
    ssq = ScopusSearchQuery(key, params)
    records = []

    try:
        for paper in ssq:
            records.append(paper)  # each paper is usually a dict
    except Exception as e:
        print("Error while fetching Scopus results:", e)

    papers = pd.DataFrame(records)
    print("Retrieved", len(papers), "papers")

    papers = papers[
        ["dc:identifier", "dc:title", "prism:coverDate", "citedby-count", "subtypeDescription",
         "openaccessFlag"]]

    papers = papers.rename(
        columns={"dc:identifier": "identifier", "dc:title": "title", "prism:coverDate": "coverDate",
                 "citedby-count": "citedCount"})

    for item in papers.index:
        try:
            SCOPUS_ID = papers["identifier"][item]

            response = requests.get(f"https://api.elsevier.com/content/abstract/scopus_id/{SCOPUS_ID}",
                                    headers={"Accept": "application/json"}, params={"apiKey": key})
            json_resp = response.json()

            authors = ", ".join(
                f"{a['preferred-name'].get('ce:given-name', '')} {a['preferred-name'].get('ce:surname', '')}".strip()
                for a in json_resp.get('abstracts-retrieval-response', {}).get('authors', {}).get('author', [])
            ) or None

            papers.loc[item, "authors"] = authors
            print(f"Adding {SCOPUS_ID} successful")

        except Exception as err:
            print(err)
            continue

    print_to_csv(file_name, papers)


'''
scrape scopus for papers using a list of scopus ids retracted manually (for sources from other libraries)
adds in all relevant information and all authors required
'''
def scrape_papers_per_id(params: dict,input_file_path: str, file_name: str):
    ids = pd.read_csv(input_file_path, sep=';', encoding='utf-8')

    for item in ids.index:
        try:
            SCOPUS_ID = ids["identifier"][item]

            response = requests.get(f"https://api.elsevier.com/content/abstract/scopus_id/{SCOPUS_ID}", headers={"Accept": "application/json"}, params=params)
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

    print_to_csv(file_name, ids)

'''
csv saving function to align parameters
'''
def print_to_csv(file_name: str, df: pd.DataFrame):
    if df is not None:
        file_path = "output_files/" + file_name
        df.to_csv(file_path, sep=';', encoding='utf-8', index=False, header=True)



