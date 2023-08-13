from moviepy.editor import *
from utils.toml_helper import *
from random import randint
from time import time
from math import ceil, floor
import yt_dlp

config = load_config()

def R(a:float, b:float):
    a = floor(a)
    b = ceil(b)
    return randint(a, b)

def download_background_video():  
    video_url = config["background"]["video_url"]
    video_name = config["background"]["video_name"]
    video_credit = config["background"]["video_credit"]

 
    # check if file exists
    if os.path.exists(f"assets/background/video/{video_credit}-{video_name}.mp4"):
        print("Background video already exists!")
        return
    
    print("Downloading background video...")
    ydl_opts = {
        "format": "bestvideo[height<=1080][ext=mp4]",
        "outtmpl": f"assets/background/video/{video_credit}-{video_name}.mp4",
        "retries": 10,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

    print("Downloaded background video!")

def download_background_audio():  
    audio_url = config["background"]["audio_url"]
    audio_name = config["background"]["audio_name"]
    audio_credit = config["background"]["audio_credit"]
     
    # check if file exists
    if os.path.exists(f"assets/background/audio/{audio_credit}-{audio_name}.mp3"):
        print("Background audio already exists!")
        return
    
    print("Downloading background audio...")
    
    ydl_opts = {
        "outtmpl": f"assets/background/audio/{audio_credit}-{audio_name}.mp3",
        "format": "bestaudio/best",
        "extract_audio": True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([audio_url])

    print("Downloaded background audio!")

    

def get_video_subclip(length:int=10, id:str=time()):
    # load bg video
    video_name = config["background"]["video_name"]
    video_credit = config["background"]["video_credit"]
    video = VideoFileClip(f"assets/background/video/{video_credit}-{video_name}.mp4")
    # make a subclip of it with length
    
    start=R(0, video.duration - length)
    end=start+length
    subclip = video.subclip(start, end)
    # save it

    # creat temp folder if not exists
    if not os.path.exists("temp"):
        os.mkdir("temp")

    filename = f"temp/video-subclip-{id}.mp4"
    subclip.write_videofile(filename, fps=24)

    print("Created video subclip!")

    return filename
 
def get_audio_subclip(length:int=10, id:str=time()):
    # load bg audio
    audio_name = config["background"]["audio_name"]
    audio_credit = config["background"]["audio_credit"]
    audio = AudioFileClip(f"assets/background/audio/{audio_credit}-{audio_name}.mp3")
    # make a subclip of it with length
    
    start=R(0, audio.duration - length)
    end=start+length
    subclip = audio.subclip(start, end)
    # save it

    # creat temp folder if not exists
    if not os.path.exists("temp"):
        os.mkdir("temp")

    filename = f"temp/audio-subclip-{id}.mp3"
    
    subclip.write_audiofile(filename)

    print("Created audio subclip!")

    return filename
 