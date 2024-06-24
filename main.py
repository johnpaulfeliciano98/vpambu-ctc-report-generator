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

    # Paths to the input CSV files
    ts_path = "input/dispatch_trip_list_short_2024-04-04_161848_527.csv"
    ctc_file_path = (
        "input/Download(via_Manifest)_16e15fa4-b454-4c30-8a76-2945bdff6d8c.csv"
    )

    # Load the CSV files into DataFrames
    ctc_df = pd.read_csv(ctc_file_path, index_col=False)
    ts_df = pd.read_csv(ts_path, index_col=False)

    # Data cleaning and transformation for Traumasoft DataFrame
    ts_df = dt.remove_trailing_nan_rows(ts_df, "Run #")
    ts_df["PU Address"] = ts_df["PU Address"].astype(str).str.strip()
    ts_df["PU Address"] = ts_df["PU Address"].apply(dt.normalize_address)

    # Data extraction, transformation, and standardization for Call the Car DataFrame
    ctc_df[["Wait Time", "Oxygen"]] = ctc_df["Origin Comments"].apply(
        lambda x: pd.Series(dt.extract_wait_time_and_oxygen(x))
    )
    ctc_df = dt.standardize_address(dt.standardize_name(ctc_df))
    ctc_df["PU Address"] = ctc_df["PU Address"].apply(dt.normalize_address)
    ctc_df["Pick Up Address"] = ctc_df["Pick Up Address"].apply(
        dt.normalize_and_concatenate_address
    )
    ctc_df["Drop Off Address"] = ctc_df["Drop Off Address"].apply(
        dt.normalize_and_concatenate_address
    )

    # Merge the DataFrames on 'Patient Name', 'Date of Service', and 'PU Address'
    merged_df = pd.merge(
        ts_df,
        ctc_df,
        on=["Patient Name", "Date of Service", "PU Address"],
        how="inner",
    )

    # TODO: Deal with constant values and columns without program generated content
    # Retain specific columns in the merged DataFrame
    desired_columns = [
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
    merged_df = merged_df[desired_columns]

    # Save the merged DataFrame to the output file
    output_folder = "output"
    os.makedirs(output_folder, exist_ok=True)
    output_file = os.path.join(output_folder, "merged.csv")
    merged_df.to_csv(output_file, index=False)

    print(f"CSV saved to {output_file}")


if __name__ == "__main__":
    main()
