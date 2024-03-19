Instagram Profile Checker
=========================

Description
-----------
This script is designed to check the validity of Instagram profiles. It allows users to input Instagram usernames either manually or from a CSV file, checks if these profiles are available on Instagram, and exports the results to a CSV file and a text file.

Features
--------
- Load Instagram usernames from a CSV file or manual input.
- Check the availability of each Instagram profile.
- Export the results to a CSV file and a separate text file for invalid profiles.
- Logging of all activities, including errors and info messages.

Requirements
------------
- Python 3
- Selenium WebDriver
- `chardet` library for character encoding detection

Setup
-----
1. Ensure Python 3 is installed on your system.
2. Install Selenium WebDriver and `chardet`:



3. Download the appropriate WebDriver for your browser and ensure it's in your PATH.

Usage
-----
1. Run the script:


2. Choose the data source:
- Enter '1' to load from a CSV file.
- Enter '2' to input data manually.
- Enter 'back' to exit the script.
3. If you chose to load from a CSV file, provide the file path when prompted.
4. If you chose manual input, enter the Instagram usernames as instructed.
5. After the script finishes checking the profiles, choose whether to export the results.
6. Find the exported files and logs in the specified directory.

CSV File Format
---------------
The CSV file should have a column named 'ig user' with Instagram usernames.

Output
------
- A CSV file named `instagram_profiles.csv` containing the usernames and their validity status.
- A text file named `invalid_users.txt` listing all invalid usernames.
- Log files are created in the specified directory for each script execution.
