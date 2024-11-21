import pandas as pd


def create_event_details():
    """Creates a DataFrame with detailed event descriptions."""
    event_details = {
        "E1": {
            "Event Name": "Quick Sand",
            "Format": "10 rounds of sandbag carry + 400m run",
            "Day": "Friday",
            "Date": "November 8",
            "Time": "12:30 p.m. GMT",
            "Intensity Level": 4,
            "Event Type": "Endurance",
            "Primary Muscles": "Legs, Glutes, Core",
            "Secondary Muscles": "Shoulders, Stabilizers",
            "Movements": "Sandbag carry, 400m run",
            "Time Cap": "No Time Cap"
        },
        "E2": {
            "Event Name": "North Sea Tiger",
            "Format": "Echo Bike, ring muscle-ups, snatches, shuttle sprints",
            "Day": "Friday",
            "Date": "November 8",
            "Time": "3:45 p.m. GMT",
            "Intensity Level": 5,
            "Event Type": "Mixed (Sprint & Strength)",
            "Primary Muscles": "Shoulders, Chest, Legs",
            "Secondary Muscles": "Core, Arms",
            "Movements": "Echo Bike, Ring Muscle-Ups, Squat Snatches, Shuttle Sprints",
            "Time Cap": "8 minutes"
        },
        "E3": {
            "Event Name": "Braveheart",
            "Format": "Wall walk complex + heavy back squats",
            "Day": "Friday",
            "Date": "November 8",
            "Time": "7:15 p.m. GMT",
            "Intensity Level": 5,
            "Event Type": "Strength",
            "Primary Muscles": "Shoulders, Arms, Legs",
            "Secondary Muscles": "Core, Back",
            "Movements": "Wall Walk Complex, Heavy Back Squats",
            "Time Cap": "No Time Cap"
        },
        "E4": {
            "Event Name": "Hunting Haggis",
            "Format": "Rowing, thrusters, log muscle-ups",
            "Day": "Saturday",
            "Date": "November 9",
            "Time": "10:40 a.m. GMT",
            "Intensity Level": 4,
            "Event Type": "Endurance",
            "Primary Muscles": "Legs, Back, Core",
            "Secondary Muscles": "Shoulders, Stabilizers",
            "Movements": "Rowing, Thrusters, Log Muscle-Ups",
            "Time Cap": "No Time Cap"
        },
        "E5": {
            "Event Name": "Devil's Tail",
            "Format": "Rope climbs, Cyr bell devil presses",
            "Day": "Saturday",
            "Date": "November 9",
            "Time": "1:30 p.m. GMT",
            "Intensity Level": 3,
            "Event Type": "Strength",
            "Primary Muscles": "Arms, Shoulders, Core",
            "Secondary Muscles": "Legs",
            "Movements": "Rope Climbs, Cyr Bell Devil Presses",
            "Time Cap": "No Time Cap"
        },
        "E6": {
            "Event Name": "The Duel IV",
            "Format": "Burpees Over Hay Bale, Sled Push, Power Stairs",
            "Day": "Saturday",
            "Date": "November 9",
            "Time": "4:00 p.m. GMT",
            "Intensity Level": 3,
            "Event Type": "Strength",
            "Primary Muscles": "Legs, Shoulders, Core",
            "Secondary Muscles": "Arms, Back",
            "Movements": "Burpees Over Hay Bale, Sled Push, Power Stairs",
            "Time Cap": "No Time Cap"
        },
        "E7": {
            "Event Name": "Gondola",
            "Format": "Pegboard Traverse, SkiErg, GHD Sit-Ups",
            "Day": "Sunday",
            "Date": "November 10",
            "Time": "11:10 a.m. GMT",
            "Intensity Level": 4,
            "Event Type": "Mixed (Endurance & Skill)",
            "Primary Muscles": "Arms, Core, Legs",
            "Secondary Muscles": "Shoulders, Back",
            "Movements": "Pegboard Traverse, SkiErg, GHD Sit-Ups",
            "Time Cap": "No Time Cap"
        },
        "E8": {
            "Event Name": "Tight Rope",
            "Format": "Heavy Rope Double-Unders, Cyr Bell Lunges, Handstand Walk",
            "Day": "Sunday",
            "Date": "November 10",
            "Time": "1:25 p.m. GMT",
            "Intensity Level": 4,
            "Event Type": "Mixed (Endurance & Strength)",
            "Primary Muscles": "Shoulders, Core, Legs",
            "Secondary Muscles": "Stabilizers, Arms",
            "Movements": "Heavy Rope Double-Unders, Cyr Bell Lunges, Handstand Walk",
            "Time Cap": "No Time Cap"
        },
        "E9": {
            "Event Name": "The Excavator",
            "Format": "Progressive Sandbag Cleans",
            "Day": "Sunday",
            "Date": "November 10",
            "Time": "2:45 p.m. GMT",
            "Intensity Level": 5,
            "Event Type": "Strength",
            "Primary Muscles": "Legs, Back, Arms",
            "Secondary Muscles": "Core, Shoulders",
            "Movements": "Progressive Sandbag Cleans",
            "Time Cap": "No Time Cap"
        }
    }
    return pd.DataFrame.from_dict(event_details, orient="index").reset_index().rename(columns={"index": "Event"})


def main():
    """Main function to create and display event details."""
    # Generate detailed event descriptions
    event_details_df = create_event_details()

    # Display or return the DataFrame for further analysis
    return event_details_df


if __name__ == '__main__':
    # Execute the main function
    event_details_df = main()
