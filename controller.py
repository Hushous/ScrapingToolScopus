from dotenv import load_dotenv
import os
import scopus_tool

load_dotenv()

def scopus_search_string():
    key = os.getenv('KEY', "Key does not exist")
    query_str = os.getenv('QUERYSTRING', "QueryString not existing")

    params_query_string = {'query': query_str,
             'count': 25,
             'view': 'STANDARD'}

    scopus_tool.scrape_by_search_string(key, params_query_string, "list_without_used_scopus")

def scopus_per_id(library_name: str):
    key = os.getenv('KEY', "Key does not exist")
    params_per_id = {"apiKey": key}
    input_file_name = "ids_scopus_" + library_name
    file_path = "input_files/" + input_file_name
    output_file_name = "list_without_used_" + library_name

    scopus_tool.scrape_papers_per_id(params_per_id,file_path,output_file_name)

#scopus_search_string()
scopus_per_id("science_direct")