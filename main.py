import yt_dlp
import sys
import json
import os
import uuid

def get_video_info(video_url):
    ydl_opts = {
        'no_warnings': True,
        'skip_download': True,
        'noplaylist': True
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(video_url, download=False)
        video_info = {
            'url': video_url,
            'title': info_dict.get('title', None),
            'thumbnail_url': info_dict.get('thumbnail', None),
            'author': info_dict.get('uploader', None),
            'duration': info_dict.get('duration', None),
        }
    return video_info


def download_audio(video_url, no_play_list, download_path='./', cookies=None):
    video_id = str(uuid.uuid4())
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
        'noplaylist': no_play_list,
        'outtmpl': f'%(title)s_{video_id}.%(ext)s',
        'cookie': cookies
        
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(video_url, download=True)
        file_path = ydl.prepare_filename(result)
        file_path = os.path.splitext(file_path)[0] + '.mp3'

    print(file_path)
    return file_path

if __name__ == "__main__":
    command = sys.argv[1]
    no_play_list = sys.argv[2]
    video_url = sys.argv[3]
    download_path = sys.argv[4]
    print("EJECUTANDO")

    if command == 'info':
        print("ENTRA A INFO")
        video_info = get_video_info(video_url)
        print(json.dumps(video_info))
    elif command == 'download':
        download_audio(video_url, no_play_list, download_path)
    else:
        print('Invalid command')
