from multiprocessing import cpu_count
import shutil
from typing import List
from moviepy.editor import *
from random import randint
from TTS.TikTok import *
from video_creation.background import *
from utils.quote_helper import *

config = load_config()


def R(min: int, max: int):
    return randint(min, max)


def create_text_shadows(
    word, word_duration, word_start, size, font_size: int = 140
) -> List[TextClip]:
    shadows = ["gray10", "gray20", "gray30", "gray40"]
    ans = []
    shadow_color = shadows[R(0, len(shadows) - 1)]

    text_shadow = (
        TextClip(
            word,
            fontsize=font_size,
            color=shadow_color,
            size=size,
        )
        .set_duration(word_duration)
        .set_opacity(0.5)
        .set_start(word_start)
    )

    ans = [
        text_shadow.set_position((0, 3)),
        text_shadow.set_position((0, -3)),
        text_shadow.set_position((-3, 0)),
        text_shadow.set_position((3, 0)),
    ]
    return ans


def merge_subclips_and_tts(
    video_subclip_filename, audio_subclip_filename, tts_filename
) -> CompositeVideoClip:
    h = 1920
    w = 1080

    video_subclip = VideoFileClip(video_subclip_filename)
    video_subclip = video_subclip.resize(height=h)
    video_subclip_h = video_subclip.size[0]
    video_subclip_w = video_subclip.size[1]
    video_subclip = video_subclip.crop(
        x_center=video_subclip_w / 2, y1=0, width=w, y2=h
    )

    audio_subclip = AudioFileClip(audio_subclip_filename)
    tts = AudioFileClip(tts_filename)

    video_subclip = video_subclip.volumex(0)
    audio_subclip = audio_subclip.volumex(0.15)
    tts = tts.volumex(0.85).set_start(config["quotes"]["extra_duration"] / 2)

    combined_audio = CompositeAudioClip([audio_subclip, tts])

    final_clip = video_subclip.set_audio(combined_audio)
    return final_clip


def merge_text_clips_by_word(quote, id, duration, size) -> List[TextClip]:
    words = quote.split(" ")

    letter_duration = duration / len(quote.replace(" ", "").replace("te", "t"))
    colors = ["white", "yellow"]

    text_clips = []
    word_start = 0
    for i, word in enumerate(words):
        word_duration = len(word) * letter_duration
        if i == 0:
            word_duration += config["quotes"]["extra_duration"] / 2

        text_q = TextClip(
            word,
            fontsize=140,
            color=colors[R(0, len(colors) - 1)],
            size=size,
        )
        text_q = (
            text_q.set_duration(word_duration).set_opacity(0.88).set_start(word_start)
        )

        text_shadows = []
        text_shadows = create_text_shadows(word, word_duration, word_start, size)

        # shadow first
        text_clips.extend(text_shadows)
        text_clips.append(text_q)

        word_start += word_duration

    return text_clips


def merge_text_clips_by_pharse(quote, id, duration, size) -> List[TextClip]:
    words = quote.split(" ")

    quote_len = len(quote)
    words_len = len(words)
    avg_word_len = quote_len / words_len

    letter_duration = duration / len(quote.replace(" ", "").replace("te", "t"))
    colors = ["white", "yellow"]

    text_clips = []
    word_start = 0

    pharse = ""
    first_pharse = True
    fontsize = 90
    for i, word in enumerate(words):
        if len(pharse) < 1.5 * avg_word_len and i + 1 != len(words):
            pharse += word + " "
            continue
        else:
            pharse += word
            word_duration = len(pharse.replace(" ", "")) * letter_duration
            if first_pharse:
                word_duration += config["quotes"]["extra_duration"] / 2
                first_pharse = False

            text_q = (
                TextClip(
                    pharse,
                    fontsize=fontsize,
                    color=colors[R(0, len(colors) - 1)],
                    size=size,
                )
                .set_duration(word_duration)
                .set_opacity(0.88)
                .set_start(word_start)
            )

            text_shadows = []
            text_shadows = create_text_shadows(
                pharse, word_duration, word_start, size, font_size=fontsize
            )

            # shadow first
            text_clips.extend(text_shadows)
            text_clips.append(text_q)

            word_start += word_duration
            pharse = ""

    return text_clips


def save_result(final_clip: CompositeVideoClip, id: str) -> None:
    if not os.path.exists("results"):
        os.mkdir("results")

    final_filename = f"results/quote-{id}.mp4"
    final_clip.write_videofile(
        final_filename, threads=cpu_count(), verbose=False, fps=24
    )


def assemble_video(
    video_subclip_filename: str,
    audio_subclip_filename: str,
    tts_filename: str,
    quote: str,
    id: int,
) -> None:
    final_clip = merge_subclips_and_tts(
        video_subclip_filename, audio_subclip_filename, tts_filename
    )

    text_clips = merge_text_clips_by_pharse(
        quote, id, final_clip.duration, final_clip.size
    )

    final_clip = CompositeVideoClip([final_clip, *text_clips])

    save_result(final_clip, id)

    print("Finished assembling video!!!")


def process_quotes(quotes, clean_temp) -> None:
    if len(quotes) == 0:
        print("No quotes found")
        return
    else:
        print(f"Found {len(quotes)} quotes:")

    tts = TikTok()
    for i, q in enumerate(quotes):
        try:
            print(f"Processing quote {i+1}/{len(quotes)}")
            id = q.id
            quote = q.quote
            tts_filename = f"temp/tts-{id}.mp3"

            if not os.path.exists("temp"):
                os.mkdir("temp")

            tts.run(
                quote,
                tts_filename,
                random_voice=config["settings"]["tts"]["random_voice"],
            )
            duration = AudioFileClip(tts_filename).duration
            duration += config["quotes"]["extra_duration"]
            video_subclip_filename = get_video_subclip(duration, id)
            audio_subclip_filename = get_audio_subclip(duration, id)

            assemble_video(
                video_subclip_filename, audio_subclip_filename, tts_filename, quote, id
            )

            save_quote_to_history(q)
        except Exception as e:
            print(f"Failed to process quote number {i+1}. Skipping...")
            print(f"Error: {e}")
        except KeyboardInterrupt:
            print("Keyboard interrupt detected. Exiting...")
            break

    if os.path.exists("temp") and clean_temp:
        shutil.rmtree("temp")
