import os
from tempfile import tempdir
import data_transformation as dt
import pandas as pd


def file_input():
    # import all files in "input" folder both ts and ctc
    # iterate through csv files in folder
    # Address ts_path and ctc_file_path for multiple files
    # Potential solution for ctc
    # Import csv
    # ctc files start with "Download..."
    # Create first ctc_df
    # Import second csv and append to ctc_df
    # Ignore column headers
    # Or find a way to import all files at once

    # Potential solution for ts
    # Import csv
    # ts files start with "dispatch..."
    # Create first ts_df
    # Remove trailing NaN rows from ts_df
    # Import second csv and append to ts_df
    # Ignore column headers
    # Remove trailing NaN rows from ts_df again

    folder_path = "input"
    files = os.listdir(folder_path)
    print(files)

    # return [ts_df, ctc_df]
    return None


file_input()


def combine_csv_files(directory):
    # Initialize empty DataFrames
    download_df = pd.DataFrame()
    dispatch_df = pd.DataFrame()

    # List all files in the directory
    files = os.listdir(directory)

    # Filter files for 'Download' and 'dispatch'
    download_files = [
        f for f in files if f.startswith("Download") and f.endswith(".csv")
    ]
    dispatch_files = [
        f for f in files if f.startswith("dispatch") and f.endswith(".csv")
    ]

    # Function to process and append CSV files
    def process_files(file_list, df, file_type, clean_column=None):
        for i, file in enumerate(file_list):
            file_path = os.path.join(directory, file)
            temp_df = pd.read_csv(file_path, header=0)
            initial_row_count = temp_df.shape[0]

            if file_type == "dispatch" and clean_column is not None:
                temp_df = dt.remove_trailing_nan_rows(temp_df, "Run #")

            final_row_count = temp_df.shape[0]

            if i == 0:
                df = temp_df
            else:
                df = pd.concat([df, temp_df], ignore_index=True)

            print(
                f"Processed '{file_type}' file: {file} with {initial_row_count} initial rows and {final_row_count} final rows"
            )
        return df

    # Process 'Download' files
    download_df = process_files(download_files, download_df, "Download")

    # Process 'dispatch' files
    dispatch_df = process_files(
        dispatch_files, dispatch_df, "dispatch", clean_column="Run #"
    )

    return [download_df, dispatch_df]


# Usage
directory = "input"
combined_df = combine_csv_files(directory)


# Save the combined DataFrame to a new CSV file if needed
combined_df[0].to_csv("combined_ctc.csv", index=False)
combined_df[1].to_csv("combined_ts.csv", index=False)
