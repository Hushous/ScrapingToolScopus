from dotenv import load_dotenv

from constants import constants_scopus_tool
from scraper import scopus_tool

load_dotenv()


def create_full_list(long_version: bool):
    """
    execute a search query, search for papers using different database input files and put together in a list
    """
    # scopus_tool.scrape_by_search_string(long_version)

    databases = [
        constants_scopus_tool.FILENAME_ACM,
        constants_scopus_tool.FILENAME_IEEE,
        constants_scopus_tool.FILENAME_SCIENCE_DIRECT,
    ]

    for item in databases:
        scopus_tool.scrape_papers_per_id(item, long_version)

    scopus_tool.create_continuous_list()


def scopus_search_string(long_version: bool):
    """
    start a search for papers
    use QUERY_STRING from .env
    use KEY (api_key) from .env
    long_version: true -> all papers, else df.head()
    """
    scopus_tool.scrape_by_search_string(long_version)


def scopus_per_id(library_name: str, long_version: bool):
    """
    Search for Papers via input .csv
    needs to contain column identifier: str
    :param long_version:
    :param library_name: name of database to search (acm, ieee, science_direct)
    """
    scopus_tool.scrape_papers_per_id(library_name, long_version)


scopus_tool.create_continuous_list()
