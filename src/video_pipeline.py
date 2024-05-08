from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from oauth2client.file import Storage
from oauth2client.client import flow_from_clientsecrets
from oauth2client.tools import run_flow
from pytube import YouTube

CLIENT_SECRETS_FILE = "credentials/pix-code.json"
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"

def get_authenticated_service():
    """
    Create an authenticated YouTube service object by obtaining user credentials or
    refreshing existing ones. This function facilitates the OAuth2 flow using
    the client secrets file and stores the credentials for future use.

    Returns:
        googleapiclient.discovery.Resource: Authenticated YouTube API service object.
    """
    flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE, scope=SCOPES)
    storage = Storage(f"{API_SERVICE_NAME}-{API_VERSION}.oauth2.json")
    credentials = storage.get()

    if credentials is None or credentials.invalid:
        credentials = run_flow(flow, storage)

    return build(API_SERVICE_NAME, API_VERSION, credentials=credentials)

def upload_video(youtube, file_path, title, description, category_id, keywords, privacy_status):
    """
    Uploads a video file to YouTube using the provided YouTube service object.

    Args:
        youtube (Resource): Authenticated YouTube API service object.
        file_path (str): Path to the video file to be uploaded.
        title (str): Title of the video.
        description (str): Description of the video.
        category_id (str): YouTube category ID for the video.
        keywords (list[str]): List of tags for the video.
        privacy_status (str): Privacy status of the video (e.g., 'public', 'private', 'unlisted').

    Returns:
        dict: The API response containing information about the uploaded video.
    """
    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": keywords,
            "categoryId": category_id,
        },
        "status": {"privacyStatus": privacy_status},
    }

    insert_request = youtube.videos().insert(
        part=",".join(body.keys()),
        body=body,
        media_body=MediaFileUpload(file_path, chunksize=-1, resumable=True),
    )

    response = insert_request.execute()
    return response

def download_video(url):
    """
    Downloads the highest resolution video available from the specified YouTube URL
    and saves it locally.

    Args:
        url (str): The URL of the YouTube video to be downloaded.
    """
    yt = YouTube(url)
    yt.streams.get_highest_resolution().download("results/downloads/")
    print("Downloaded video from YouTube")