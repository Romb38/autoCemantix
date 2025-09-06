import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def create_graph_stats(cfg):

    df = pd.read_csv(cfg["stats_file"], parse_dates=["timestamp"])
    df["day"] = df["timestamp"].dt.date

    grouped = df.groupby("day").mean(numeric_only=True)

    # Calcul de la moyenne globale de api_delay (sur tout le fichier)
    avg_api_delay = df["api_delay"].mean()

    for column in ["invalid_word_removed_count", "solving_time", "requests_count"]:
        plt.figure(figsize=(10, 5))

        # Titre personnalisé avec valeur dynamique pour solving_time
        if column == "solving_time":
            title = f"{column.replace('_', ' ').title()} per day ({avg_api_delay:.1f} sec of API delay)"
        else:
            title = f"{column.replace('_', ' ').title()} per day"

        # Tracer
        grouped[column].plot(marker="o")

        # Axes
        plt.title(title)
        plt.xlabel("Day")
        plt.ylabel(column.replace("_", " ").title())
        plt.grid(True)

        # Affichage propre des dates (1 tick / jour)
        plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=1))
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.xticks(rotation=45)

        plt.tight_layout()

        # Sauvegarde
        output_path = f"{cfg['graphs_saving_folder']}/{column}_per_day.png"
        plt.savefig(output_path)
        plt.close()
