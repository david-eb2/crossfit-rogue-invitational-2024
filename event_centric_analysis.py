# Import necessary libraries
import re

import matplotlib.pyplot as plt
import pandas as pd

# Define constants
PASTEL_COLOR_PALETTE = ['#AEC6CF', '#FFB347', '#B39EB5', '#FF6961', '#77DD77', '#F49AC2', '#CFCFC4', '#FDFD96',
                        '#84B6F4', '#FDDB6D']
MARKER_SHAPES = ['o', 's', 'D', '^', 'p']  # Circle, square, diamond, triangle up, pentagon


# Function to load data
def load_data(event_details_path):
    """Load the event details CSV file."""
    return pd.read_csv(event_details_path)


# Function to preprocess event data
def preprocess_events(event_details):
    """Clean and preprocess the event data."""
    # Format date and time
    event_details['Formatted Date'] = event_details['Date'] + ' 2024'
    event_details['Formatted Time'] = (
        event_details['Time']
        .str.replace(' GMT', '')
        .str.replace('a.m.', 'AM')
        .str.replace('p.m.', 'PM')
    )
    event_details['Datetime'] = pd.to_datetime(
        event_details['Formatted Date'] + ' ' + event_details['Formatted Time'],
        format='%B %d %Y %I:%M %p'
    )
    event_details['Day'] = pd.to_datetime(event_details['Datetime']).dt.day_name()
    event_details['Movement Complexity'] = event_details['Movements'].str.split(', ').apply(len)

    # Extract numeric time caps
    event_details['Time Cap Minutes'] = event_details['Time Cap'].apply(
        lambda x: int(re.search(r'(\d+)\s*minutes', x).group(1)) if pd.notnull(x) and re.search(r'(\d+)\s*minutes',
                                                                                                x) else None
    )

    # Calculate fatigue index
    event_details['Fatigue Index'] = event_details['Time Cap Minutes'] * event_details['Movement Complexity']
    return event_details.sort_values('Datetime')


# Function to map colors to event types
def generate_color_mapping(event_details, color_palette=PASTEL_COLOR_PALETTE):
    """Generate a mapping of event types to colors."""
    unique_event_types = event_details['Event Type'].unique()
    return {event_type: color_palette[i % len(color_palette)] for i, event_type in enumerate(unique_event_types)}


# Function to map markers to event types
def generate_marker_mapping(event_details, marker_shapes=MARKER_SHAPES):
    """Generate a mapping of event types to marker shapes."""
    unique_event_types = event_details['Event Type'].unique()
    return {event_type: marker_shapes[i % len(marker_shapes)] for i, event_type in enumerate(unique_event_types)}


# Function to plot event type distribution per day as a bar chart
def plot_event_type_distribution(event_details, color_mapping):
    """Plot the distribution of event types per day."""
    event_counts = event_details.groupby(['Day', 'Event Type']).size().unstack(fill_value=0)
    event_counts.plot(kind='bar', figsize=(14, 8), color=[color_mapping[event] for event in event_counts.columns],
                      alpha=0.9, width=0.8)
    plt.title('Event Type Distribution Per Day', fontsize=16)
    plt.xlabel('Day', fontsize=12)
    plt.ylabel('Number of Events', fontsize=12)
    plt.xticks(rotation=0, fontsize=10)
    plt.legend(title='Event Type', fontsize=10)
    plt.grid(axis='y', alpha=0.4)
    plt.tight_layout()
    plt.show()


# Function to plot a timeline of events with markers
def plot_event_timeline(event_details, color_mapping, marker_mapping):
    """Plot a timeline of events with custom markers."""
    plt.figure(figsize=(14, 8))
    for _, row in event_details.iterrows():
        plt.scatter(
            row['Day'],
            row['Event Name'],
            color=color_mapping[row['Event Type']],
            marker=marker_mapping[row['Event Type']],
            s=200,
            label=row['Event Type'] if row['Event Type'] not in plt.gca().get_legend_handles_labels()[1] else ""
        )
    plt.title('Event Type Distribution Timeline', fontsize=16)
    plt.xlabel('Day', fontsize=12)
    plt.ylabel('Event Name', fontsize=12)
    plt.xticks(rotation=0, fontsize=10)
    plt.legend(title='Event Type', fontsize=12, loc='upper left')
    plt.grid(axis='x', alpha=0.3)
    plt.tight_layout()
    plt.show()


# Function to plot fatigue index by event
def plot_fatigue_index(event_details):
    """Plot the fatigue index for each event."""
    plt.figure(figsize=(14, 8))
    plt.barh(event_details['Event Name'], event_details['Fatigue Index'], color='#76B041')
    plt.title('Estimated Fatigue Impact by Event', fontsize=16)
    plt.xlabel('Fatigue Index', fontsize=12)
    plt.ylabel('Event Name', fontsize=12)
    plt.grid(axis='x', alpha=0.5)
    plt.tight_layout()
    plt.show()


# Main function
def main(event_details_path):
    """Main function to run the analysis and visualizations."""
    # Load and preprocess data
    event_details = load_data(event_details_path)
    event_details = preprocess_events(event_details)

    # Generate mappings
    color_mapping = generate_color_mapping(event_details)
    marker_mapping = generate_marker_mapping(event_details)

    # Plot visualizations
    plot_event_type_distribution(event_details, color_mapping)
    plot_event_timeline(event_details, color_mapping, marker_mapping)
    plot_fatigue_index(event_details)


# Entry point
if __name__ == '__main__':
    # Replace with the path to your CSV file
    event_details_path = 'data/processed/full_event_details.csv'
    main(event_details_path)
