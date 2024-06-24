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

import re
from scourgify import normalize_address_record


def remove_trailing_nan_rows(df, column_name):
    """
    Removes all rows starting from the first row where the specified column has NaN values.

    This function searches for the first occurrence of NaN in the specified column
    and removes that row and all subsequent rows from the DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame to be cleaned.
        column_name (str): The name of the column to check for NaN values.

    Returns:
        pd.DataFrame: The cleaned DataFrame without trailing rows that contain NaN
        in the specified column.

    Raises:
        IndexError: If there are no NaN values in the specified column.
    """
    # Find the index of the first row where the specified column is NaN
    first_nan_index = df[df[column_name].isna()].index[0]

    # Drop all rows from the first NaN row to the end
    cleaned_df = df.iloc[:first_nan_index]

    return cleaned_df


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
    # Define the patterns to match wait time and oxygen separately
    wait_time_pattern = r"Wait time:\s*(\d+)\s*minutes"
    oxygen_pattern = r"(\d+)\s*(?:liter|liters|LPM|L|lts|LITERS|lt|l)\b"

    # Search for wait time in the comment
    wait_time_match = re.search(wait_time_pattern, comment, re.IGNORECASE)
    wait_time = int(wait_time_match.group(1)) if wait_time_match else 0

    # Search for oxygen in the comment
    oxygen_match = re.search(oxygen_pattern, comment, re.IGNORECASE)
    oxygen = int(oxygen_match.group(1)) if oxygen_match else 0

    # Additional check for phrases that imply oxygen is required but not explicitly mentioned
    if (
        "Therapist REQ" in comment
        or "Deep suction" in comment
        or "Vent" in comment
        or "tracheostomy" in comment
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
        # Check if "First Name" and "Last Name" columns exist in the DataFrame
        if "First Name" in df.columns and "Last Name" in df.columns:
            # Create a new "Patient Name" column combining "Last Name" and "First Name"
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

        # Create a new "Pick Up Address" column
        df["Pick Up Address"] = (
            df["Origin Street"]
            + ", "
            + df["Origin City"]
            + ", "
            + df["Origin State"]
            + ", "
            + df["Origin Postal"]
        )

        # Create a new "Drop Off Address" column
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

    # Print the updated DataFrame (for debugging purposes)
    # print("Updated DataFrame (standardize_address):\n", df, "\n")


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
        # Normalize the address
        normalized = normalize_address_record(address)
        # Return only the "address_line_1" value
        return normalized.get("address_line_1")
    except Exception as e:
        # Handle errors in address normalization
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
