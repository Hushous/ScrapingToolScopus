from dotenv import load_dotenv

from bib_tex import bib_tex_creation
from constants import constants_scopus_tool
from scraper import scopus_tool

load_dotenv()


def scrape_paper_information(long_version: bool):
    """
    scrape scopus per search query and use input files in /scraper/input to request
    all information about found papers
    :param long_version: True if all papers are considered, False else
    """

    databases = [
        constants_scopus_tool.FILENAME_ACM,
        constants_scopus_tool.FILENAME_IEEE,
        constants_scopus_tool.FILENAME_SCIENCE_DIRECT,
    ]

    scopus_tool.create_all_paper_csv(long_version, databases)


def create_bib_tex():
    """
    create a bib_tex file from the generated output file of scraper_paper_information
    """
    bib_tex_creation.create_bib_from_records()


# scrape_paper_information(False)
#create_bib_tex()
