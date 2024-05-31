"""
Handle data transformation for Call the Car manifest CSV files
Manipulate the pandas dataframe object of the imported CSV file
"""


import os
import re
import pandas as pd

def extract_wait_time_and_oxygen(comment):
    """
    Returns wait time and oxygen
    Receives comment
    """
    # TODO: change function parameter to dataframe object. will need to modify tests.py
    # TODO: append wait_time and oxygen to new columns in dataframe
    # TODO: set origin comment to make lines 26 & 29 case insensitive without
    #   breaking regex pattern
    
    # Define the pattern to match
    pattern = r"Wait time:\s*(\d+)\s*minutes(?:.*?\b(\d+)\s*(?:liter|liters|LPM|L|lts|LITERS|lt|l)\b)?"

    # Remove single and double quotes from the pattern
    comment = comment.replace("'", "").replace('"', "")

    # Search for the pattern in the string
    match = re.search(pattern, comment)

    # If a match is found, extract the numbers
    if match:
        wait_time = int(match.group(1))
        oxygen_match = match.group(2)
        if oxygen_match:
            oxygen = int(oxygen_match)
        elif any(word in comment for word in ["Therapist REQ", "Deep suction", "Vent"]):
            oxygen = None
        elif (
            any(word in comment for word in ["Therapist REQ", "Deep suction", "Vent"])
            and oxygen_match is None
        ):
            oxygen = None
        else:
            oxygen = 0
    else:
        wait_time = 0
        oxygen = 0

    return [wait_time, oxygen]


def standardize_name(file_path):
    """
    Reads a CSV file, combines 'First Name' and 'Last Name' into 'Patient Name',
    and saves the updated DataFrame to an output CSV file.
    """
    # Load the CSV file into a DataFrame
    df = pd.read_csv(file_path, index_col=False)

    # Check the structure and contents of the DataFrame
    print("Original DataFrame (standardize_name):")
    print(df.head())

    # Check if "First Name" and "Last Name" columns exist in the DataFrame
    if "First Name" in df.columns and "Last Name" in df.columns:
        # Create a new "Patient Name" column combining "Last Name" and "First Name"
        df["Patient Name"] = (
            df["Last Name"].str.strip() + ", " + df["First Name"].str.strip()
        )

        # Display the first few rows of the updated DataFrame to verify the changes
        print("Updated DataFrame (standardize_name):")
        print(df.head())

        # Specify the directory where you want to save the updated CSV file
        output_folder = "output"
        os.makedirs(output_folder, exist_ok=True)  # Create the directory if it doesn't exist

        # Specify the path where you want to save the updated CSV file
        output_file_path = os.path.join(output_folder, "updated.csv")

        # Save the updated DataFrame to a new CSV file
        # df.to_csv(output_file_path, index=False)

        print(f"Updated CSV file saved to {output_file_path}")

        return df
    else:
        print("Columns 'First Name' and 'Last Name' are not found in the CSV file.")
        # run stderror
        # TODO: CHANGE TO ERROR HANDLING
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
    # Load the DataFrame from the CSV file
    # df = pd.read_csv(csv_file, index_col=False)

    # Print the original DataFrame (for debugging purposes)
    print("Original DataFrame (standardize_address):")
    print(df.head())

    # Define column mapping
    column_mapping = {
        "Origin Street": "PU Address",
        "Origin City": "PU City",
        "Origin State": "PU State",
        "Origin Postal": "PU Zip"
    }

    # Rename the columns
    df = df.rename(columns=column_mapping)

    # Print the updated DataFrame (for debugging purposes)
    print("Updated DataFrame (standardize_address):")
    print(df.head())

    # Specify the directory where you want to save the updated CSV file
    output_folder = "output"
    os.makedirs(output_folder, exist_ok=True)  # Create the directory if it doesn't exist

    # Specify the path where you want to save the updated CSV file
    output_file = os.path.join(output_folder, "updated.csv")

    # Save the updated DataFrame to the output file
    df.to_csv(output_file, index=False)

    print(f"CSV saved to {output_file}")
    return df

def process_csv_files(csv_file):
    """
    Calls the standardize_name and standardize_address functions with the provided file paths.
    """
    # TODO: Import CSV before calling standardize_name here or import CSV in main
    print("Processing name CSV file:")
    updated_df = standardize_name(csv_file)
    print("Processing address CSV file:")
    updated_df = standardize_address(updated_df)
    return updated_df

# Example usage:
# process_csv_files("import/Download(via_Manifest)_16e15fa4-b454-4c30-8a76-2945bdff6d8c.csv")



# test function for standardze_address
# standardize_address("import/Download(via_Manifest)_16e15fa4-b454-4c30-8a76-2945bdff6d8c.csv")
