"""
Authors: John Paul Feliciano, Rodrigo Andaya Jr
Project: Viewpoint Ambulance Call the Car Report Generator
"""

import os
import pandas as pd
import data_transformation as dt


def main():
    """
    main function
    """

    ts_path = "import/dispatch_trip_list_short_2024-05-08_161848_527.csv"
    ctc_file_path = (
        "import/Download(via_Manifest)_16e15fa4-b454-4c30-8a76-2945bdff6d8c.csv"
    )

    # create ts and ctc data frames
    ts_df = pd.read_csv(ts_path, index_col=False)

    # Load the CSV file into a DataFrame
    ctc_df = pd.read_csv(ctc_file_path, index_col=False)
    # print("Original Dataframe")
    # print(ctc_df)

    # print(type(ts_df['Patient Name']))
    # print(type(ts_df['Date of Service']))
    # print(type(ts_df['PU Address']))
    # print(type(ts_df['PU City']))
    # print(type(ts_df['PU State']))

    # print("Extracted Origin Comments:")
    # print(ctc_df["Origin Comments"])

    # Extract Wait Time and Oxygen from Origin Comments
    ctc_df = dt.process_comments(ctc_df)
    # print("Extracted Wait Time and Oxygen:")
    # print(ctc_df[["Trip ID", "Origin Comments", "Wait Time", "Oxygen"]])
    # Create and populate "Patient Name" column and return the df to standardize_address()
    #   to update "Origin" column names to "PU"
    ctc_df = dt.standardize_address(dt.standardize_name(ctc_df))

    # print(type(ctc_df['Patient Name']))
    # print(type(ctc_df['Date of Service']))
    # print(type(ctc_df['PU Address']))
    # print(type(ctc_df['PU City']))
    # print(type(ctc_df['PU State']))

    # # inner join on name, dos, address
    merged_df = pd.merge(
        ts_df, ctc_df, on=["Patient Name", "Date of Service", "PU Address"], how="right"
    )

    print(merged_df)

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
