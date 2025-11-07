import pandas as pd
import os

papers = pd.read_csv("scopus_list", sep=';', encoding='utf-8')

print(papers)
