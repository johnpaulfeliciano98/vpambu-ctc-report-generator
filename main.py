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

    # Check the structure and contents of the DataFrame
    print("Original DataFrame:\n", df.head(), "\n")

    # Example how to access Origin Comments cell
    origin_comments = df["Origin Comments"].loc[df.index[0]]
    print("Extracted Origin Comment:\n", origin_comments)
    print(
        "Extracted [wait_time, oxygen]:",
        dt.extract_wait_time_and_oxygen(origin_comments),
        "\n",
    )

    # Run standardize_name and standardize_address
    df = dt.standardize_address(dt.standardize_name(df))

    # Verify column values have been updated
    print("Verify updated columns\n", df.columns.values, "\n")

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
