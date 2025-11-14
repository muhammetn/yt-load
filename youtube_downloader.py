import yt_dlp
import os
from pathlib import Path

def get_video_info(url):
    """
    Get information about a video or playlist before downloading
    """
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            if 'entries' in info:
                # It's a playlist
                print(f"Playlist: {info.get('title', 'Unknown')}")
                print(f"Number of videos: {len(info['entries'])}")
                print("\nVideos in playlist:")
                for i, entry in enumerate(info['entries']):
                    if entry:
                        print(f"{i+1}. {entry.get('title', 'Unknown')}")
            else:
                # It's a single video
                print(f"Title: {info.get('title', 'Unknown')}")
                print(f"Duration: {info.get('duration', 'Unknown')} seconds")
                print(f"Uploader: {info.get('uploader', 'Unknown')}")
                print(f"View count: {info.get('view_count', 'Unknown')}")
                
            return info
    except Exception as e:
        print(f"An error occurred while fetching info: {e}")
        return None

def download_video_hq(url, output_path="downloads"):
    """
    Download YouTube video in high quality (up to 1080p) with audio
    """
    # Create output directory if it doesn't exist
    Path(output_path).mkdir(exist_ok=True)
    
    # CORRECT configuration for high quality with audio
    ydl_opts = {
        # This format selector ensures video+audio merging
        'format': 'bestvideo[height<=1080]+bestaudio/best[height<=1080]',
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        'merge_output_format': 'mp4',  # Important: specifies output format after merging
        
        # FFmpeg configuration for merging - FIXED this section
        'postprocessors': [
            {
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
            },
            {
                'key': 'FFmpegMetadata',
            }
        ],
        
        # Additional options
        'writesubtitles': True,
        'writeautomaticsub': True,
        'subtitleslangs': ['en'],
        'ignoreerrors': True,
        'no_warnings': False,  # Changed to False to see warnings
        'verbose': True,  # Added for debugging
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"Downloading: {url}")
            # Get info first to show what we're downloading
            info = ydl.extract_info(url, download=False)
            print(f"Title: {info.get('title', 'Unknown')}")
            print(f"Duration: {info.get('duration', 0)} seconds")
            
            # Now download
            ydl.download([url])
            print("Download completed successfully!")
            return info
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def download_playlist_hq(url, output_path="downloads"):
    """
    Download entire YouTube playlist in high quality with audio
    """
    Path(output_path).mkdir(exist_ok=True)
    
    ydl_opts = {
        'format': 'bestvideo[height<=1080]+bestaudio/best[height<=1080]',
        'outtmpl': os.path.join(output_path, '%(playlist_title)s', '%(title)s.%(ext)s'),
        'merge_output_format': 'mp4',
        'postprocessors': [
            {
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
            },
            {
                'key': 'FFmpegMetadata',
            }
        ],
        'writesubtitles': True,
        'writeautomaticsub': True,
        'subtitleslangs': ['en'],
        'ignoreerrors': True,
        'no_warnings': False,
        'verbose': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"Downloading playlist: {url}")
            
            # Get playlist info first
            info = ydl.extract_info(url, download=False)
            if 'entries' in info:
                print(f"Playlist: {info.get('title', 'Unknown')}")
                print(f"Number of videos: {len(info['entries'])}")
            
            # Download the playlist
            ydl.download([url])
            print("Playlist download completed!")
    except Exception as e:
        print(f"An error occurred: {e}")

def check_system_requirements():
    """
    Check if required tools are available
    """
    try:
        # Check if ffmpeg is available by trying to get its version
        result = os.popen('ffmpeg -version').read()
        if 'ffmpeg version' in result:
            print("✅ FFmpeg is available")
            return True
        else:
            print("❌ FFmpeg not found. Please install FFmpeg for best results.")
            return False
    except:
        print("❌ FFmpeg not found. Please install FFmpeg for best results.")
        return False

# Alternative format selectors if the above doesn't work:
def get_alternative_format_selectors():
    """
    Different format selectors you can try
    """
    formats = {
        "option1": "bestvideo[height<=1080]+bestaudio/best[height<=1080]",
        "option2": "bv[height<=1080]+ba/b[height<=1080]",
        "option3": "best[height<=1080]",  # This might get lower quality but ensures audio
        "option4": "bestvideo+bestaudio/best",
        "option5": "mp4/best[height<=1080]",  # Force MP4 container
    }
    return formats

def download_with_fallback(url, output_path="downloads", is_playlist=False):
    """
    Try multiple format selectors until one works
    """
    format_selectors = get_alternative_format_selectors()
    
    for name, format_selector in format_selectors.items():
        print(f"\nTrying format selector: {name} - {format_selector}")
        
        ydl_opts = {
            'format': format_selector,
            'outtmpl': os.path.join(output_path, '%(playlist_title)s', '%(title)s.%(ext)s') if is_playlist else os.path.join(output_path, '%(title)s.%(ext)s'),
            'merge_output_format': 'mp4',
            'ignoreerrors': True,
            'no_warnings': False,
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                if is_playlist:
                    result = ydl.download([url])
                else:
                    result = ydl.download([url])
                
                print(f"✅ Success with format: {name}")
                return True
                
        except Exception as e:
            print(f"❌ Failed with format {name}: {e}")
            continue
    
    print("❌ All download attempts failed!")
    return False

def main():
    print("YouTube Video/Playlist Downloader (HD with Audio)")
    print("=" * 50)
    
    # Check system requirements
    check_system_requirements()
    
    while True:
        print("\nOptions:")
        print("1. Download single video")
        print("2. Download playlist")
        print("3. Get video/playlist info")
        print("4. Download with fallback options (if regular download fails)")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == '1':
            url = input("Enter YouTube video URL: ").strip()
            output_path = input("Enter output directory (default: 'downloads'): ").strip()
            output_path = output_path if output_path else "downloads"
            download_video_hq(url, output_path)
            
        elif choice == '2':
            url = input("Enter YouTube playlist URL: ").strip()
            output_path = input("Enter output directory (default: 'downloads'): ").strip()
            output_path = output_path if output_path else "downloads"
            download_playlist_hq(url, output_path)
            
        elif choice == '3':
            url = input("Enter YouTube URL: ").strip()
            get_video_info(url)
            
        elif choice == '4':
            url = input("Enter YouTube URL: ").strip()
            output_path = input("Enter output directory (default: 'downloads'): ").strip()
            output_path = output_path if output_path else "downloads"
            is_playlist = input("Is this a playlist? (y/n): ").strip().lower() == 'y'
            download_with_fallback(url, output_path, is_playlist)
            
        elif choice == '5':
            print("Goodbye!")
            break
            
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()