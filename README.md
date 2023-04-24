# YouTube Channel Subscription Tool

This tool allows you to subscribe to a list of YouTube channels using the YouTube API v3. The list of channels should be provided as a CSV file with one channel URL per line. The tool handles authentication through OAuth 2.0, and it requires a client secrets JSON file to interact with the YouTube API.

## Requirements

- Python 3.6 or higher
- Google API Python Client
- Google Auth OAuthlib

You can install the required packages using the following command:
```
pip install google-api-python-client google-auth-oauthlib
```

### Export your YouTube subscriptions
1. Go to the [Google takeout manager](https://takeout.google.com/takeout/custom/youtube).
2. Log in if asked.
3. Click on "All YouTube data included", then on "Deselect all", then select only "subscriptions" and click "OK".
4. Click on "Next step" and then on "Create export".
5. Click on the "Download" button after it appears. (This is the CSV the script will use.)

## Setup

1. Create a new project in the [Google Developers Console](https://console.developers.google.com/).
2. Enable the YouTube Data API v3 for your project.
3. Create OAuth 2.0 credentials and download the client secrets JSON file. (Make sure to add the [/auth/youtube](https://www.googleapis.com/auth/youtube.force-ssl) scope in the OAuth consent screen) 
4. Rename the downloaded file to `client_secrets.json` and place it in the same directory as the script.
5. Place the CSV file from Google takeout in the same directory as the script and name it `channels.csv`.

## Usage
```
usage: python subscribe.py [--secrets SECRETS] [--csv CSV]

Subscribe to a list of YouTube channels from a CSV file.

optional arguments:
--secrets SECRETS Path to the client secrets JSON file (default: client_secrets.json)
--csv CSV Path to the CSV file with channel URLs (default: channels.csv)
```

## Example

To subscribe to the channels listed in a CSV file called `channels.csv` using the `client_secrets.json` file for authentication, run the following command:
```python subscribe.py --secrets client_secrets.json --csv channels.csv```


## License

This project is released under the MIT License.
