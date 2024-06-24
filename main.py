"""
Authors: John Paul Feliciano, Rodrigo Andaya Jr
Project: Viewpoint Ambulance Call the Car Report Generator

Main script to process and merge data from two CSV files and generate a report.

This script performs the following steps:
1. Loads two CSV files containing data from Traumasoft and Call the Car.
2. Cleans Traumasoft data by removing trailing NaN rows based on the 'Run #' column.
3. Extracts wait time (in minutes) and oxygen requirement from the 'Origin Comments' column
   in the Call the Car DataFrame.
4. Standardizes address columns and creates combined address columns in the Call the Car DataFrame.
5. Normalizes address formats in both DataFrames.
6. Merges the two DataFrames on 'Patient Name', 'Date of Service', and 'PU Address'.
7. Selects specific columns of interest for the merged DataFrame.
8. Saves the merged DataFrame to a CSV file in the specified output directory.

The output CSV file contains the merged data with selected columns necessary for generating reports.

Requirements:
- pandas
- data_transformation (imported as dt)

Usage:
Ensure that the input CSV file paths are correctly specified in the script before running.
The merged CSV file will be saved in the 'output' directory.

Returns:
None
"""

import os
import pandas as pd
import data_transformation as dt


def main():
    """
    Executes data processing and report generation.

    This function orchestrates the entire data processing workflow,
    including loading, cleaning, merging, and saving data from Traumasoft
    and Call the Car CSV files to generate a consolidated report.

    Args:
        None

    Returns:
        None
    """

    ts_path = "input/dispatch_trip_list_short_2024-04-04_161848_527.csv"
    ctc_file_path = (
        "input/Download(via_Manifest)_16e15fa4-b454-4c30-8a76-2945bdff6d8c.csv"
    )

    # Load the CSV files into dataframes
    ctc_df = pd.read_csv(ctc_file_path, index_col=False)
    ts_df = pd.read_csv(ts_path, index_col=False)

    # Remove Traumasoft report summary from dataframe
    ts_df = dt.remove_trailing_nan_rows(ts_df, "Run #")

    # Extract Wait Time and Oxygen from Origin Comments
    ctc_df[["Wait Time", "Oxygen"]] = ctc_df["Origin Comments"].apply(
        lambda x: pd.Series(dt.extract_wait_time_and_oxygen(x))
    )

    # Create and populate "Patient Name" column and return the df to standardize_address()
    #   to update "Origin" column names to "PU"
    ctc_df = dt.standardize_address(dt.standardize_name(ctc_df))

    # Ensure 'PU Address' column is treated as strings
    ts_df["PU Address"] = ts_df["PU Address"].astype(str).str.strip()

    # Normalize address format in the dataframes
    ts_df["PU Address"] = ts_df["PU Address"].apply(dt.normalize_address)
    ctc_df["PU Address"] = ctc_df["PU Address"].apply(dt.normalize_address)
    ctc_df["Drop Off Address"] = ctc_df["Drop Off Address"].apply(
        dt.normalize_and_concatenate_address
    )
    ctc_df["Pick Up Address"] = ctc_df["Pick Up Address"].apply(
        dt.normalize_and_concatenate_address
    )

    # Inner Join Traumasoft and Call the Car dataframes on
    # Patient Name, Date of Service and Pickup Address
    merged_df = pd.merge(
        ts_df,
        ctc_df,
        on=["Patient Name", "Date of Service", "PU Address"],
        how="inner",
    )

    # TODO: Deal with constant values and columns without program generated content
    # Retain desired columns
    merged_df = merged_df[
        [
            # Vendor Name “Viewpoint Ambulance Inc.”
            # Vendor Tax ID “47-2166204”
            "Trip ID",  # CTC Trip ID
            "Date of Service",  # Date of Service
            "Last Name",  # Member Last Name
            "First Name",  # Member First Name
            "Pick Up Address",  # Pick Up Address “Street, City, State, Postal”
            "Drop Off Address",  # Drop Off Address
            "Pickup Time_y",  # Requested Arrival Time
            "Appointment Time",  # Appointment Time
            "At Scene",  # Actual Pickup Arrival Date
            "At Destination",  # Actual Pickup Arrival Time
            "LOS_y",  # Level of Service
            "At Destination",  # Actual Drop off Arrival Date
            "Crew",  # Driver Name
            "Driver's License",  # Driver License Number
            "VIN",  # Vehicle VIN
            "Status_x",  # Trip Status “COMPLETE”
            "Mileage",  # Miles
            "Wait Time",  # Wait Time Minutes
            "Oxygen",  # Oxygen Provided
            # Total Cost
            # Comment
        ]
    ]

    # Specify the directory where you want to save the updated CSV file
    output_folder = "output"
    os.makedirs(
        output_folder, exist_ok=True
    )  # Create the directory if it doesn't exist

    # Specify the path where you want to save the updated CSV file
    output_file = os.path.join(output_folder, "merged.csv")

    # Save the updated DataFrame to the output file
    merged_df.to_csv(output_file, index=False)

    print(f"CSV saved to {output_file}")


if __name__ == "__main__":
    main()
