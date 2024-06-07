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

    file_path = "import/Download(via_Manifest)_16e15fa4-b454-4c30-8a76-2945bdff6d8c.csv"
    # Load the CSV file into a DataFrame
    df = pd.read_csv(file_path, index_col=False)
    print("Original Dataframe")
    print(df)

    print("Extracted Origin Comments:")
    print(df["Origin Comments"])

    # Extract Wait Time and Oxygen from Origin Comments
    df = dt.process_comments(df)
    print("Extracted Wait Time and Oxygen:")
    print(df[["Trip ID", "Origin Comments", "Wait Time", "Oxygen"]])
    # Create and populate "Patient Name" column and return the df to standardize_address()
    #   to update "Origin" column names to "PU"
    df = dt.standardize_address(dt.standardize_name(df))

    # Verify column values have been updated and print the entire dataframe
    with pd.option_context("display.max_rows", None, "display.max_columns", None):
        print(df)

    # Specify the directory where you want to save the updated CSV file
    output_folder = "output"
    os.makedirs(
        output_folder, exist_ok=True
    )  # Create the directory if it doesn't exist

    # Specify the path where you want to save the updated CSV file
    output_file = os.path.join(output_folder, "updated.csv")

    # Save the updated DataFrame to the output file
    df.to_csv(output_file, index=False)

    print(f"CSV saved to {output_file}")


if __name__ == "__main__":
    main()
