##
# @file generateStatsGraph.py
# @brief Module to generate some statistics graph based on file defined by config file

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os

def create_graph_stats(cfg):
    """
    Create three graphs based on statistics file in folder specified by config file. It creates :
    - invalid_word_removed_count_per_day.png
    - requests_count_per_day.png
    - solving_time_per_day.png
    If the folder doesn't exists, it will be created.

    :param dict cfg Config file as python dictionary
    :returns: None
    """

    os.makedirs(cfg['graphs_saving_folder'], exist_ok=True)

    df = pd.read_csv(cfg["stats_file"], parse_dates=["timestamp"])
    df["day"] = df["timestamp"].dt.date

    grouped = df.groupby("day").mean(numeric_only=True)

    avg_api_delay = df["api_delay"].mean()

    for column in ["invalid_word_removed_count", "solving_time", "requests_count"]:
        plt.figure(figsize=(10, 5))

        # Adding api_delay if the graph concern time
        if column == "solving_time":
            title = f"{column.replace('_', ' ').title()} per day ({avg_api_delay:.1f} sec of average API delay)"
        else:
            title = f"{column.replace('_', ' ').title()} per day"

        # Plotting
        grouped[column].plot(marker="o")


        plt.title(title)
        plt.xlabel("Day")
        if column == "solving_time":
            plt.ylabel(column.replace("_", " ").title() + " (sec)")
        else :
            plt.ylabel(column.replace("_", " ").title())
        plt.grid(True)

        # Show one date per point on the graph
        plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=1))
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.xticks(rotation=45)

        plt.tight_layout()

        # Saving
        output_path = f"{cfg['graphs_saving_folder']}/{column}_per_day.png"
        plt.savefig(output_path)
        plt.close()
