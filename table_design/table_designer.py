import os

import dataframe_image as dfi
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from constants import constants_scopus_tool


def prepare_df():
    """
    prepares dataframe from input files to create different charts or tables
    :return: prepared dataframe
    """
    folder_path = constants_scopus_tool.FOLDER_PATH_TABLE_DESIGN_INPUT

    # create parent folder on the fly
    os.makedirs(folder_path, exist_ok=True)

    csv_files = [f for f in os.listdir(folder_path) if f.lower().endswith(".csv")]

    if not csv_files:
        raise ValueError("No CSV files found in the specified folder.")

    dataframes = []

    for file in csv_files:
        full_path = os.path.join(folder_path, file)
        df = pd.read_csv(full_path, sep=";", encoding="utf-8")

        dataframes.append(df)

    df = pd.concat(dataframes, ignore_index=True)

    cols = [
        "number",
        "identifier",
        "channel",
        "push_notifications",
        "integrated_ai",
        "ai_chat_bot",
        "use_government_data",
        "use_low_cost_sensors",
        "interpretation_capabilities",
        "integration_of_maps",
        "downloadable_data",
        "upload_of_additional_data",
    ]

    df.drop(
        "open_access",
        axis=1,
        inplace=True,
    )

    cols = sorted(cols)
    # Convert "True"/"False" strings to actual booleans
    df[cols] = df[cols].replace(
        {
            "True": True,
            "False": False,
        }
    )

    return df


# Done
def kind_of_artifact():
    """
    creates a list of artifacts from the given dataframe containing the respective channel column
    """

    df = prepare_df()

    # Keep only relevant columns
    df = df[
        [
            "number",
            "identifier",
            "channel",
        ]
    ]

    # Count occurrences of each channel
    counts = df["channel"].value_counts().reset_index()
    counts.columns = [
        "channel",
        "count",
    ]

    # Set Seaborn style
    sns.set_theme(style="whitegrid")  # clean background with grid
    sns.set_palette("pastel")  # soft color palette

    plt.figure(
        figsize=(
            12,
            6,
        )
    )

    # Test

    # Create Seaborn barplot
    ax = sns.barplot(
        data=counts,
        x="channel",
        y="count",
        edgecolor="gray",
    )

    # Rotate x-axis labels for readability
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right")

    # Titles and labels
    plt.title(
        "Kind of Artifacts in Findings",
        fontsize=16,
        weight="bold",
    )
    plt.xlabel(
        "Providing Channels",
        fontsize=12,
    )
    plt.ylabel(
        "Number of Occurrences",
        fontsize=12,
    )

    # Optional: add value labels on top of bars
    for p in ax.patches:
        ax.annotate(
            f"{int(p.get_height())}",
            (
                p.get_x() + p.get_width() / 2.0,
                p.get_height(),
            ),
            ha="center",
            va="bottom",
            fontsize=10,
        )

    plt.tight_layout()

    folder_name = constants_scopus_tool.FOLDER_PATH_TABLE_DESIGN_OUTPUT
    file_name = constants_scopus_tool.FILE_NAME_ARTIFACT_TABLE
    file_path = os.path.join(folder_name, file_name)

    # create parent folder on the fly
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    plt.savefig(
        file_path,
        dpi=300,
        bbox_inches="tight",
    )
    # plt.show()


def matrix_generating():
    """
    create a matrix chart of the given df
    """

    df = prepare_df()

    # Requirement columns
    requirement_cols = [
        "channel",
        "push_notifications",
        "integrated_ai",
        "ai_chat_bot",
        "use_government_data",
        "use_low_cost_sensors",
        "interpretation_capabilities",
        "integration_of_maps",
        "downloadable_data",
        "upload_of_additional_data",
    ]

    # Make 'channel' the first column, sort the rest
    requirement_cols = ["channel"] + sorted(
        [c for c in requirement_cols if c != "channel"]
    )

    df["channel"] = df["channel"].notna()

    matrix = df.set_index("number")[requirement_cols]

    # Figure sizing
    num_rows = len(requirement_cols)
    fig_width = 15
    fig_height = num_rows * 1.5
    plt.figure(
        figsize=(
            fig_width,
            fig_height,
        )
    )

    # Green/red palette
    cmap = sns.color_palette(
        [
            "#ffcccc",
            "#ccffcc",
        ]
    )  # red=False, green=True

    ax = sns.heatmap(
        matrix,
        cmap=cmap,
        cbar=False,
        linewidths=0.5,
        linecolor="grey",
    )

    plt.title("Requirement Matrix per Number")
    plt.xlabel("Number")
    plt.ylabel("Requirement")

    # Y-axis labels horizontal
    ax.set_yticklabels(
        ax.get_yticklabels(),
        rotation=0,
        ha="right",
    )
    # X-axis labels rotated for readability
    ax.set_xticklabels(
        ax.get_xticklabels(),
        rotation=45,
        ha="right",
    )

    folder_name = constants_scopus_tool.FOLDER_PATH_TABLE_DESIGN_OUTPUT
    file_name = constants_scopus_tool.FILE_NAME_MATRIX
    file_path = os.path.join(folder_name, file_name)

    plt.tight_layout()
    plt.savefig(
        file_path,
        dpi=300,
        bbox_inches="tight",
    )
    # plt.show()


# produces two outputs, to align both pngs in the paper side by side, saving space
def create_conversion_table():
    """
    Creates a conversion table to identify all papers' titles with a unique number
    and splits it into 2 parts that are exported as PNG images.
    """

    # create number dataframe
    df_numbers = prepare_df()

    # load titles
    folder_path = "scraper/output"
    file_name = "list_all.csv"
    full_path = os.path.join(folder_path, file_name)
    df_titles = pd.read_csv(full_path, sep=";", encoding="utf-8")

    # merge
    df = df_numbers.merge(df_titles, on="identifier", how="left")

    # keep only relevant columns
    df = df[["number", "title"]]
    df = df.rename(columns={"number": "Index", "title": "Paper Title"})

    df = df.dropna()

    # split 50:50
    n = len(df) // 2
    df_first = df.iloc[:n].reset_index(drop=True)
    df_second = df.iloc[n:].reset_index(drop=True)

    # output folder
    folder_path = constants_scopus_tool.FOLDER_PATH_TABLE_DESIGN_OUTPUT
    os.makedirs(folder_path, exist_ok=True)

    file_path_1 = os.path.join(
        folder_path, constants_scopus_tool.FILE_NAME_CONVERSION_TABLE_1
    )
    file_path_2 = os.path.join(
        folder_path, constants_scopus_tool.FILE_NAME_CONVERSION_TABLE_2
    )

    __export_df_png(df_first, file_path_1)
    __export_df_png(df_second, file_path_2)


def __export_df_png(df, file_path):
    # --- Completely remove the index so it cannot render ---
    df = df.copy()
    df.index = [""] * len(df)  # wipe index labels
    df = df.reset_index(drop=True)

    # --- Build styles ---
    styled = df.style.hide(axis="index").set_table_styles(
        [
            {
                "selector": "th",
                "props": [
                    ("font-family", "Times New Roman"),
                    ("font-size", "12pt"),
                    ("font-weight", "bold"),
                    ("text-align", "left"),
                ],
            },
            {
                "selector": "td",
                "props": [
                    ("font-family", "Times New Roman"),
                    ("font-size", "12pt"),
                    ("text-align", "left"),
                ],
            },
        ]
    )

    # Bold row where col1 == "Paper Title"
    first_col = df.columns[0]
    if "Paper Title" in df[first_col].values:
        idx = df[df[first_col] == "Paper Title"].index
        styled = styled.set_properties(
            subset=pd.IndexSlice[idx, :], **{"font-weight": "bold"}
        )

    # --- Export WITHOUT the index ---
    dfi.export(styled.hide(axis="index"), file_path)
