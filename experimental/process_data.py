import pandas as pd


# Function to split each event column into three separate columns
def expand_event_column(df, event_col):
    # Extract columns: placement, time_score, time_score_diff using regex
    placement_col = f"{event_col}_Placement"
    time_score_col = f"{event_col}_Time/Score"
    time_score_diff_col = f"{event_col}_Time/Score_Diff"

    # Regex to extract each part of the data in each event column
    df[[placement_col, time_score_col, time_score_diff_col]] = df[event_col].str.extract(
        r"(\d+):\s*([^|]+)\s*\|\s*\(([^)]+)\)"
    )
    return df


data = pd.read_csv("../rogue_invitational_leaderboard_combined_2024.csv")

# Apply this function to each event column to expand them
event_columns = [col for col in data.columns if col.startswith("E")]
for event in event_columns:
    data = expand_event_column(data, event)

# Drop the original unprocessed event columns
data_expanded = data.drop(columns=event_columns)

# Enhancing event details with more granular components for each category
event_detailed_categories = {
    "E1": {"Event Name": "Quick Sand", "Format": "10 rounds of sandbag carry + 400m run",
           "Category": "Endurance", "Endurance Component": 1, "Strength Component": 0, "Skill Component": 0},
    "E2": {"Event Name": "North Sea Tiger", "Format": "Echo Bike, ring muscle-ups, snatches, shuttle sprints",
           "Category": "Mixed Endurance & Strength", "Endurance Component": 1, "Strength Component": 1,
           "Skill Component": 0},
    "E3": {"Event Name": "Braveheart", "Format": "Wall walk complex + heavy back squats",
           "Category": "Strength", "Endurance Component": 0, "Strength Component": 1, "Skill Component": 0},
    "E4": {"Event Name": "Hunting Haggis", "Format": "Rowing, thrusters, log muscle-ups",
           "Category": "Endurance", "Endurance Component": 1, "Strength Component": 0, "Skill Component": 0},
    "E5": {"Event Name": "Devil's Tail", "Format": "Rope climbs, Cyr bell devil presses",
           "Category": "Strength", "Endurance Component": 0, "Strength Component": 1, "Skill Component": 0},
    "E6": {"Event Name": "The Duel IV", "Format": "Burpees, sled push, power stairs",
           "Category": "Strength", "Endurance Component": 0, "Strength Component": 1, "Skill Component": 0},
    "E7": {"Event Name": "Gondola", "Format": "Pegboard, SkiErg, GHD sit-ups",
           "Category": "Mixed Endurance & Skill", "Endurance Component": 1, "Strength Component": 0,
           "Skill Component": 1},
    "E8": {"Event Name": "Tight Rope", "Format": "Double-unders, Cyr bell lunges, handstand walk",
           "Category": "Mixed Endurance, Strength, & Skill", "Endurance Component": 1, "Strength Component": 1,
           "Skill Component": 1},
    "E9": {"Event Name": "The Excavator", "Format": "Progressive sandbag cleans",
           "Category": "Strength", "Endurance Component": 0, "Strength Component": 1, "Skill Component": 0}
}

# Convert the detailed dictionary into a DataFrame
event_detailed_categories_df = pd.DataFrame.from_dict(event_detailed_categories, orient="index").reset_index().rename(
    columns={"index": "Event"})

# Display this enhanced event details DataFrame to the user
# Adding estimated muscle group involvement based on event description and typical demands
event_muscle_involvement = {
    "E1": {"Event Name": "Quick Sand", "Upper Body": 1, "Lower Body": 3, "Core/Full Body": 2},
    "E2": {"Event Name": "North Sea Tiger", "Upper Body": 2, "Lower Body": 3, "Core/Full Body": 3},
    "E3": {"Event Name": "Braveheart", "Upper Body": 2, "Lower Body": 3, "Core/Full Body": 1},
    "E4": {"Event Name": "Hunting Haggis", "Upper Body": 2, "Lower Body": 3, "Core/Full Body": 3},
    "E5": {"Event Name": "Devil's Tail", "Upper Body": 3, "Lower Body": 2, "Core/Full Body": 2},
    "E6": {"Event Name": "The Duel IV", "Upper Body": 3, "Lower Body": 3, "Core/Full Body": 2},
    "E7": {"Event Name": "Gondola", "Upper Body": 3, "Lower Body": 2, "Core/Full Body": 3},
    "E8": {"Event Name": "Tight Rope", "Upper Body": 3, "Lower Body": 3, "Core/Full Body": 2},
    "E9": {"Event Name": "The Excavator", "Upper Body": 3, "Lower Body": 3, "Core/Full Body": 2}
}

# Convert this dictionary to a DataFrame and merge with the existing detailed categories
event_muscle_involvement_df = pd.DataFrame.from_dict(event_muscle_involvement, orient="index").reset_index().rename(
    columns={"index": "Event"})

# Merging muscle involvement details with event details
event_detailed_categories_df = event_detailed_categories_df.merge(event_muscle_involvement_df,
                                                                  on=["Event", "Event Name"])
"""
These values represent relative intensity levels, with 1 for low, 2 for moderate, and 3 for high engagement.
"""
