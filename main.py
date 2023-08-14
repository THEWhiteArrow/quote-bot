import shutil
from moviepy.editor import * 
from quotes.quotes_wrapper import get_quotes
from utils.toml_helper import *
from video_creation.background import *
from utils.ffmpeg_install import *
from TTS.TikTok import *
from video_creation.assemble import *



def prepare_toml():
    if not exists_toml("./config.toml"):
        create_toml_config()

def main(clean_temp=True):
    prepare_toml()

    download_background_video()
    download_background_audio()

    quotes = get_quotes()  
    
    if len(quotes) == 0:
        print("No quotes found")
        return
    else:
        print(f"Found {len(quotes)} quotes:")
      
    for i,q in enumerate(quotes):
        tts = TikTok()
        print(f"Processing quote {i+1}/{len(quotes)}")
        id=q.id
        quote=q.quote
        tts_filename=f"temp/tts-{id}.mp3"

        if not os.path.exists("temp"):
            os.mkdir("temp")
            
        tts.run(quote, tts_filename, random_voice=config["settings"]["tts"]["random_voice"])
        duration = AudioFileClip(tts_filename).duration
        video_subclip_filename=get_video_subclip(duration,id)
        audio_subclip_filename=get_audio_subclip(duration,id)

        assemble_video(video_subclip_filename,audio_subclip_filename,tts_filename,quote,id)

    # remove temp folder
    if os.path.exists("temp") and clean_temp:
        shutil.rmtree("temp")




if __name__ == "__main__": 
    main(False)

 

    

