from moviepy.editor import *
from gtts import gTTS as gtts 
from quotes.quotes_wrapper import get_quotes


def convert_video():
    clip = VideoFileClip("./goku.mp4")

    text_q = TextClip("Hello World", fontsize=20, color='white', size=clip.size)
    text_q = text_q.set_duration(5).set_pos('center').set_opacity(0.6)

    final_clip = CompositeVideoClip([clip, text_q])
    final_clip.write_videofile("final.mp4", fps=24)

def convert_tts():
    tts = gtts("<speak>Hello world<mark/> yo how u doing?</speak>", lang="en")
    tts.save("hello.mp3")
    
def prepare_toml():
    # TODO: Create a toml file with the following structure:
    # [quotes]
    # min_length = 75
    # max_length = 100
    pass


 







if __name__ == "__main__":
    # convert_video()
    # convert_tts()
    prepare_toml()
    print( get_quotes() ) 