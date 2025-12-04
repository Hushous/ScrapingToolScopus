import os

import pandas as pd
import pybliometrics
from pybliometrics.scopus import AbstractRetrieval

from constants import constants_scopus_tool


def create_bib_from_records(output_file="references.bib"):
    """
    Takes a list of Scopus IDs (records[]),
    builds correct BibTeX for each,
    and writes a complete references.bib file.
    """

    pybliometrics.init()

    folder_path = constants_scopus_tool.FILEPATH_OUTPUT_SCOPUS_SEARCH
    file_name = constants_scopus_tool.FILENAME_ALL + ".csv"

    records = (
        pd.read_csv(
            f"{folder_path}/{file_name}",
            sep=";",
            encoding="utf-8",
            usecols=["identifier"],
        )["identifier"]
        .astype(str)
        .tolist()
    )
    bib_entries = []

    for scopus_id in records:
        try:
            ar = AbstractRetrieval(str(scopus_id))
        except Exception as e:
            print(f"Error retrieving {scopus_id}: {e}")
            continue

        try:
            bib = bibtex_from_scopus(ar)
            bib_entries.append(bib)
            print(f"✓ Added {scopus_id}")
        except Exception as e:
            print(f"Error generating BibTeX for {scopus_id}: {e}")

    # Sort bib entries alphabetically by identifier
    bib_entries.sort(key=lambda b: b.split("{", 1)[1].split(",", 1)[0])

    folder_path = constants_scopus_tool.FOLDER_PATH_REFERENCES
    os.makedirs(folder_path, exist_ok=True)

    file_path = os.path.join(folder_path, output_file)

    # Write to .bib file
    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(bib_entries)

    print(f"\n Written {len(bib_entries)} entries to {output_file}")


def bibtex_from_scopus(ar):
    """
    Create a BibTeX entry for Scopus documents
    """

    # Authors
    try:
        authors = " and ".join(
            f"{a.given_name} {a.surname}" for a in (ar.authors or [])
        )
    except Exception:
        authors = ""

    # Year
    year = ""
    try:
        if ar.coverDate:
            year = ar.coverDate[:4]
    except:
        pass

    # Identifier
    surname_first_author = ar.authors[0].surname
    key = f"{surname_first_author}{year}"

    # Title
    title = ar.title or ""

    # DOI
    doi = ar.doi or ""

    # Container source: journal, booktitle, conference name
    source = ""
    if hasattr(ar, "publicationName") and ar.publicationName:
        source = ar.publicationName
    elif hasattr(ar, "conference_name") and ar.conference_name:
        source = ar.conference_name
    elif hasattr(ar, "publicationTitle") and ar.publicationTitle:
        source = ar.publicationTitle

    # Pages
    pages = ar.pageRange or ""

    # Volume/Issue (may be None)
    volume = ar.volume or ""
    number = ""
    try:
        number = ar.issueIdentifier or ""
    except Exception:
        pass

    # Document type mapping
    subtype = (ar.subtypedescription or "").lower()

    if "conference" in subtype:
        entry_type = "inproceedings"
    elif "chapter" in subtype:
        entry_type = "incollection"
    elif "book" in subtype:
        entry_type = "book"
    elif "review" in subtype:
        entry_type = "article"
    elif "article" in subtype:
        entry_type = "article"
    else:
        entry_type = "misc"

    # Construct BibTeX
    bibtex = f"@{entry_type}{{{key},\n"
    if authors:
        bibtex += f"  author = {{{authors}}},\n"
    if title:
        bibtex += f"  title = {{{title}}},\n"
    if year:
        bibtex += f"  year = {{{year}}},\n"
    if source:
        if entry_type == "inproceedings":
            bibtex += f"  booktitle = {{{source}}},\n"
        elif entry_type in ("article", "review"):
            bibtex += f"  journal = {{{source}}},\n"
        else:
            bibtex += f"  howpublished = {{{source}}},\n"
    if volume:
        bibtex += f"  volume = {{{volume}}},\n"
    if number:
        bibtex += f"  number = {{{number}}},\n"
    if pages:
        bibtex += f"  pages = {{{pages}}},\n"
    if doi:
        bibtex += f"  doi = {{{doi}}},\n"

    bibtex += "}\n \n"
    return bibtex
