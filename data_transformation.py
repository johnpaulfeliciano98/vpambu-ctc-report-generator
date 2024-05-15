import re


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


# def standardize_name(self):
#     """
#     Returns "lname + "," + fname"
#     Receives First Name, Last Name
#     """
#     pass


# def standardize_address(self, street, city, state, postal):
#     """
#     Renames "Origin Street" to "PU Address"
#             "Origin City" to "PU City"
#             "Origin State" to "PU State"
#             "Origin Postal" to "PU Zip"
#     Receives Origin Street, Origin City, Origin State, Origin Postal
#     """
#     pass
