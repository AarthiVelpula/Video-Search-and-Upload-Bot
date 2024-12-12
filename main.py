import os
import requests
import asyncio
from pathlib import Path
from tqdm import tqdm
import aiohttp
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

FLIC_TOKEN = "flic_c8d6459f17f02bc9fe7508d5f1d204b148c759f30ec775ff8a897e2d839c8112"
INSTAGRAM_ACCESS_TOKEN = "your_instagram_access_token"
INSTAGRAM_USER_ID = "your_instagram_id"
BASE_DIR = Path("videos")
BASE_DIR.mkdir(exist_ok=True)

INSTAGRAM_BASE_URL = "https://graph.instagram.com"
GENERATE_UPLOAD_URL = "https://api.socialverseapp.com/posts/generate-upload-url"
CREATE_POST_URL = "https://api.socialverseapp.com/posts"

def fetch_reels_by_hashtag(hashtag, limit=5, languages=["en", "hi"]):
    print(f"Fetching reels for hashtag: {hashtag}")
    search_url = f"{INSTAGRAM_BASE_URL}/ig_hashtag_search?user_id={INSTAGRAM_USER_ID}&q={hashtag}&access_token={INSTAGRAM_ACCESS_TOKEN}"
    response = requests.get(search_url)
    response.raise_for_status()
    hashtag_id = response.json()['data'][0]['id']
    reels_url = f"{INSTAGRAM_BASE_URL}/{hashtag_id}/top_media?user_id={INSTAGRAM_USER_ID}&fields=id,media_type,media_url,caption,language&access_token={INSTAGRAM_ACCESS_TOKEN}"
    response = requests.get(reels_url)
    response.raise_for_status()
    reels = [item for item in response.json()['data'] if item['media_type'] == "VIDEO" and item.get('language') in languages][:limit]
    return reels

async def download_video(video_url, video_id):
    print(f"Downloading video: {video_url}")
    async with aiohttp.ClientSession() as session:
        async with session.get(video_url) as response:
            response.raise_for_status()
            filepath = BASE_DIR / f"{video_id}.mp4"
            with open(filepath, "wb") as f:
                async for chunk in response.content.iter_any():
                    f.write(chunk)
            print(f"Downloaded video: {filepath}")
    return filepath

def generate_upload_url():
    headers = {"Flic-Token": FLIC_TOKEN, "Content-Type": "application/json"}
    response = requests.get(GENERATE_UPLOAD_URL, headers=headers)
    response.raise_for_status()
    return response.json()

async def upload_video(filepath, upload_url):
    print(f"Uploading video: {filepath}")
    async with aiohttp.ClientSession() as session:
        with open(filepath, "rb") as f:
            async with session.put(upload_url, data=f) as response:
                response.raise_for_status()
    print(f"Uploaded video: {filepath}")

def create_post(title, hash_value, category_id=1):
    headers = {"Flic-Token": FLIC_TOKEN, "Content-Type": "application/json"}
    payload = {
        "title": title,
        "hash": hash_value,
        "is_available_in_public_feed": False,
        "category_id": category_id,
    }
    response = requests.post(CREATE_POST_URL, json=payload, headers=headers)
    response.raise_for_status()
    print(f"Post created: {response.json()['id']}")

async def process_videos():
    hashtag = "motivation"
    reels = fetch_reels_by_hashtag(hashtag, limit=5)
    print(reels)  # Debugging to ensure reels are fetched correctly.

    for reel in reels:
        video_url = reel['media_url']
        video_id = reel['id']
        filepath = await download_video(video_url, video_id)

        upload_data = generate_upload_url()
        upload_url = upload_data['upload_url']
        hash_value = upload_data['hash']

        await upload_video(filepath, upload_url)

        create_post(title="Motivational Reel", hash_value=hash_value, category_id=1)

        os.remove(filepath)
        print(f"Deleted local file: {filepath}")

class VideoHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.src_path.endswith('.mp4'):
            print(f"New video detected: {event.src_path}")
            asyncio.run(process_videos())

def monitor_directory():
    event_handler = VideoHandler()
    observer = Observer()
    observer.schedule(event_handler, path=str(BASE_DIR), recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    print("Starting the application...")
    
    # Test process_videos directly
    asyncio.run(process_videos())
    
    # Uncomment this if directory monitoring is needed
    # print("Starting directory monitoring...")
    # monitor_directory()
