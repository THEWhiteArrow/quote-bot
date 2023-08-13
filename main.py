from moviepy.editor import *
from gtts import gTTS as gtts
from quotes.quotes_wrapper import get_quotes
from utils.toml_helper import *
from video_creation.background import *
from utils.ffmpeg_install import *
from TTS.TikTok import *
from video_creation.assemble import *

def convert_video():
    clip = VideoFileClip("./goku.mp4")

    text_q = TextClip("Hello World", fontsize=20, color="white", size=clip.size)
    text_q = text_q.set_duration(5).set_pos("center").set_opacity(0.6)

    final_clip = CompositeVideoClip([clip, text_q])
    final_clip.write_videofile("final.mp4", fps=24)


def convert_tts():
    tts = gtts("<speak>Hello world<mark/> yo how u doing?</speak>", lang="en")
    tts.save("hello.mp3")


def prepare_toml():
    if not exists_toml("./config.toml"):
        create_toml_config()


if __name__ == "__main__": 
    # prepare_toml()
    # quotes = get_quotes()  
    
    # tts = TikTok()
    # for q in quotes:
    #     id=q.timestamp
    #     quote=q.quote
    #     tts_filename=f"temp/tts-{id}.mp3"

    #     if not os.path.exists("temp"):
    #         os.mkdir("temp")
            
    #     tts.run(quote, tts_filename)
    #     duration = AudioFileClip(tts_filename).duration
    #     video_subclip_filename=get_video_subclip(duration,id)
    #     audio_subclip_filename=get_audio_subclip(duration,id)

    #     #   assemble_video()
    #     assemble_video(video_subclip_filename,audio_subclip_filename,tts_filename,quote,id)


    # assemble_video(
    #     "temp/video-subclip-1691932240.mp4",
    #     "temp/audio-subclip-1691932240.mp3",
    #     "temp/tts-1691932240.mp3",
    #     "Hello world text to speech",
    #     1691932240
    # )
    assemble_video(
        "assets/background/video/demo.mp4",
        "assets/background/audio/demo.mp3",
        "assets/background/audio/demo1.mp3",
        "Hello world text to speech",
        1691932240
    )

