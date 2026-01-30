import os

import numpy as np
import pandas as pd
import requests
from ScopusScrapus import ScopusSearchQuery

from constants import constants_scopus_tool


def create_all_paper_csv(long_version: bool, databases: list):
    """
    create the full csv list, looking for all databases inserted.
    :param databases: list of all databases name (used in names of .csv data)
    :param long_version:
    """

    print("Start Scopus Scraping Process")
    scrape_by_search_string(long_version)

    print("Start Processing .csv Data")
    for item in databases:
        scrape_papers_per_id(item, long_version)

    try:
        __create_continuous_list()
    except Exception as err:
        print(f"Something went wrong!: {err}")


def scrape_by_search_string(long_version: bool):
    """
    do scopus search by query string derived from .env.
    outputs scopus_id as identifier, title, coverDate, citeCount, subTypeDescription, openAccessFlag and authors
    """

    key = os.getenv("KEY", "No Key established in .env")
    query_str = os.getenv("QUERYSTRING", "No Query String established in .env")
    params = {"query": query_str, "count": 25, "view": "STANDARD"}

    # create dataframe from search string
    papers = __search_scopus(key, params)

    # for testing purposes
    if not long_version:
        papers = papers.head()

    for item in papers.index:
        try:
            scopus_id = str(papers["identifier"][item])

            json_resp = __request_scopus_paper(key, scopus_id)

            authors = __author_join(json_resp)

            papers.loc[item, constants_scopus_tool.AUTHORS] = authors
            print(f"Adding {scopus_id} successful")

        except Exception as err:
            print(err)
            continue

    # adds a column of the origin as scopus to reidentify
    papers["origin"] = "scopus"

    filename = constants_scopus_tool.FILENAME_SCOPUS_QUERY
    print_to_csv(filename, papers)


def scrape_papers_per_id(library_name: str, long_version: bool):
    """
    scrape paper information per scopus id from scopus itself
    :param long_version: True if all papers are regarded, False if only 5
    :param library_name: name of the scraped library
    """

    key = os.getenv("Key", "No Key established in .env")

    input_file_path = constants_scopus_tool.FILEPATH_INPUT_OTHER_SEARCH
    file_name = constants_scopus_tool.FILENAME_BASE_SEARCH + library_name + ".csv"
    file_path = os.path.join(input_file_path, file_name)

    # create parent folder on the fly
    os.makedirs(input_file_path, exist_ok=True)

    ids = pd.read_csv(file_path, sep=";", encoding="utf-8")

    # only use 5 papers for testing purposes
    if not long_version:
        ids = ids.head()

    for item in ids.index:
        try:
            scopus_id = str(ids["identifier"][item])

            json_resp = __request_scopus_paper(key, scopus_id)

            core = json_resp.get("abstracts-retrieval-response", {}).get("coredata", {})

            ids.loc[item, constants_scopus_tool.TITLE] = core.get("dc:title") or None
            ids.loc[item, constants_scopus_tool.COVER_DATE] = (
                core.get("prism:coverDate") or None
            )
            ids.loc[item, constants_scopus_tool.CITED_COUNT] = (
                int(core.get("citedby-count", 0)) if core.get("citedby-count") else None
            )
            ids.loc[item, constants_scopus_tool.SUBTYPE_DESCRIPTION] = (
                core.get("subtypeDescription") or None
            )
            ids.loc[item, constants_scopus_tool.OPEN_ACCESS_FLAG] = (
                True if core.get("openaccessFlag") == "true" else False
            )

            authors = __author_join(json_resp)
            ids.loc[item, constants_scopus_tool.AUTHORS] = authors

            print(f"Adding {scopus_id} successful")

        except Exception as err:
            print(err)
            continue

    ids["origin"] = library_name
    ids = (
        ids[[c for c in ids.columns if c != "used"] + ["used"]]
        if "used" in ids.columns
        else ids
    )

    filename = constants_scopus_tool.FILENAME_BASE_NOT_SCOPUS + library_name
    print_to_csv(filename, ids)


def print_to_csv(file_name: str, df: pd.DataFrame):
    """
    :param file_name: Name of the file (with or without .csv)
    :param df: DataFrame to write
    """
    if df is not None:
        # Add .csv only if not already present (case-insensitive)
        if not file_name.lower().endswith(".csv"):
            file_name += ".csv"

        folder_name = constants_scopus_tool.FILEPATH_OUTPUT_SCOPUS_SEARCH
        file_path = os.path.join(folder_name, file_name)

        # create parent folder on the fly
        os.makedirs(folder_name, exist_ok=True)

        df.to_csv(file_path, sep=";", encoding="utf-8", index=False, header=True)


def __create_continuous_list():
    """
    Reads all .csv or .CSV files in a folder, concatenates them,
    ensures 'used' column exists, and fills missing entries with NaN.
    Throws out duplicate entries to ensure a unique titles list
    Saves the combined CSV to a .csv.
    """

    folder_path = constants_scopus_tool.FILEPATH_OUTPUT_SCOPUS_SEARCH

    csv_files = [f for f in os.listdir(folder_path) if f.lower().endswith(".csv")]

    if not csv_files:
        raise ValueError("No CSV files found in the specified folder.")

    dataframes = []

    column = constants_scopus_tool.USED

    for file in csv_files:
        full_path = os.path.join(folder_path, file)
        df = pd.read_csv(full_path, sep=";", encoding="utf-8")

        # Ensure the 'used' column exists
        if column not in df.columns:
            df[column] = np.nan
        else:
            # Fill missing values in the column
            df[column] = df[column].fillna(np.nan)

        dataframes.append(df)

    combined_df = pd.concat(dataframes, ignore_index=True)

    # drop duplicate titles
    unique_df = combined_df.drop_duplicates(subset=["title"], inplace=False)

    print_to_csv(constants_scopus_tool.FILENAME_ALL, unique_df)


def __search_scopus(key: str, params: dict) -> pd.DataFrame:
    """
    searches for all relevant papers to a query string derived from .env.
    :param key: api key of scopus
    :param params: dict of parameters to put for the search
    :return: dataframe of relevant information about searched papers
    """
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
        [
            "dc:identifier",
            "dc:title",
            "prism:coverDate",
            "citedby-count",
            "subtypeDescription",
            "openaccessFlag",
        ]
    ]

    papers = papers.rename(
        columns={
            "dc:identifier": constants_scopus_tool.IDENTIFIER,
            "dc:title": constants_scopus_tool.TITLE,
            "prism:coverDate": constants_scopus_tool.COVER_DATE,
            "citedby-count": constants_scopus_tool.CITED_COUNT,
            "subtypeDescription": constants_scopus_tool.SUBTYPE_DESCRIPTION,
            "openaccessFlag": constants_scopus_tool.OPEN_ACCESS_FLAG,
        }
    )

    papers[constants_scopus_tool.IDENTIFIER] = papers[
        constants_scopus_tool.IDENTIFIER
    ].str.replace("SCOPUS_ID:", "", regex=False)

    return papers


def __request_scopus_paper(key: str, identifier: str):

    response = requests.get(
        f"https://api.elsevier.com/content/abstract/scopus_id/{identifier}",
        headers={"Accept": "application/json"},
        params={"apiKey": key},
    )
    json_resp = response.json()

    return json_resp


def __author_join(json_resp: any) -> str:
    authors = (
        ", ".join(
            f"{a['preferred-name'].get('ce:given-name', '')} {a['preferred-name'].get('ce:surname', '')}".strip()
            for a in json_resp.get("abstracts-retrieval-response", {})
            .get("authors", {})
            .get("author", [])
        )
        or None
    )

    return authors
