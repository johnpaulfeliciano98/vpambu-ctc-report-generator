"""
Utilities for manipulating dataframes and normalizing addresses.

Functions:
- remove_trailing_nan_rows(df, column_name):
    Removes rows from a dataframe starting from the first row where the specified
    column has NaN values.

- extract_wait_time_and_oxygen(comment):
    Extracts wait time in minutes and oxygen volume in liters from a comment string.

- standardize_name(df):
    Combines 'First Name' and 'Last Name' into 'Patient Name' in the DataFrame.

- standardize_address(df):
    Standardizes address columns and creates new combined address columns in the DataFrame.

- normalize_address(address):
    Normalizes an address and returns the first line of the normalized address.

- normalize_and_concatenate_address(address):
    Normalizes an address and concatenates its components into a single string.
"""

import os
import re

import pandas as pd
from scourgify import normalize_address_record


def combine_csv_files(input_files):
    """
    Combine CSV files from a specified directory or a list of files into two DataFrames.

    This function processes CSV files starting with "Download" and "dispatch" in their filenames.
    It reads and combines these files into two separate DataFrames: one for "Download" files
    and one for "dispatch" files. For "dispatch" files, trailing rows with NaN values in a
    specified column are removed.

    Parameters:
    -----------
    input_files : str or list
        If a string, it represents the directory containing the CSV files to process.
        If a list, it represents the specific filenames to process.

    Returns:
    --------
    list of pandas.DataFrame
        A list containing two DataFrames:
        - The first DataFrame contains combined data from "Download" files.
        - The second DataFrame contains combined data from "dispatch" files after removing
          trailing NaN rows based on the "Run #" column.

    Raises:
    -------
    ValueError
        If `input_files` is neither a string nor a list.

    Example:
    --------
    >>> combined_dfs = combine_csv_files("path/to/directory")
    >>> download_df, dispatch_df = combined_dfs[0], combined_dfs[1]

    >>> specific_files = ["Download1.csv", "dispatch1.csv"]
    >>> combined_dfs = combine_csv_files(specific_files)
    >>> download_df, dispatch_df = combined_dfs[0], combined_dfs[1]
    """

    # Initialize empty DataFrames
    download_df = pd.DataFrame()
    dispatch_df = pd.DataFrame()

    # Check if input_files is a string (input_files name) or a list (specific files)
    if isinstance(input_files, str):
        print(f"combine_csv_files: str {input_files} detected")
        # List all files in the input_files
        files = os.listdir(input_files)
        base_directory = input_files  # Store base input_files for file_path calculation
    elif isinstance(input_files, list):
        print(f"combine_csv_files: list {input_files} detected")
        # Use specified files from the list
        files = input_files
        base_directory = "input"
    else:
        raise ValueError(
            "Parameter 'input_files' must be a string or a list of filenames."
        )

    # Filter files for 'Download' and 'dispatch'
    download_files = [
        f for f in files if f.startswith("Download") and f.endswith(".csv")
    ]
    dispatch_files = [
        f for f in files if f.startswith("dispatch") and f.endswith(".csv")
    ]

    print(f"download_files:\n{download_files}")
    print(f"dispatch_files:\n{dispatch_files}")

    # Function to process and append CSV files
    def process_files(file_list, df, file_type, clean_column=None):
        for i, file in enumerate(file_list):
            file_path = os.path.join(base_directory, file)

            temp_df = pd.read_csv(file_path, header=0, index_col=False)
            initial_row_count = temp_df.shape[0]

            if file_type == "dispatch" and clean_column is not None:
                temp_df = remove_trailing_nan_rows(temp_df, clean_column)
                # print(temp_df[clean_column].to_string())

            final_row_count = temp_df.shape[0]

            if i == 0:
                df = temp_df.copy()  # Initialize df with temp_df content
            else:
                df = pd.concat([df, temp_df], ignore_index=True)

            print(
                f"Processed '{file_type}' file: {file} with {initial_row_count} initial rows and {final_row_count} final rows"
            )
        return df  # Return the updated dataframe after concatenation

    # Process 'Download' files
    download_df = process_files(download_files, download_df, "Download")

    # Process 'dispatch' files
    dispatch_df = process_files(
        dispatch_files, dispatch_df, "dispatch", clean_column="Run #"
    )

    return [download_df, dispatch_df]


def remove_trailing_nan_rows(df, column_name):
    """
    Removes all rows starting from the first row where the specified column has NaN values.

    Args:
        df (pd.DataFrame): The DataFrame to be cleaned.
        column_name (str): The name of the column to check for NaN values.

    Returns:
        pd.DataFrame: The cleaned DataFrame without trailing rows that contain
        NaN in the specified column.
    """
    # first_nan_index = df[df[column_name].isna()].index[0]
    # cleaned_df = df.iloc[:first_nan_index]

    # Remove rows where the specified column has NaN values
    df_cleaned = df.dropna(subset=[column_name])

    # Remove rows where the specified column contains non-numeric data (assuming "Run #" should be numeric)
    df_cleaned = df_cleaned[df_cleaned[column_name].str.match(r"\d+(-\d+)?$", na=False)]

    # Find the last valid index in the specified column
    last_valid_index = df_cleaned[column_name].last_valid_index()

    # Keep only the rows up to the last valid index
    df_cleaned = df_cleaned.loc[:last_valid_index]

    return df_cleaned


def extract_wait_time_and_oxygen(comment):
    """
    Extracts wait time and oxygen requirement from a comment string.

    This function searches for wait time in minutes and oxygen volume in liters
    from a given comment string. If specific keywords indicating oxygen
    requirement are found but no explicit oxygen volume is mentioned, the
    oxygen value is set to None.

    Args:
        comment (str): The comment string to extract information from.

    Returns:
        tuple: A tuple containing:
            - wait_time (int): The extracted wait time in minutes. If not found, returns 0.
            - oxygen (int or None): The extracted oxygen volume in liters. If not found and
              specific keywords are present, returns None. Otherwise, returns 0.
    """
    # Define patterns to match wait time and oxygen
    wait_time_pattern = r"Wait time:\s*(\d+)\s*minutes"
    oxygen_pattern = r"(\d+)\s*(?:liter|liters|LPM|L|lts|LITERS|lt|l)\b"

    wait_time_match = re.search(wait_time_pattern, comment, re.IGNORECASE)
    wait_time = int(wait_time_match.group(1)) if wait_time_match else 0

    oxygen_match = re.search(oxygen_pattern, comment, re.IGNORECASE)
    oxygen = int(oxygen_match.group(1)) if oxygen_match else 0

    # Check for phrases implying oxygen requirement
    if any(
        keyword in comment
        for keyword in ["Therapist REQ", "Deep suction", "Vent", "tracheostomy"]
    ):
        oxygen = oxygen if oxygen else None

    return wait_time, oxygen


def standardize_name(df):
    """
    Combines 'First Name' and 'Last Name' into 'Patient Name' in the DataFrame.

    This function checks for the presence of 'First Name' and 'Last Name' columns
    in the provided DataFrame. If both columns exist, it creates a new column
    'Patient Name' by combining the 'Last Name' and 'First Name' columns, separated
    by a comma.

    Args:
        df (pd.DataFrame): The DataFrame containing 'First Name' and 'Last Name' columns.

    Returns:
        pd.DataFrame: The updated DataFrame with a new 'Patient Name' column, or
        None if the required columns are not found.
    """

    try:
        if "First Name" in df.columns and "Last Name" in df.columns:
            df["Patient Name"] = (
                df["Last Name"].str.strip() + ", " + df["First Name"].str.strip()
            )

            return df

    except Exception as e:
        print(f"An error occurred: {e}")
        # Optionally, you could return None or raise the error again depending on your needs.
        # return None
        raise


def standardize_address(df):
    """
    Standardizes address columns in the DataFrame and creates new columns for combined addresses.

    This function renames specific columns related to origin addresses and creates new columns
    for combined 'Pick Up Address' and 'Drop Off Address' by concatenating street, city, state,
    and postal code columns. It checks for the presence of required columns before performing
    operations.

    Args:
        df (pd.DataFrame): The DataFrame containing address information.

    Returns:
        pd.DataFrame: The updated DataFrame with renamed columns and new combined address columns.
    """
    pickup_required_columns = [
        "Origin Street",
        "Origin City",
        "Origin State",
        "Origin Postal",
        "Destination Street",
        "Destination City",
        "Destination State",
        "Destination Postal",
    ]

    try:
        # Check for required columns
        missing_columns = [
            col for col in pickup_required_columns if col not in df.columns
        ]
        if missing_columns:
            raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")

        # Convert columns to string type to avoid .str accessor issues
        for column in pickup_required_columns:
            df[column] = df[column].astype(str).str.strip()

        # Create new address columns
        df["Pick Up Address"] = (
            df["Origin Street"]
            + ", "
            + df["Origin City"]
            + ", "
            + df["Origin State"]
            + ", "
            + df["Origin Postal"]
        )

        df["Drop Off Address"] = (
            df["Destination Street"]
            + ", "
            + df["Destination City"]
            + ", "
            + df["Destination State"]
            + ", "
            + df["Destination Postal"]
        )

        # Define column mapping to compare PU Address between traumasoft and ctc dataframes
        column_mapping = {
            "Origin Street": "PU Address",
            "Origin City": "PU City",
            "Origin State": "PU State",
            "Origin Postal": "PU Zip",
        }

        df = df.rename(columns=column_mapping)

    except Exception as e:
        print(f"An error occurred: {e}")
        # Optionally, you could return None or raise the error again depending on your needs.
        # return None
        raise

    return df


def normalize_date(date_str):
    parts = date_str.split("/")
    return "/".join(str(int(part)) for part in parts)


def normalize_address(address):
    """
    Normalizes an address and returns the first line of the address.

    This function takes an address, normalizes it using the `normalize_address_record`
    function, and returns the "address_line_1" component. If an error occurs during
    normalization, it handles the exception and returns None.

    Args:
        address (str): The address to be normalized.

    Returns:
        str: The normalized first line of the address ("address_line_1"), or
        None if normalization fails.
    """
    try:
        normalized = normalize_address_record(address)
        return normalized.get("address_line_1")
    except Exception as e:
        print(f"Error normalizing address {address}: {e}")
        return None


def normalize_and_concatenate_address(address):
    """
    Normalizes an address and concatenates its components into a single string.

    This function takes an address, normalizes it using the `normalize_address_record`
    function, and concatenates the components (address line 1, address line 2, city,
    state, and postal code) into a single string. Components that are None or empty
    are omitted from the concatenated string. If an error occurs during normalization,
    the function handles the exception and returns None.

    Args:
        address (str): The address to be normalized.

    Returns:
        str: The normalized and concatenated address string, or None if normalization fails.
    """
    try:
        normalized = normalize_address_record(address)
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
        print(f"Error normalizing address {address}: {e}")
        return None
