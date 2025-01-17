# from django.views.decorators.csrf import csrf_exempt
# from django.shortcuts import render
# from django.http import FileResponse, HttpResponse
# import yt_dlp
# import os
# import re

# # Global variable to store progress information
# download_progress = {
#     'eta': None,
#     'total_size': None,
#     'downloaded_bytes': None
# }

# # Progress hook function to capture ETA and size
# def progress_hook(d):
#     if d['status'] == 'downloading':
#         download_progress['eta'] = d.get('eta')
#         download_progress['total_size'] = d.get('total_bytes')
#         download_progress['downloaded_bytes'] = d.get('downloaded_bytes')
#         print(f"Downloading... {download_progress['downloaded_bytes']}/{download_progress['total_size']} bytes. ETA: {download_progress['eta']}s")

# # Function to download the TikTok video
# def download_tiktok_video(url):
#     match = re.match(r'https://www\.tiktok\.com/@([^/]+)/video/(\d+)', url)
#     if not match:
#         print("Invalid TikTok URL.")
#         return None

#     username = match.group(1)  
#     video_id = match.group(2)  
#     video_path = f'videos/{username}_{video_id}.mp4'
    
#     ydl_opts = {
#         'format': 'best',
#         'noplaylist': True,
#         'outtmpl': video_path,  
#         'quiet': False,
#         'progress_hooks': [progress_hook],  # Attach progress hook here
#         'postprocessors': [{
#             'key': 'FFmpegVideoConvertor',
#             'preferedformat': 'mp4',
#         }],
#     }

#     with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#         try:
#             ydl.download([url])
#             print("Video downloaded successfully!")
#             return video_path
#         except Exception as e:
#             print(f"Error downloading video: {e}")
#             return None

# # View to handle TikTok video download request
# @csrf_exempt
# def downloader_tiktok(request):
#     if request.method == "POST":
#         tiktok_url = request.POST.get('tiktok_url')  
#         print(f"TikTok URL Received: {tiktok_url}")

#         # Download the video
#         video_path = download_tiktok_video(tiktok_url)
        
#         if video_path and os.path.exists(video_path):
#             # Use FileResponse for proper file handling
#             response = FileResponse(open(video_path, 'rb'), content_type='video/mp4')
#             response['Content-Disposition'] = f'attachment; filename={os.path.basename(video_path)}'
            
#             # Display ETA and size in the response
#             eta = download_progress.get('eta')
#             total_size = download_progress.get('total_size')
#             response['Content-Length'] = total_size if total_size else os.path.getsize(video_path)
#             response['X-Download-ETA'] = f'{eta} seconds' if eta else 'Unknown ETA'
            
#             return response
        
#         return HttpResponse("Error downloading video.")
    
#     return render(request, "download_html.html")


from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import FileResponse, HttpResponse
import yt_dlp
import os

# Global variable to store progress information
download_progress = {
    'eta': None,
    'total_size': None,
    'downloaded_bytes': None
}

# Progress hook function to capture ETA and size
def progress_hook(d):
    if d['status'] == 'downloading':
        download_progress['eta'] = d.get('eta')
        download_progress['total_size'] = d.get('total_bytes')
        download_progress['downloaded_bytes'] = d.get('downloaded_bytes')
        print(f"Downloading... {download_progress['downloaded_bytes']}/{download_progress['total_size']} bytes. ETA: {download_progress['eta']}s")

# Function to download video from any URL
def download_video(url):
    video_path = 'videos/downloaded_video.mp4'  # Default filename (can be changed to something more dynamic)
    
    ydl_opts = {
        'format': 'best',
        'noplaylist': True,
        'outtmpl': video_path,  # Save file as downloaded_video.mp4 in the videos directory
        'quiet': False,
        'progress_hooks': [progress_hook],  # Attach progress hook here
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([url])
            print("Video downloaded successfully!")
            return video_path
        except Exception as e:
            print(f"Error downloading video: {e}")
            return None

# View to handle video download request
@csrf_exempt
def downloader(request):
    if request.method == "POST":
        video_url = request.POST.get('video_url')  # Generic 'video_url' field for any video
        print(f"Video URL Received: {video_url}")

        # Download the video
        video_path = download_video(video_url)
        
        if video_path and os.path.exists(video_path):
            # Use FileResponse for proper file handling
            response = FileResponse(open(video_path, 'rb'), content_type='video/mp4')
            response['Content-Disposition'] = f'attachment; filename={os.path.basename(video_path)}'
            
            # Display ETA and size in the response
            eta = download_progress.get('eta')
            total_size = download_progress.get('total_size')
            response['Content-Length'] = total_size if total_size else os.path.getsize(video_path)
            response['X-Download-ETA'] = f'{eta} seconds' if eta else 'Unknown ETA'
            
            return response
        
        return HttpResponse("Error downloading video.")
    
    return render(request, "download_html.html")
