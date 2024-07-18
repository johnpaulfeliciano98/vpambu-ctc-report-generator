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
    python main.py [parameters]

    Ensure that the input CSV file paths are correctly specified in the script before running.
    The merged CSV file will be saved in the 'output' directory.

Parameters:
    sys.argv[1:]: List
        Command-line arguments passed to the script.
        Each argument represents a file or input.

Example:
    $ python main.py # This will automatically take all files from the input folder
    $ python main.py file1.csv file2.csv
"""

import os
import sys

import pandas as pd
from dotenv import load_dotenv
import data_processing as dt


def main():
    """
    Entry point of the script.

    Handles command-line arguments and performs operations based on them.
    """

    load_dotenv()

    # python main.py
    if len(sys.argv) == 1:
        # Import the entire input folder
        print("Importing entire input folder")
        input_df = dt.combine_csv_files("input")
    else:
        # Import specific files
        parameters = [f"{param}" for param in sys.argv[1:]]
        print("Parameters:", parameters)
        input_df = dt.combine_csv_files(parameters)

    ctc_df = input_df[0]
    ts_df = input_df[1]

    # Data cleaning and transformation for Traumasoft DataFrame
    ts_df["Date of Service"] = ts_df["Date of Service"].apply(dt.normalize_date)
    ts_df["PU Address"] = ts_df["PU Address"].astype(str).str.strip()
    ts_df["PU Address"] = ts_df["PU Address"].apply(dt.normalize_address)

    # Data extraction, transformation, and standardization for Call the Car DataFrame
    ctc_df["Date of Service"] = ctc_df["Date of Service"].apply(dt.normalize_date)
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

    # For debugging, output the processed dataframes to separate files
    # with open("processed_ts_df.txt", "w", encoding="utf-8") as f:
    #     print("Filename:", ts_df.to_string(), file=f)
    # with open("processed_ctc_df.txt", "w", encoding="utf-8") as f:
    #     print("Filename:", ctc_df.to_string(), file=f)

    # Merge the DataFrames on 'Patient Name', 'Date of Service', and 'PU Address'
    merged_df = pd.merge(
        ts_df,
        ctc_df,
        on=["Patient Name", "Date of Service", "PU Address"],
        how="inner",
    )

    merged_df["At Scene"] = pd.to_datetime(merged_df["At Scene"])
    merged_df["At Destination"] = pd.to_datetime(merged_df["At Destination"])

    # Create "At Scene Date" and "At Scene Time" columns
    merged_df["Actual Pickup Arrival Date"] = merged_df["At Scene"].dt.date
    merged_df["Actual Pickup Arrival Time"] = merged_df["At Scene"].dt.time
    merged_df["Actual Drop off Arrival Date"] = merged_df["At Destination"].dt.date
    merged_df["Actual Drop off Arrival Time"] = merged_df["At Destination"].dt.time

    merged_df["CTC Trip ID"] = merged_df["Trip ID"]
    merged_df["Member Last Name"] = merged_df["Last Name"]
    merged_df["Member First Name"] = merged_df["First Name"]
    merged_df["Requested Arrival Time"] = merged_df["Pickup Time_y"]
    merged_df["Level of Service"] = merged_df["LOS_y"]
    merged_df["Driver Name"] = merged_df["Crew"]
    merged_df["Driver License Number"] = merged_df["Driver's License"]
    merged_df["Vehicle VIN"] = merged_df["VIN"]
    merged_df["Trip Status"] = merged_df["Status_x"]
    merged_df["Mileage"] = merged_df["Miles"]
    merged_df["Wait Time Minutes"] = merged_df["Wait Time"]
    merged_df["Oxygen Provided"] = merged_df["Oxygen"]

    # Constant values in merged dataframe
    merged_df["Vendor Name"] = os.getenv("VENDOR_NAME")
    merged_df["Vendor Tax ID"] = os.getenv("VENDOR_TAX_ID")
    merged_df["Total Cost"] = ""
    merged_df["Comment"] = ""

    # Retain specific columns in the merged DataFrame
    desired_columns = [
        "Vendor Name",
        "Vendor Tax ID",
        "CTC Trip ID",
        "Date of Service",
        "Member Last Name",
        "Member First Name",
        "Pick Up Address",
        "Drop Off Address",
        "Requested Arrival Time",
        "Appointment Time",
        "Actual Pickup Arrival Date",
        "Actual Pickup Arrival Time",
        "Actual Drop off Arrival Date",
        "Actual Drop off Arrival Time",
        "Level of Service",
        "Driver Name",
        "Driver's License",
        "Vehicle VIN",
        "Trip Status",
        "Miles",
        "Wait Time Minutes",
        "Oxygen Provided",
        "Total Cost",
        "Comment",
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
