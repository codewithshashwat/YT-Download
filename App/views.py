# downloader/views.py
import os
import re
import json
import subprocess
from django.shortcuts import render, redirect
from django.http import FileResponse, HttpResponse
from django.urls import reverse
from .forms import DownloadForm
from django.conf import settings
import uuid

def home(request):
    form = DownloadForm()
    return render(request, 'index.html', {'form': form})

def download_video(request):
    if request.method == 'POST':
        form = DownloadForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            try:
                # Use yt-dlp to get video info
                cmd = ['yt-dlp', '-J', url]
                result = subprocess.run(cmd, capture_output=True, text=True)
                
                if result.returncode != 0:
                    raise ValueError(f"yt-dlp error: {result.stderr}")
                
                video_data = json.loads(result.stdout)
                
                # Extract video information
                video_info = {
                    'title': video_data['title'],
                    'thumbnail': video_data['thumbnail'],
                    'duration': format_duration(video_data['duration']),
                    'author': video_data['uploader'],
                    'views': format_views(video_data.get('view_count', 0)),
                    'video_id': video_data['id'],
                }
                
                # Get available formats
                streams = []
                for format in video_data['formats']:
                    if format.get('vcodec') != 'none' and format.get('acodec') != 'none':
                        resolution = format.get('height', 0)
                        if resolution > 0:
                            streams.append({
                                'resolution': f"{resolution}p",
                                'format_id': format['format_id'],
                                'filesize': format_size(format.get('filesize', 0)),
                                'mime_type': format.get('ext', 'mp4'),
                            })
                
                # Sort by resolution (highest first)
                streams = sorted(streams, key=lambda x: int(x['resolution'].replace('p', '')), reverse=True)
                
                return render(request, 'download.html', {
                    'video_info': video_info,
                    'streams': streams,
                })
            except Exception as e:
                error_message = f"An error occurred: {str(e)}"
                return render(request, 'index.html', {
                    'form': form,
                    'error_message': error_message,
                    'troubleshooting_tips': True
                })
    else:
        form = DownloadForm()
    
    return render(request, 'index.html', {'form': form})

def download_file(request, resolution, video_id):
    try:
        url = f"https://www.youtube.com/watch?v={video_id}"
        
        # Create media directory if it doesn't exist
        os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
        
        # Generate a unique filename
        unique_id = str(uuid.uuid4())[:8]
        
        # Get video info to get the title
        cmd = ['yt-dlp', '-J', url]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            raise ValueError(f"yt-dlp error: {result.stderr}")
        
        video_data = json.loads(result.stdout)
        sanitized_title = re.sub(r'[^\w\s-]', '', video_data['title']).strip().replace(' ', '_')
        filename = f"{sanitized_title}_{unique_id}.mp4"
        file_path = os.path.join(settings.MEDIA_ROOT, filename)
        
        # Download the video with specified resolution
        height = resolution.replace('p', '')
        cmd = [
            'yt-dlp', 
            '-f', f'best[height<={height}]', 
            '-o', file_path,
            url
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            raise ValueError(f"Download failed: {result.stderr}")
        
        # Serve the file
        if os.path.exists(file_path):
            response = FileResponse(open(file_path, 'rb'))
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response
        else:
            return HttpResponse("Downloaded file could not be found", status=404)
    
    except Exception as e:
        return HttpResponse(f"Download failed: {str(e)}", status=500)

# Helper functions
def format_duration(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    if hours > 0:
        return f"{hours}:{minutes:02d}:{seconds:02d}"
    else:
        return f"{minutes}:{seconds:02d}"

def format_views(views):
    if views >= 1_000_000:
        return f"{views/1_000_000:.1f}M"
    elif views >= 1_000:
        return f"{views/1_000:.1f}K"
    return str(views)

def format_size(bytes):
    if bytes == 0:
        return "Unknown"
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes < 1024:
            return f"{bytes:.1f} {unit}"
        bytes /= 1024
    return f"{bytes:.1f} TB"