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
    flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE, scope=SCOPES)
    storage = Storage(f"{API_SERVICE_NAME}-{API_VERSION}.oauth2.json")
    credentials = storage.get()

    if credentials is None or credentials.invalid:
        credentials = run_flow(flow, storage)

    return build(API_SERVICE_NAME, API_VERSION, credentials=credentials)


def upload_video(
    youtube, file_path, title, description, category_id, keywords, privacy_status
):
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

def list_my_videos(youtube, max_results=25):
    """
    List videos from the authenticated user's channel along with their URLs.

    Parameters:
    youtube: The authenticated youtube service object.
    max_results (int): Maximum number of videos to retrieve.

    Returns:
    List of videos with their IDs, titles, and URLs.
    """
    # Retrieve the list of videos uploaded to the authenticated user's channel.
    request = youtube.videos().list(
        part='snippet,contentDetails,statistics',
        maxResults=max_results,
        mine=True  # Set to True to list videos uploaded by the user
    )
    response = request.execute()

    videos = []
    for item in response.get('items', []):
        video_id = item['id']
        videos.append({
            'id': video_id,
            'title': item['snippet']['title'],
            'description': item['snippet']['description'],
            'statistics': item['statistics'],
            'url': f'https://www.youtube.com/watch?v={video_id}'
        })

    return videos

def download_video(url):
    yt = YouTube(url)
    yt.streams.get_highest_resolution().download("results/downloads/")
    print("Downloaded video from YouTube")


def main():
    youtube = get_authenticated_service()
    file_path = "results/vids/frankenstein.mp4"
    title = "pix-code-color-frankenstein"
    description = "Testing for pix-code color video upload"
    category_id = "22"
    keywords = ["storage", "encryption"]
    privacy_status = "unlisted"

    upload_response = upload_video(
        youtube, file_path, title, description, category_id, keywords, privacy_status
    )
    print("Uploaded video with ID:", upload_response["id"])


if __name__ == "__main__":
    main()
