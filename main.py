"""
Authors: John Paul Feliciano, Rodrigo Andaya Jr
Project: Viewpoint Ambulance Call the Car Report Generator
"""

import os
import pandas as pd
import data_transformation as dt
from scourgify import normalize_address_record
import numpy as np


def main():
    """
    main function
    """

    ts_path = "import/dispatch_trip_list_short_2024-04-04_161848_527.csv"
    ctc_file_path = (
        "import/Download(via_Manifest)_16e15fa4-b454-4c30-8a76-2945bdff6d8c.csv"
    )

    # Load the CSV files into dataframes
    ctc_df = pd.read_csv(ctc_file_path, index_col=False)
    ts_df = pd.read_csv(ts_path, index_col=False)

    # TODO: move this to data_transformation.py
    # Find the index of the first row in ts_df where "Run #" is NaN
    first_nan_index = ts_df[ts_df["Run #"].isna()].index[0]

    # Drop all rows from the first NaN row to the end
    ts_df = ts_df.iloc[:first_nan_index]

    # Extract Wait Time and Oxygen from Origin Comments
    ctc_df = dt.process_comments(ctc_df)

    # Create and populate "Patient Name" column and return the df to standardize_address()
    #   to update "Origin" column names to "PU"
    ctc_df = dt.standardize_address(dt.standardize_name(ctc_df))

    # Ensure 'PU Address' column is treated as strings
    ts_df["PU Address"] = ts_df["PU Address"].astype(str).str.strip()

    # Function to normalize an address and return only the "address_line_1"
    def normalize_address(address):
        try:
            # Normalize the address
            normalized = normalize_address_record(address)
            # Return only the "address_line_1" value
            return normalized.get("address_line_1")
        except Exception as e:
            # Handle errors in address normalization
            print(f"Error normalizing address {address}: {e}")
            return None

    # Function to normalize an address and concatenate it into a single string
    def normalize_and_concatenate_address(address):
        try:
            # Normalize the address
            normalized = normalize_address_record(address)
            # Concatenate the address components into a single string
            normalized_address = ", ".join(
                filter(
                    None,
                    [
                        normalized.get("address_line_1"),
                        normalized.get("address_line_2"),
                        normalized.get("city"),
                        normalized.get("state"),
                        normalized.get("postal_code"),
                    ],
                )
            )
            return normalized_address
        except Exception as e:
            # Handle errors in address normalization
            print(f"Error normalizing address {address}: {e}")
            return None

    # Normalize address format in the dataframes
    ts_df["PU Address"] = ts_df["PU Address"].apply(normalize_address)
    ctc_df["PU Address"] = ctc_df["PU Address"].apply(normalize_address)
    ctc_df["Drop Off Address"] = ctc_df["Drop Off Address"].apply(
        normalize_and_concatenate_address
    )
    ctc_df["Pick Up Address"] = ctc_df["Pick Up Address"].apply(
        normalize_and_concatenate_address
    )

    # Inner Join Traumasoft and Call the Car dataframes on Patient Name, Date of Service and Pickup Address
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

    # Verify column values have been updated and print the entire dataframe
    # with pd.option_context("display.max_rows", None, "display.max_columns", None):
    #     print(ctc_df)

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
