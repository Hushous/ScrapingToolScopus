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

def create_reading_list(df: pd.DataFrame):
    used_papers = df[df["used"] == 1.0]
    print(df)

    file_path = "done/" + "used_papers.csv"
    used_papers.to_csv(file_path, sep=';', encoding='utf-8', index=False, header=True)

def create_separate_lists(df: pd.DataFrame):
    part1, part2, part3, part4 = np.array_split(df, 4)

    file_path = "distribute/" + "eins.csv"
    part1.to_csv(file_path, sep=';', encoding='utf-8', index=False, header=True)

    file_path = "distribute/" + "zwei.csv"
    part2.to_csv(file_path, sep=';', encoding='utf-8', index=False, header=True)

    file_path = "distribute/" + "drei.csv"
    part3.to_csv(file_path, sep=';', encoding='utf-8', index=False, header=True)

    file_path = "distribute/" + "vier.csv"
    part4.to_csv(file_path, sep=';', encoding='utf-8', index=False, header=True)

#used_count(read_csv("literature_review.csv"), "used")

#create_df_all()
#create_reading_list(read_csv("literature_review.csv"))

#create_separate_lists(read_csv("used_papers.csv"))