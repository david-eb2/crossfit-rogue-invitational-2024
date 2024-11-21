import matplotlib.pyplot as plt
import pandas as pd


# Step 1: Load and Prepare Data
def load_and_prepare_data(leaderboard_path, events_path):
    # Load datasets
    leaderboard_data = pd.read_csv(leaderboard_path)
    events_data = pd.read_csv(events_path)

    # Filter placement columns for events
    placement_columns = ['Athlete', 'Division'] + [col for col in leaderboard_data.columns if '_Placement' in col]

    # Reshape leaderboard data to long format
    leaderboard_long = leaderboard_data[placement_columns].melt(
        id_vars=['Athlete', 'Division'],
        var_name='Event',
        value_name='Placement'
    )

    # Extract Event IDs
    leaderboard_long['Event_ID'] = leaderboard_long['Event'].str.extract(r'(E\d+)')

    # Ensure Event_ID has no missing values
    leaderboard_long = leaderboard_long.dropna(subset=['Event_ID'])

    # Convert Placement to numeric
    leaderboard_long['Placement'] = pd.to_numeric(leaderboard_long['Placement'], errors='coerce')

    # Merge with event details
    leaderboard_long = leaderboard_long.merge(
        events_data[['Event', 'Event Type', 'Intensity Level', 'Day']].rename(columns={'Event': 'Event_ID'}),
        on='Event_ID',
        how='left'
    )

    # Filter valid placements
    leaderboard_long = leaderboard_long[(leaderboard_long['Placement'] >= 1) & (leaderboard_long['Placement'] <= 20)]

    return leaderboard_long, leaderboard_data, events_data


# Step 2: Compute Athlete Consistency
def compute_consistency(leaderboard_long):
    consistency = leaderboard_long.groupby('Athlete')['Placement'].std().reset_index()
    consistency.columns = ['Athlete', 'Consistency Score']
    return consistency


# Step 3: Compute Day-by-Day Trends
def compute_daywise_trends(leaderboard_long):
    daywise_trends = leaderboard_long.groupby(['Athlete', 'Day'])['Placement'].mean().reset_index()
    daywise_trends['Placement Change'] = daywise_trends.groupby('Athlete')['Placement'].diff()
    total_placement_change = daywise_trends.groupby('Athlete')['Placement Change'].sum().reset_index()
    total_placement_change.columns = ['Athlete', 'Total Placement Change']
    return total_placement_change.sort_values('Total Placement Change')


# Step 4: Specialization and Versatility Analysis
def compute_specialization_and_versatility(leaderboard_long):
    # Specialization: Average placement by event type
    specialization = leaderboard_long.groupby(['Athlete', 'Event Type'])['Placement'].mean().reset_index()
    specialization.columns = ['Athlete', 'Event Type', 'Average Placement']

    # Versatility: Standard deviation of average placement across event types
    versatility = specialization.groupby('Athlete')['Average Placement'].std().reset_index()
    versatility.columns = ['Athlete', 'Versatility Score']

    return specialization, versatility


# Step 5: Compute Clutch Performances
def compute_clutch_performance(leaderboard_long, events_data):
    high_intensity_events = events_data[events_data['Intensity Level'] == events_data['Intensity Level'].max()]['Event']
    clutch_data = leaderboard_long[leaderboard_long['Event_ID'].isin(high_intensity_events)]
    clutch_performance = clutch_data.groupby('Athlete')['Placement'].mean().reset_index()
    clutch_performance.columns = ['Athlete', 'Clutch Placement']
    return clutch_performance


# Step 6: Visualizations
# Visualize performance across events with markers and grid
def plot_performance_across_events(leaderboard_long, leaderboard_data, events_data, division, top_n=5):
    division_data = leaderboard_long[leaderboard_long['Division'] == division]

    # Determine top athletes based on the final competition rank
    top_athletes = leaderboard_data[leaderboard_data['Division'] == division].nsmallest(top_n, 'Rank')['Athlete']

    # Ensure all events are represented
    all_events = events_data[['Event', 'Day']].drop_duplicates().rename(columns={'Event': 'Event_ID'})
    all_events = all_events.sort_values(by='Event_ID')

    plt.figure(figsize=(15, 8))
    color_map = plt.cm.tab10(range(len(top_athletes)))
    athlete_colors = {athlete: color_map[idx] for idx, athlete in enumerate(top_athletes)}

    for athlete in division_data['Athlete'].unique():
        athlete_data = division_data[division_data['Athlete'] == athlete]
        linestyle = '-' if athlete in top_athletes.values else '--'
        color = athlete_colors.get(athlete, 'gray')
        alpha = 0.9 if athlete in top_athletes.values else 0.4
        label = athlete if athlete in top_athletes.values else None
        plt.plot(
            athlete_data['Event_ID'],
            athlete_data['Placement'],
            marker='o',
            linestyle=linestyle,
            color=color,
            alpha=alpha,
            label=label
        )

    # Correct x-axis with all Event_IDs and corresponding days
    event_labels = [f"{event_id} ({day})" for event_id, day in zip(all_events['Event_ID'], all_events['Day'])]
    plt.title(f"{division} Athlete Performance Across Events and Days")
    plt.xlabel("Event (Day shown below)")
    plt.ylabel("Placement (Lower is Better)")
    plt.xticks(range(len(all_events)), labels=event_labels, rotation=45)
    plt.gca().invert_yaxis()
    plt.yticks(range(1, 21))  # Ensure y-axis uses integers only
    plt.grid(axis='both', linestyle='--', linewidth=0.5)
    plt.legend(title='Top Athletes', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.show()


# Visualize specialization vs versatility by division
# Updated function: Enhanced scatter plot for specialization vs versatility
def plot_specialization_vs_versatility_by_division(specialization, versatility, division):
    merged_data = specialization.groupby('Athlete')['Average Placement'].mean().reset_index()
    merged_data = merged_data.merge(versatility, on='Athlete')
    plt.figure(figsize=(12, 8))
    colors = plt.cm.tab20(range(len(merged_data)))  # Unique colors for each athlete

    # Scatter plot with enhanced aesthetics
    for i, row in merged_data.iterrows():
        plt.scatter(
            row['Versatility Score'],
            row['Average Placement'],
            color=colors[i],
            edgecolor='black',
            s=150,  # Larger data point size for visibility
            marker='o'  # Use circle marker instead of 'x'
        )
        # Adjust text position to avoid overlap with symbols
        plt.text(
            row['Versatility Score'] + 0.02,  # Slight offset on x-axis
            row['Average Placement'] + 0.1,  # Slight offset on y-axis
            row['Athlete'],
            fontsize=8,
            alpha=0.7
        )

    plt.title(f"{division} Specialization vs. Versatility")
    plt.xlabel("Versatility Score (Lower = More Versatile)")  # Updated label
    plt.ylabel("Average Placement (Lower is Better)")
    plt.grid(axis='both', linestyle='--', linewidth=0.5)
    plt.tight_layout()
    plt.show()


# Updated function: Visualize consistency by division with unique colors and sorting
def plot_consistency_by_division(consistency, division, leaderboard_long):
    division_athletes = leaderboard_long[leaderboard_long['Division'] == division]['Athlete'].unique()
    division_consistency = consistency[consistency['Athlete'].isin(division_athletes)].sort_values('Consistency Score')
    colors = plt.cm.tab20(range(len(division_consistency)))

    plt.figure(figsize=(10, 6))
    plt.bar(division_consistency['Athlete'], division_consistency['Consistency Score'], color=colors)
    plt.title(f"{division} Athlete Consistency Across Events (Sorted by Score)")
    plt.xlabel("Athlete")
    plt.ylabel("Consistency Score (Lower is Better)")
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', linestyle='--', linewidth=0.5)
    plt.tight_layout()
    plt.show()


def plot_daywise_improvements_by_division(total_placement_change, division):
    plt.figure(figsize=(12, 8))
    colors = total_placement_change['Total Placement Change'].apply(lambda x: 'green' if x < 0 else 'red')
    plt.barh(total_placement_change['Athlete'], total_placement_change['Total Placement Change'], color=colors,
             alpha=0.8)
    plt.axvline(0, color='black', linestyle='--', linewidth=0.8)
    plt.title(f"{division} Total Placement Change Across All Events")
    plt.xlabel("Total Placement Change (Negative = Improves)")
    plt.ylabel("Athlete")
    plt.grid(linestyle='--', linewidth=0.5)
    plt.tight_layout()
    plt.show()


# Visualize clutch performance by division
def plot_clutch_performance_by_division(clutch_performance, division):
    # Filter clutch performance for the given division
    plt.figure(figsize=(10, 6))
    clutch_sorted = clutch_performance.sort_values('Clutch Placement', ascending=True)
    colors = plt.cm.tab20(range(len(clutch_sorted)))  # Use tab20 colormap for distinct colors

    # Bar chart for clutch performance
    plt.bar(clutch_sorted['Athlete'], clutch_sorted['Clutch Placement'], color=colors, alpha=0.8)
    plt.axhline(y=min(clutch_sorted['Clutch Placement']), color='black', linestyle='--', linewidth=0.8)

    plt.title(f"{division} Clutch Performance in High-Intensity Events")
    plt.xlabel("Athlete")
    plt.ylabel("Clutch Placement (Lower is Better)")
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', linestyle='--', linewidth=0.5)
    plt.tight_layout()
    plt.grid()
    plt.show()


# Step 7: Run the Analysis
def run_athlete_analysis(leaderboard_path, events_path):
    # Load and prepare data
    leaderboard_long, leaderboard_data, events_data = load_and_prepare_data(leaderboard_path, events_path)

    # Compute metrics
    consistency = compute_consistency(leaderboard_long)
    total_placement_change = compute_daywise_trends(leaderboard_long)
    specialization, versatility = compute_specialization_and_versatility(leaderboard_long)
    clutch_performance = compute_clutch_performance(leaderboard_long, events_data)

    # Visualize results by division
    for division in leaderboard_long['Division'].unique():
        # Performance trends across events and days
        plot_performance_across_events(leaderboard_long, leaderboard_data, events_data, division)

        # Consistency visualization
        plot_consistency_by_division(consistency, division, leaderboard_long)

        # Day-by-day improvements visualization
        division_data = total_placement_change[
            total_placement_change['Athlete'].isin(
                leaderboard_long[leaderboard_long['Division'] == division]['Athlete']
            )
        ]
        plot_daywise_improvements_by_division(division_data, division)

        # Specialization vs. Versatility visualization
        division_specialization = specialization[
            specialization['Athlete'].isin(
                leaderboard_long[leaderboard_long['Division'] == division]['Athlete']
            )
        ]
        division_versatility = versatility[
            versatility['Athlete'].isin(
                leaderboard_long[leaderboard_long['Division'] == division]['Athlete']
            )
        ]
        plot_specialization_vs_versatility_by_division(division_specialization, division_versatility, division)

        # Clutch performance visualization
        division_clutch = clutch_performance[
            clutch_performance['Athlete'].isin(
                leaderboard_long[leaderboard_long['Division'] == division]['Athlete']
            )
        ]
        plot_clutch_performance_by_division(division_clutch, division)


# Execute analysis
run_athlete_analysis(leaderboard_path='data/processed/rogue_leaderboard_2024.csv',
                     events_path='data/processed/full_event_details.csv')
