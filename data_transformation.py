import re
import pandas as pd


def extract_wait_time_and_oxygen(comment):
    """
    Returns wait time and oxygen
    Receives comment
    """
    # Define the pattern to match
    pattern = r"Wait time:\s*(\d+)\s*minutes(?:.*?\b(\d+)\s*(?:liter|liters|LPM|L|lts|LITERS|lt|l)\b)?"

    # Remove single and double quotes from the pattern
    comment = comment.replace("'", "").replace('"', "")

    # Search for the pattern in the string
    match = re.search(pattern, comment)

    # If a match is found, extract the numbers
    if match:
        wait_time = int(match.group(1))
        oxygen_match = match.group(2)
        if oxygen_match:
            oxygen = int(oxygen_match)
        elif any(word in comment for word in ["Therapist REQ", "Deep suction", "Vent"]):
            oxygen = None
        elif (
            any(word in comment for word in ["Therapist REQ", "Deep suction", "Vent"])
            and oxygen_match is None
        ):
            oxygen = None
        else:
            oxygen = 0
    else:
        wait_time = 0
        oxygen = 0

    return [wait_time, oxygen]


def standardize_name(self):
    # Specify the path to the CSV file you want to read
    file_path = "import/"

    # Load the CSV file into a DataFrame
    df = pd.read_csv(file_path, index_col=False)

    # Check the structure and contents of the DataFrame
    print(df.head())

    # Check if "First Name" and "Last Name" columns exist in the DataFrame
    if "First Name" in df.columns and "Last Name" in df.columns:
        # Create a new "Patient Name" column combining "Last Name" and "First Name"
        df["Patient Name"] = (
            df["Last Name"].str.strip() + ", " + df["First Name"].str.strip()
        )

        # Display the first few rows of the updated DataFrame to verify the changes
        print(df.head())

        # Specify the directory where you want to save the updated CSV file
        output_folder = "output"
        os.makedirs(
            output_folder, exist_ok=True
        )  # Create the directory if it doesn't exist

        # Specify the path where you want to save the updated CSV file
        output_file_path = os.path.join(output_folder, "updated.csv")

        # Save the updated DataFrame to a new CSV file
        df.to_csv(output_file_path, index=False)

        print(f"Updated CSV file saved to {output_file_path}")
    else:
        print("Columns 'First Name' and 'Last Name' are not found in the CSV file.")


# def standardize_address(self, street, city, state, postal):
#     """
#     Renames "Origin Street" to "PU Address"
#             "Origin City" to "PU City"
#             "Origin State" to "PU State"
#             "Origin Postal" to "PU Zip"
#     Receives Origin Street, Origin City, Origin State, Origin Postal
#     """
#     pass
