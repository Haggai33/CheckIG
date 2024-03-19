
import re
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
import time
import csv
from datetime import datetime
import logging
import os
import chardet

def setup_logging():
    log_filename = datetime.now().strftime("instagram_check_%Y%m%d_%H%M%S.log")
    log_filepath = os.path.join("C:\\Users\\User\\Downloads", log_filename)
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s: %(levelname)s - %(message)s',
                        handlers=[
                            logging.FileHandler(log_filepath),
                            logging.StreamHandler()
                        ])

def load_ig_users_from_csv(file_path):
    ig_users_from_csv = []
    valid_count = 0
    empty_count = 0
    error_count = 0

    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
        file_encoding = result['encoding']

    try:
        with open(file_path, mode='r', encoding=file_encoding) as file:
            reader = csv.DictReader(file)
            reader.fieldnames = [name.lower() for name in reader.fieldnames]
            column_name = "ig user"

            if column_name not in reader.fieldnames:
                raise ValueError("Column 'ig user' not found in the CSV file")

            for row in reader:
                try:
                    ig_user = row.get(column_name)
                    if ig_user and ig_user.strip():
                        ig_users_from_csv.append(ig_user.strip())
                        valid_count += 1
                    else:
                        empty_count += 1
                except Exception as e:
                    error_count += 1
    except Exception as e:
        print(f"Error reading file: {e}")

    print(f"Valid rows extracted: {valid_count}")
    print(f"Empty rows encountered: {empty_count}")
    print(f"Rows with errors: {error_count}")

    return ig_users_from_csv

def extract_artist_and_usernames():
    logging.info("Starting to extract artist names and usernames")
    print("Example format:\nThe Hip Abduction\n@thehipabduction\n.\nCatching Flies\n@catchingfliesmusic\n.")
    print("Please enter the text (press Enter twice to end input):")
    input_lines = []

    while True:
        line = input()
        if line == '':
            break
        input_lines.append(line)

    artist_user_pairs = []

    for i in range(1, len(input_lines)):
        if input_lines[i].startswith('@'):
            artist_name = input_lines[i-1].strip()
            ig_user = input_lines[i].strip().lstrip('@')
            artist_user_pairs.append((artist_name, ig_user))

    logging.info("Extraction complete")
    return artist_user_pairs

def check_instagram_profiles(ig_users):
    logging.info("Starting Instagram profile check")
    driver = webdriver.Chrome()
    profile_status = {}

    base_url = "https://www.instagram.com/"

    for username in ig_users:
        try:
            url = base_url + username
            driver.get(url)
            time.sleep(2)
            page_source = driver.page_source
            if "Sorry, this page isn't available." in page_source:
                profile_status[username] = False
                logging.info(f"Profile {username} is not valid")
            else:
                profile_status[username] = True
                logging.info(f"Profile {username} is valid")
        except WebDriverException as e:
            logging.error(f"WebDriverException for profile {username}: {e}")
            profile_status[username] = False
        except Exception as e:
            logging.error(f"Error checking profile {username}: {e}")
            profile_status[username] = False

    driver.quit()
    logging.info("Instagram profile check complete")
    return profile_status

def export_to_csv(profile_status, file_path):
    try:
        logging.info("Exporting results to CSV")
        with open(file_path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['IG User', 'Valid', 'Timestamp'])
            for username, is_valid in profile_status.items():
                writer.writerow([username, 'Valid' if is_valid else 'Not Valid', datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
        print(f"CSV file exported to {file_path}")
        logging.info("CSV export complete")
    except Exception as e:
        logging.error(f"Error exporting to CSV: {e}")
        print(f"Error exporting to CSV. Check log for details.")


def export_invalid_users(profile_status, file_path):
    try:
        logging.info("Exporting invalid users to text file")
        with open(file_path, 'w', encoding='utf-8') as file:
            for username, is_valid in profile_status.items():
                if not is_valid:
                    file.write(f"{username}\n.\n")
        print(f"Text file exported to {file_path}")
        logging.info("Invalid users export complete")
    except Exception as e:
        logging.error(f"Error exporting invalid users to text file: {e}")
        print(f"Error exporting invalid users to text file. Check log for details.")

def handle_data_source_selection():
    while True:
        input_choice = input("Enter '1' to load from CSV, '2' to enter text manually, or 'back' to go back: ").lower()
        if input_choice == 'back':
            return None, None
        elif input_choice == '1':
            file_path = input("Please enter the file path for the CSV file: ")
            return 'csv', file_path
        elif input_choice == '2':
            return 'text', None
        else:
            print("Invalid input. Please enter '1', '2', or 'back'.")

def main():
    setup_logging()
    data_source, file_path = handle_data_source_selection()

    if data_source == 'csv':
        ig_users = load_ig_users_from_csv(file_path)
    elif data_source == 'text':
        artist_user_pairs = extract_artist_and_usernames()
        ig_users = [username for artist, username in artist_user_pairs]  # רק שמות המשתמשים
    else:
        return

    profile_status = check_instagram_profiles(ig_users)

    export_choice = input("Do you want to export the results (CSV and text files)? (y/n): ").lower()
    if export_choice == 'y':
        csv_file_path = os.path.join("C:\\Users\\User\\Downloads", "instagram_profiles.csv")
        invalid_users_file_path = os.path.join("C:\\Users\\User\\Downloads", "invalid_users.txt")
        export_to_csv(profile_status, csv_file_path)
        export_invalid_users(profile_status, invalid_users_file_path)

    for username, is_valid in profile_status.items():
        print(f"IG User: {username}, Status: {'Valid' if is_valid else 'Not Valid'}")

    logging.info("Script execution completed")

if __name__ == "__main__":
    main()



# import re
# from selenium import webdriver
# import time
# import csv
# from datetime import datetime
# import logging
# import os
#
# # Set up logging to file and console
# log_filename = datetime.now().strftime("instagram_check_%Y%m%d_%H%M%S.log")
# log_filepath = os.path.join("C:\\Users\\User\\Downloads", log_filename)
# logging.basicConfig(level=logging.INFO,
#                     format='%(asctime)s: %(levelname)s - %(message)s',
#                     handlers=[
#                         logging.FileHandler(log_filepath),
#                         logging.StreamHandler()
#                     ])
#
# def extract_artist_and_usernames():
#     logging.info("Starting to extract artist names and usernames")
#     print("Please enter the text (press Enter twice to end input):")
#     print("Example format:\nThe Hip Abduction\n@thehipabduction\n.\nCatching Flies\n@catchingfliesmusic\n.")
#     input_lines = []
#
#     while True:
#         line = input()
#         if line == '':
#             break
#         input_lines.append(line)
#
#     text = '\n'.join(input_lines)
#     artist_user_pairs = []
#
#     for i in range(1, len(input_lines)):
#         if input_lines[i].startswith('@'):
#             artist_name = input_lines[i-1].strip()
#             ig_user = input_lines[i].strip().lstrip('@')
#             artist_user_pairs.append((artist_name, ig_user))
#
#     logging.info("Extraction complete")
#     return artist_user_pairs
#
# def check_instagram_profiles(artist_user_pairs):
#     logging.info("Starting Instagram profile check")
#     driver = webdriver.Chrome()
#     profile_status = {}
#
#     base_url = "https://www.instagram.com/"
#
#     for artist, username in artist_user_pairs:
#         try:
#             url = base_url + username
#             driver.get(url)
#             time.sleep(2)
#             page_source = driver.page_source
#             if "Sorry, this page isn't available." in page_source:
#                 profile_status[(artist, username)] = False
#                 logging.info(f"Profile {username} ({artist}) is not valid")
#             else:
#                 profile_status[(artist, username)] = True
#                 logging.info(f"Profile {username} ({artist}) is valid")
#         except Exception as e:
#             logging.error(f"Error checking profile {username} ({artist}): {e}")
#             profile_status[(artist, username)] = False
#
#     driver.quit()
#     logging.info("Instagram profile check complete")
#     return profile_status
#
# def export_to_csv(profile_status, file_path):
#     try:
#         logging.info("Exporting results to CSV")
#         with open(file_path, 'w', newline='', encoding='utf-8') as file:
#             writer = csv.writer(file)
#             writer.writerow(['Artist Name', 'IG User', 'Valid', 'Timestamp'])
#             for (artist, username), is_valid in profile_status.items():
#                 writer.writerow([artist, username, 'Valid' if is_valid else 'Not Valid', datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
#         print(f"CSV file exported to {file_path}")
#         logging.info("CSV export complete")
#     except Exception as e:
#         logging.error(f"Error exporting to CSV: {e}")
#
# def export_invalid_users(profile_status, file_path):
#     try:
#         logging.info("Exporting invalid users to text file")
#         with open(file_path, 'w', encoding='utf-8') as file:
#             for (artist, username), is_valid in profile_status.items():
#                 if not is_valid:
#                     file.write(f"{artist}\n{username}\n.\n")
#         print(f"Text file exported to {file_path}")
#         logging.info("Invalid users export complete")
#     except Exception as e:
#         logging.error(f"Error exporting invalid users to text file: {e}")
#
# # Extract artist names and usernames from user input
# artist_user_pairs = extract_artist_and_usernames()
#
# # Check the Instagram profiles
# profile_status = check_instagram_profiles(artist_user_pairs)
#
# # Ask user if they want to export results
# export_choice = input("Do you want to export the results (CSV and text files)? (y/n): ").lower()
# if export_choice == 'y':
#     csv_file_path = os.path.join("C:\\Users\\User\\Downloads", "instagram_profiles.csv")
#     invalid_users_file_path = os.path.join("C:\\Users\\User\\Downloads", "invalid_users.txt")
#
#     # Export results to CSV
#     export_to_csv(profile_status, csv_file_path)
#
#     # Export invalid users to a text file
#     export_invalid_users(profile_status, invalid_users_file_path)
#
# # Print results
# for (artist, username), is_valid in profile_status.items():
#     print(f"Artist: {artist}, IG User: {username}, Status: {'Valid' if is_valid else 'Not Valid'}")
#
# logging.info("Script execution completed")
#
#
