from multiprocessing import cpu_count
from moviepy.editor import *
from random import randint

def R(min:int,max:int):
    return randint(min,max)

def assemble_video(video_subclip_filename:str,audio_subclip_filename:str,tts_filename:str,quote:str, id:int):
    h=1920
    w=1080 
    
    video_subclip = VideoFileClip(video_subclip_filename)
    video_subclip = video_subclip.resize(height=h) 
    video_subclip_h = video_subclip.size[0]
    video_subclip_w = video_subclip.size[1]
    video_subclip = video_subclip.crop(x_center=video_subclip_w/2, y1=0, width=w, y2=h) 
 
    audio_subclip = AudioFileClip(audio_subclip_filename)
    tts = AudioFileClip(tts_filename)

    video_subclip = video_subclip.volumex(0) 
    audio_subclip = audio_subclip.volumex(0.2) 
    tts = tts.volumex(0.75) 

    combined_audio = CompositeAudioClip([audio_subclip, tts])


    final_clip = video_subclip.set_audio(combined_audio)
     
    duration = final_clip.duration
    words = quote.split(" ")
     
    letter_duration = duration/ len(quote.replace(" ","").replace("te","t"))
    colors = ['white','yellow']
    shadows = ['gray10','gray20','gray30','gray40'] 

    text_clips = []
    word_start = 0

    for i, word in enumerate(words):
        word_duration = len(word)*letter_duration
        
        text_q = TextClip(word, fontsize=150, color=colors[R(0,len(colors)-1)], size=final_clip.size)
        text_q = text_q.set_duration(word_duration).set_opacity(0.88).set_start(word_start).set_position((0,0))
 
        text_shadow = TextClip(word, fontsize=155, color=shadows[R(0,len(shadows)-1)], size=final_clip.size)
        text_shadow = text_shadow.set_duration(word_duration).set_opacity(0.75).set_start(word_start).set_position((0,3))

        # shadow first
        text_clips.append(text_shadow)
        text_clips.append(text_q)

        word_start += word_duration
  
    final_clip = CompositeVideoClip([final_clip, *text_clips])

    if not os.path.exists("results"):
        os.mkdir("results")

    final_filename=f"results/quote-{id}.mp4"
    final_clip.write_videofile(final_filename,threads=cpu_count(),verbose=False ,fps=24)

    print("Finished assembling video!!!")
 