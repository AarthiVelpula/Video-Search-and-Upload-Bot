This Python-based bot automates the process of searching for motivational videos (Instagram reels in English or Hindi), downloading the videos, uploading the videos to a server using provided APIs, and automatically deleting local files post-upload.  

Features include fetching motivational videos based on hashtags, saving Instagram videos locally in `.mp4` format, uploading videos to a server using pre-signed URLs, automatically removing downloaded videos after upload, monitoring the `/videos` directory for new `.mp4` files and processing them, handling downloads and uploads concurrently with asynchronous operations, and managing API errors and file operations gracefully.  

Ensure Python 3.8+ is installed. Install dependencies using `pip install -r requirements.txt`. Required dependencies: `aiohttp`, `requests`, `tqdm`, `watchdog`.  

Clone the repository using `git clone <repository_url>` and navigate to the folder. Configure API credentials in `main.py` by replacing `INSTAGRAM_ACCESS_TOKEN` with your Instagram Graph API access token and `INSTAGRAM_USER_ID` with your Instagram account's User ID. Run the bot using `python main.py`.  

The bot searches Instagram for reels using the hashtag `#motivation`, filters videos in English or Hindi, and downloads them as `.mp4` files saved in the `/videos` directory. Using server-provided APIs, it fetches pre-signed URLs for uploading, uploads videos to the server, and creates posts with metadata for uploaded videos. The `/videos` directory is monitored for new `.mp4` files, which are processed automatically.  

APIs used include generating an upload URL via `GET` at `https://api.socialverseapp.com/posts/generate-upload-url` with headers containing the `Flic-Token` and `Content-Type`, uploading videos using the pre-signed URL via `PUT`, and creating posts via `POST` at `https://api.socialverseapp.com/posts` with headers and a JSON body containing the title, hash, and category ID.  

Prepare a 5-minute video demonstrating setup, code walkthrough, and functionality, including fetching, downloading, uploading, and cleaning up files.  

Ensure Instagram API credentials are valid, verify server endpoints are reachable, and test the script end-to-end before submission.  

Evaluation criteria include code quality (30%), functionality (40%), documentation (15%), and presentation (15%). Upload `main.py`, `requirements.txt`, and `README.md` to the GitHub repository, submit the repository link, and share a video presentation.
