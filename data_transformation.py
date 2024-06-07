"""
Handle data transformation for Call the Car manifest CSV files
Manipulate the pandas dataframe object of the imported CSV file
"""

import re
import pandas as pd


# TODO: change function parameter to dataframe object. will need to modify tests.py


def extract_wait_time_and_oxygen(comment):
    """
    Returns wait time and oxygen from a single comment string.
    """
    # Define the patterns to match wait time and oxygen separately
    wait_time_pattern = r"Wait time:\s*(\d+)\s*minutes"
    oxygen_pattern = r"(\d+)\s*(?:liter|liters|LPM|L|lts|LITERS|lt|l)\b"

    # Search for wait time in the comment
    wait_time_match = re.search(wait_time_pattern, comment, re.IGNORECASE)
    wait_time = int(wait_time_match.group(1)) if wait_time_match else 0

    # Search for oxygen in the comment
    oxygen_match = re.search(oxygen_pattern, comment, re.IGNORECASE)
    oxygen = int(oxygen_match.group(1)) if oxygen_match else 0

    # Additional check for phrases that imply oxygen is required but not explicitly mentioned
    if (
        "Therapist REQ" in comment
        or "Deep suction" in comment
        or "Vent" in comment
        or "tracheostomy" in comment
    ):
        oxygen = oxygen if oxygen else None

    return wait_time, oxygen


def process_comments(df):
    """
    Apply the extract_wait_time_and_oxygen function to each row in the column "Origin Comments"
    """
    df[["Wait Time", "Oxygen"]] = df["Origin Comments"].apply(
        lambda x: pd.Series(extract_wait_time_and_oxygen(x))
    )
    return df


# TODO: modify to implement error handling
def standardize_name(df):
    """
    Reads a CSV file, combines 'First Name' and 'Last Name' into 'Patient Name',
    and saves the updated DataFrame to an output CSV file.
    """

    # Check if "First Name" and "Last Name" columns exist in the DataFrame
    if "First Name" in df.columns and "Last Name" in df.columns:
        # Create a new "Patient Name" column combining "Last Name" and "First Name"
        df["Patient Name"] = (
            df["Last Name"].str.strip() + ", " + df["First Name"].str.strip()
        )

        # Display the first few rows of the updated DataFrame to verify the changes
        print("Updated DataFrame (standardize_name):\n", df, "\n")

        return df
    else:
        print("Columns 'First Name' and 'Last Name' are not found in the CSV file.")
        return None


def standardize_address(df):
    """
    Renames columns in the CSV:
        "Origin Street" to "PU Address"
        "Origin City" to "PU City"
        "Origin State" to "PU State"
        "Origin Postal" to "PU Zip"
    Receives a CSV file path, reads it into a DataFrame, renames the columns,
    and saves the updated DataFrame to an output CSV file.
    """

    # Define column mapping
    column_mapping = {
        "Origin Street": "PU Address",
        "Origin City": "PU City",
        "Origin State": "PU State",
        "Origin Postal": "PU Zip",
    }

    # Rename the columns
    df = df.rename(columns=column_mapping)

    # Print the updated DataFrame (for debugging purposes)
    print("Updated DataFrame (standardize_address):\n", df, "\n")

    return df
