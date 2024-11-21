import pandas as pd

# Step 1: Load the datasets
leaderboard_data = pd.read_csv('data/processed/rogue_leaderboard_2024.csv')  # Athlete performance data
events_data = pd.read_csv('data/processed/full_event_details.csv')  # Event details

# Step 2: Reshape leaderboard data to long format
leaderboard_long = leaderboard_data.melt(
    id_vars=['Athlete', 'Division'],  # Columns to keep in the reshaped format
    var_name='Event',  # New column name for event identifiers
    value_name='Placement'  # New column name for placement data
)

# Step 3: Extract event IDs for clarity
leaderboard_long['Event_ID'] = leaderboard_long['Event'].str.extract(r'(E\d+)_')[0]

# Step 4: Convert Placement column to numeric
leaderboard_long['Placement'] = pd.to_numeric(leaderboard_long['Placement'], errors='coerce')

# Step 5: Add event details by merging with the events dataset
leaderboard_long = leaderboard_long.merge(
    events_data[['Event', 'Event Type', 'Intensity Level', 'Day']].rename(columns={'Event': 'Event_ID'}),
    on='Event_ID',
    how='left'
)

# Step 6: Clean and organize the data
# Ensure no missing placements
leaderboard_long = leaderboard_long.dropna(subset=['Placement'])

# Rearrange columns for clarity
leaderboard_long = leaderboard_long[
    ['Athlete', 'Division', 'Event_ID', 'Event Type', 'Intensity Level', 'Day', 'Placement']
]

# Step 7: Save the reshaped leaderboard for future use
leaderboard_long.to_csv('data/leaderboard_long.csv', index=False)
