import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import dataframe_image as dfi

def read_csv(document_name):
    folder = "analyzing/"
    library_name = "jan_matrix.csv"
    df = pd.read_csv(folder + document_name, sep=";", encoding="utf-8")
    return df


def prepare_df():
    #df1 = read_csv("ali_matrix.csv")
    df2 = read_csv("jan_matrix.csv")
    df3 = read_csv("pascal_matrix.csv")
    df4 = read_csv("volkan_matrix.csv")

    df = pd.concat([df2, df3, df4])

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
        "upload_of_additional_data"
    ]

    df.drop("open_access", axis=1, inplace=True)

    cols = sorted(cols)
    # Convert "True"/"False" strings to actual booleans
    df[cols] = df[cols].replace({"True": True, "False": False})

    return df

# Done
def kind_of_artifact(df: pd.DataFrame):
    # Keep only relevant columns
    df = df[["number", "identifier", "channel"]]

    # Count occurrences of each channel
    counts = df["channel"].value_counts().reset_index()
    counts.columns = ["channel", "count"]

    # Set Seaborn style
    sns.set(style="whitegrid")  # clean background with grid
    sns.set_palette("pastel")  # soft color palette

    plt.figure(figsize=(12, 6))

    # Create Seaborn barplot
    ax = sns.barplot(
        data=counts,
        x="channel",
        y="count",
        edgecolor="gray"
    )

    # Rotate x-axis labels for readability
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')

    # Titles and labels
    plt.title("Kind of Artifacts in Findings", fontsize=16, weight='bold')
    plt.xlabel("Providing Channels", fontsize=12)
    plt.ylabel("Number of Occurrences", fontsize=12)

    # Optional: add value labels on top of bars
    for p in ax.patches:
        ax.annotate(
            f'{int(p.get_height())}',
            (p.get_x() + p.get_width() / 2., p.get_height()),
            ha='center',
            va='bottom',
            fontsize=10
        )

    plt.tight_layout()
    plt.savefig("analyzing/plots/finds_of_artifacts.png", dpi=300, bbox_inches="tight")
    plt.show()


def matrix_generating(df: pd.DataFrame):
    # Requirement columns
    requirement_cols = [
        "channel",
        "push_notifications", "integrated_ai", "ai_chat_bot",
        "use_government_data", "use_low_cost_sensors",
        "interpretation_capabilities", "integration_of_maps",
        "downloadable_data", "upload_of_additional_data"
    ]

    # Make 'channel' the first column, sort the rest
    requirement_cols = ["channel"] + sorted([c for c in requirement_cols if c != "channel"])

    df["channel"] = df["channel"].notna()

    matrix = df.set_index("number")[requirement_cols]

    # Figure sizing
    num_rows = len(requirement_cols)
    fig_width = 15
    fig_height = num_rows * 1.5
    plt.figure(figsize=(fig_width, fig_height))

    # Green/red palette
    cmap = sns.color_palette(["#ffcccc", "#ccffcc"])  # red=False, green=True

    ax = sns.heatmap(
        matrix,
        cmap=cmap,
        cbar=False,
        linewidths=0.5,
        linecolor="grey"
    )

    plt.title("Requirement Matrix per Number")
    plt.xlabel("Number")
    plt.ylabel("Requirement")

    # Y-axis labels horizontal
    ax.set_yticklabels(ax.get_yticklabels(), rotation=0, ha='right')
    # X-axis labels rotated for readability
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')

    plt.tight_layout()
    plt.savefig("analyzing/plots/heatmap.png", dpi=300, bbox_inches="tight")
    plt.show()


def create_conversion_table():
#   df1 = read_csv("ali.csv")
    df2 = read_csv("jan.csv")
    df3 = read_csv("pascal.csv")
    df4 = read_csv("volkan.csv")

    new_df = pd.concat([df2, df3, df4])

    df = new_df[["number","title"]]
    df = df.rename(columns={"number": "Index", "title": "Paper Title"})

    # Ensure unique index
    df = df.reset_index(drop=True)

    # Styling
    styled_df = (
        df.style
        .hide(axis="index")  # hide the index column
        .set_table_styles([
            # Header style
            {"selector": "thead th.col0", "props": [("text-align", "center")]},  # number header
            {"selector": "thead th.col1", "props": [("text-align", "left")]},  # title header
            {"selector": "thead", "props": [("background-color", "#40466e"),
                                            ("color", "white"),
                                            ("font-weight", "bold")]},
            # Body style
            {"selector": "tbody td.col0", "props": [("text-align", "center")]},  # number cells
            {"selector": "tbody td.col1", "props": [("text-align", "left")]},  # title cells
            {"selector": "tr:nth-child(even)", "props": [("background-color", "#f2f2f2")]}
        ])
        .set_properties(**{
            "font-size": "12pt",
            "font-family": "Times New Roman"
        })
    )

    # Export as PNG
    dfi.export(styled_df, "analyzing/plots/table_output.png")


def seperate_csvs():
    df = read_csv("volkan_matrix.csv")

    df = df[["number","identifier","channel","push_notifications","integrated_ai","ai_chat_bot","use_government_data","use_low_cost_sensors","interpretation_capabilities","integration_of_maps","downloadable_data","upload_of_additional_data"]]
    print(df)

    df.to_csv("analyzing/volkan_matrix.csv", sep=';', encoding='utf-8', index=False, header=True)



create_conversion_table()
kind_of_artifact(prepare_df())
matrix_generating(prepare_df())

