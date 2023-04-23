import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import os
import re
import sys
import csv
import argparse

def get_channel_id(youtube, url):
    """
    Extracts the channel ID from a given YouTube URL.

    Args:
        youtube: A YouTube API client instance.
        url (str): The YouTube channel URL.

    Returns:
        str: The channel ID if found, None otherwise.
    """
    patterns = [
        r"(?<=channel/)[a-zA-Z0-9_-]+",  # Channel URL
        r"(?<=user/)[a-zA-Z0-9_-]+"      # User URL
    ]

    for pattern in patterns:
        channel_id = re.search(pattern, url)
        if channel_id:
            return channel_id.group(0)

    return None

def subscribe_to_channels(credentials, channel_urls):
    youtube = googleapiclient.discovery.build("youtube", "v3", credentials=credentials)

    for url in channel_urls:
        channel_id = get_channel_id(youtube, url)
        if channel_id:
            try:
                youtube.subscriptions().insert(
                    part="snippet",
                    body={
                        "snippet": {
                            "resourceId": {
                                "kind": "youtube#channel",
                                "channelId": channel_id
                            }
                        }
                    }
                ).execute()
                print(f"Subscribed to channel with ID: {channel_id}")
            except googleapiclient.errors.HttpError as error:
                print(f"An error occurred: {error}")
                print("Could not subscribe to the channel.")
        else:
            print(f"Invalid URL: {url}")

def read_urls_from_csv(file_path):
    if not os.path.isfile(file_path):
        print(f"Error: CSV file '{file_path}' not found.")
        sys.exit(1)

    channel_urls = []
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)  # Skip the header
        for row in reader:
            channel_urls.append(row[1])  # URLs are in the second column

    return channel_urls

def get_oauth_credentials(client_secrets_file, scopes):
    if not os.path.isfile(client_secrets_file):
        print(f"Error: Client secrets file '{client_secrets_file}' not found.")
        sys.exit(1)

    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_local_server(port=0)
    return credentials

def main(client_secrets_file, csv_file_path):
    scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]
    credentials = get_oauth_credentials(client_secrets_file, scopes)
    channel_urls = read_urls_from_csv(csv_file_path)
    subscribe_to_channels(credentials, channel_urls)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Subscribe to a list of YouTube channels from a CSV file.")
    parser.add_argument("--secrets", help="Path to the client secrets JSON file", default="client_secrets.json")
    parser.add_argument("--csv", help="Path to the CSV file with channel URLs", default="channels.csv")
    args = parser.parse_args()

    main(args.secrets, args.csv)
