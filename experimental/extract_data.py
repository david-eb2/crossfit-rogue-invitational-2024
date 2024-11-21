import pandas as pd
from bs4 import BeautifulSoup


def parse_leaderboard(file_path, division_name):
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

    # Build DataFrame
    df = pd.DataFrame({
        "Rank": rank_list,
        "Athlete": name_list,
        "Points": points_list,
        "Events": event_scores_list,
        "Division": division_name  # Add division column
    })

    # Expand event columns E1 through E9
    events_expanded = pd.DataFrame(df['Events'].tolist(), columns=[f"E{i + 1}" for i in range(9)])
    leaderboard_df = pd.concat([df[['Rank', 'Athlete', 'Points', 'Division']], events_expanded], axis=1)

    return leaderboard_df


# Parse both men's and women's data
women_df = parse_leaderboard("../data/html/women_division.html", "Women")
men_df = parse_leaderboard("../data/html/men_division.html", "Men")

# Merge both DataFrames
combined_df = pd.concat([women_df, men_df], ignore_index=True)

# Export to CSV
combined_df.to_csv("rogue_invitational_leaderboard_combined_2024.csv", index=False)

print("Data exported to rogue_invitational_leaderboard_combined_2024.csv")
