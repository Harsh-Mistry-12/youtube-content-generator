"""
VPN Connection:
1) Australia (Works Fine)
2) Netherlands (Does not Work)
"""

import yt_dlp

def download_tiktok_video(url, download_path='videos/bikes/custom_sporty.mp4'):
    # Set options for yt-dlp to avoid the watermark
    ydl_opts = {
        'format': 'best',  # Download the best video quality
        'noplaylist': True,  # Ensure only one video is downloaded, not a playlist
        'outtmpl': download_path,  # Set output file path
        'quiet': False,  # Show progress and errors (optional)
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',  # This is for converting the video format
            'preferedformat': 'mp4',  # Convert the video to mp4 format
        }],
        'writeinfojson': False,  # Don't save video info in a JSON file
        'noprogress': False,  # Show download progress
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([url])  # Download the video
            print(f"Video downloaded successfully at {download_path}")
        except Exception as e:
            print(f"Error downloading video: {e}")

if __name__ == "__main__":
    # Replace this with the TikTok video URL you want to download
    video_url = 'https://www.tiktok.com/@blackster883/video/7008472880660925701'
    download_tiktok_video(video_url)
