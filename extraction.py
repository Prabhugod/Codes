import requests
import os

base_url = "http://fmac.in/2ND_SEM_2021/"
output_directory = "mark_sheets_2nd_semester_ZOOLOGY/"

# Create the output directory if it doesn't exist
os.makedirs(output_directory, exist_ok=True)

for roll_number in range(85001, 85011):  # Loop through roll numbers
    roll_number_str = f"21C{roll_number:05d}"
    url = f"{base_url}{roll_number_str}.pdf"
    file_name = f"{output_directory}{roll_number_str}.pdf"

    response = requests.get(url)

    if response.status_code == 200:
        with open(file_name, "wb") as file:
            file.write(response.content)
        print(f"File '{file_name}' downloaded successfully.")
    else:
        print(f"Failed to download the file for roll number {roll_number_str}.")

print("All files downloaded.")
