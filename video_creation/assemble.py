from moviepy.editor import *
from random import randint

def R(min:int,max:int):
    return randint(min,max)

def assemble_video(video_subclip_filename:str,audio_subclip_filename:str,tts_filename:str,quote:str, id:int):
    video_subclip = VideoFileClip(video_subclip_filename)
    audio_subclip = AudioFileClip(audio_subclip_filename)
    tts = AudioFileClip(tts_filename)

    video_subclip = video_subclip.volumex(0) 
    audio_subclip = audio_subclip.volumex(1)
    tts = tts.volumex(0.5)

    combined_audio = CompositeAudioClip([audio_subclip, tts])


    final_clip = video_subclip.set_audio(combined_audio)
    
    duration = final_clip.duration
    words = quote.split(" ")
    words_count = len(words)
    word_duration = duration/words_count
    colors = ['white','yellow']

    for i, word in enumerate(words):
        text_q = TextClip(word, fontsize=20, color=colors[R(0,len(colors)-1)], size=final_clip.size)

        text_q = text_q.set_duration(word_duration).set_pos("center").set_opacity(0.86).set_start(i*word_duration)
        final_clip = CompositeVideoClip([final_clip, text_q])


    if not os.path.exists("results"):
        os.mkdir("results")

    final_filename=f"results/final-{id}.mp4"
    final_clip.write_videofile(final_filename, fps=24)

    print("Finished assembling video!!!")