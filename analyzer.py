import pandas as pd
from matplotlib import pyplot as plt
import numpy as np


def read_csv(library_name):
    folder = "done/"
    df = pd.read_csv(folder + library_name, sep=";", encoding="utf-8")
    return df


def create_df_all():
    acm = read_csv("acm_used")
    ieee = read_csv("ieee_used")
    science_direct = read_csv("science_direct_used")
    scopus = read_csv("scopus_used")

    df_merged = pd.concat([acm, ieee, science_direct, scopus], ignore_index=True)
    unique_df = df_merged.drop_duplicates(subset=['title'], inplace=False)

    unique_df.to_csv("done/literature_review.csv", encoding="utf-8", sep=";", index=False, header=True)


def used_count(df: pd.DataFrame, column: str):
    counts = df[column].value_counts()

    # Plot
    plt.figure(figsize=(6, 4))
    plt.bar(counts.index.astype(str), counts.values)
    plt.xlabel(column)
    plt.ylabel("count")
    plt.title("Boolean Value Distribution")
    plt.tight_layout()
    plt.show()


used_count(read_csv("literature_review.csv"), "used")
