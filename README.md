# Clone the repo

git clone https://github.com/Hushous/ScrapingToolScopus

# Move into the folder

cd ScrapingToolScopus

# Install dependencies

pip install -r requirements.txt

# Request API Key for Elsevier

visit https://dev.elsevier.com/ -> I want an API Key

# Create .env in root

with QUERY_STRING = <your-query-string> keep in mind to put string in extra '' to ensure correctness
and KEY = <your-api-key>

# Execute controller.py

1. When using Flag "True" for Scraping ALL found documents get processed
2. Using the Table Designer will need at least one handcrafted .csv document over requirements

# Constants_scopus_tool.py

When necessary change constants in /constants/constants_scopus_tool.py

# Additional Information

In order to use the scraper, additional input data can be fed in either "scraper/input" or "table_design/input" in the
form of .csv data
