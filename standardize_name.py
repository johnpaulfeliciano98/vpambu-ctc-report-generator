import os
import pandas as pd

# Specify the path to the CSV file you want to read
file_path = "import/Download(via_Manifest)_16e15fa4-b454-4c30-8a76-2945bdff6d8c.csv"

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
