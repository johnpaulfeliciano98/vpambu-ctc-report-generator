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
    print("Original DataFrame (standardize_name):")
    print(df.head())
    print(df['Origin Comments'].loc[df.index[0]])

    # Example how to access Origin Comments cell
    # origin_comments = df['Origin Comments'].loc[df.index[0]]
    # print(dt.extract_wait_time_and_oxygen(origin_comments))

    # Run standardize_name and standardize_address
    # dt.process_csv_files("import/Download(via_Manifest)_16e15fa4-b454-4c30-8a76-2945bdff6d8c.csv")


if __name__ == "__main__":
    main()
