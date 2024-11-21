import os

import pandas as pd
from bs4 import BeautifulSoup


def ensure_directory_exists(file_path):
    """
    Ensures that the directory for a given file path exists. Creates it if not.

    Args:
        file_path (str): Path to the file whose directory should be ensured.
    """
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Created directory: {directory}")


def parse_leaderboard(file_path, division_name):
    """
    Parse the leaderboard data from an HTML file.

    Args:
        file_path (str): Path to the HTML file.
        division_name (str): Name of the division (e.g., "Men", "Women").

    Returns:
        pd.DataFrame: Processed leaderboard data for the division.
    """
    # Load HTML content from file
    with open(file_path, "r", encoding="utf-8") as file:
        html = file.read()

    # Parse HTML with BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    # Initialize lists to store data
    rank_list = []
    name_list = []
    points_list = []
    event_scores_list = []

    # Extract each athlete's leaderboard row
    for athlete_row in soup.select(".embedded-leaderboard-item--body"):
        try:
            # Extract overall rank
            rank = athlete_row.select_one(".embedded-leaderboard-item__rank--overall").text.strip()
            rank_list.append(rank)

            # Extract name and points
            name = athlete_row.select_one(".embedded-leaderboard-item__name").text.strip()
            points = athlete_row.select_one(".embedded-leaderboard-item__score--overall").text.strip()
            name_list.append(name)
            points_list.append(points)

            # Extract event scores (E1 through E9)
            event_scores = []
            for event in athlete_row.select(".embedded-leaderboard-item__cell--workout"):
                # Extract rank and score for each event
                event_rank = event.select_one(".embedded-leaderboard-item__rank--workout").text.strip()
                event_score = " | ".join(
                    span.text.strip() for span in event.select(".embedded-leaderboard-item__score--workout span"))
                event_scores.append(f"{event_rank}: {event_score}")

            event_scores_list.append(event_scores)
        except AttributeError as e:
            print(f"Error parsing athlete row: {e}")
            continue

    # Build DataFrame
    df = pd.DataFrame({
        "Rank": rank_list,
        "Athlete": name_list,
        "Points": points_list,
        "Events": event_scores_list,
        "Division": division_name  # Add division column
    })

    # Expand event columns (E1 through E9)
    event_columns = pd.DataFrame(df['Events'].tolist(), columns=[f"E{i + 1}" for i in range(9)])
    leaderboard_df = pd.concat([df[['Rank', 'Athlete', 'Points', 'Division']], event_columns], axis=1)

    return leaderboard_df
