from dotenv import load_dotenv
from constants import constants_scopus_tool
from scraper import scopus_tool

load_dotenv()


def scopus_search_string():
    """
    start a search for papers
    use QUERY_STRING from .env
    use KEY (api_key) from .env
    """
    scopus_tool.scrape_by_search_string()


def scopus_per_id(library_name: str):
    """
    Search for Papers via input .csv
    csv needs to contain column identifier: str
    :param library_name: name of database to search (acm, ieee, science_direct)
    """
    scopus_tool.scrape_papers_per_id(library_name)


# scopus_per_id(constants_scopus_tool.FILENAME_ACM)
# scopus_per_id(constants_scopus_tool.FILENAME_IEEE)
# scopus_per_id(constants_scopus_tool.FILENAME_SCIENCE_DIRECT)
# scopus_search_string()
