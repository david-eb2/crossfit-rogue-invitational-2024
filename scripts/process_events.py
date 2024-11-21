import json
import os

import pandas as pd

from scripts.utils import ensure_directory_exists


def load_event_details(input_path):
    """
    Load event details from a JSON file.

    Args:
        input_path (str): Path to the JSON file containing event details.

    Returns:
        pd.DataFrame: Event details as a DataFrame.
    """
    with open(input_path, "r") as file:
        event_details = json.load(file)
    return pd.DataFrame.from_dict(event_details, orient="index").reset_index().rename(columns={"index": "Event"})


def save_event_details(input_path, output_path):
    """
    Loads event details from a file and saves them as a CSV.

    Args:
        input_path (str): Path to the input JSON file.
        output_path (str): Path to save the processed CSV file.
    """
    # Load event details
    event_details_df = load_event_details(input_path)

    # Ensure the output directory exists
    ensure_directory_exists(os.path.dirname(output_path))

    # Save the details to a CSV file
    event_details_df.to_csv(output_path, index=False)
    print(f"Event details saved to {output_path}")


if __name__ == "__main__":
    # Define input and output file paths
    input_file = "../data/event_details.json"
    output_file = "../data/processed/full_event_details.csv"

    # Process and save event details
    save_event_details(input_file, output_file)
