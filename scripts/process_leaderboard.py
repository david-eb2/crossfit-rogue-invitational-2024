import pandas as pd
from bs4 import BeautifulSoup

from utils import ensure_directory_exists


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


def expand_event_columns(df):
    """
    Expands event columns into Placement, Time/Score, and Time/Score Difference columns.

    Args:
        df (pd.DataFrame): Leaderboard DataFrame.

    Returns:
        pd.DataFrame: Expanded DataFrame with separate event columns.
    """
    event_columns = [col for col in df.columns if col.startswith("E")]
    for event_col in event_columns:
        # Expand each event column into three separate columns
        placement_col = f"{event_col}_Placement"
        time_score_col = f"{event_col}_Time/Score"
        time_score_diff_col = f"{event_col}_Time/Score_Diff"

        df[[placement_col, time_score_col, time_score_diff_col]] = df[event_col].str.extract(
            r"(\d+):\s*([^|]+)\s*\|\s*\(([^)]+)\)"
        )

    # Drop the original event columns
    return df.drop(columns=event_columns)


def process_all_divisions(html_paths, division_names, output_path):
    """
    Process leaderboard data for all divisions, expand event columns, and save the result.

    Args:
        html_paths (list): List of file paths to the HTML files.
        division_names (list): Corresponding division names.
        output_path (str): Path to save the processed leaderboard CSV.
    """
    combined_df = pd.DataFrame()

    # Process each division
    for file_path, division_name in zip(html_paths, division_names):
        print(f"Processing division: {division_name} from {file_path}")
        division_df = parse_leaderboard(file_path, division_name)
        combined_df = pd.concat([combined_df, division_df], ignore_index=True)

    # Expand event columns for the combined data
    combined_df = expand_event_columns(combined_df)

    # Ensure the output directory exists
    ensure_directory_exists(output_path)

    # Save combined and expanded leaderboard to CSV
    combined_df.to_csv(output_path, index=False)
    print(f"Combined leaderboard saved to {output_path}")


if __name__ == "__main__":
    # Define HTML paths and divisions
    html_paths = ["../data/html/women_division.html", "../data/html/men_division.html"]
    division_names = ["Women", "Men"]
    output_file = "../data/processed/rogue_leaderboard_2024.csv"

    # Process all divisions and save results
    process_all_divisions(html_paths, division_names, output_file)
