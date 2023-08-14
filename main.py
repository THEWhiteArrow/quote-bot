from moviepy.editor import *
from quotes.quotes_wrapper import get_quotes
from utils.toml_helper import *
from video_creation.background import *
from video_creation.assemble import *


def prepare_toml():
    if not exists_toml("./config.toml"):
        create_toml_config()


def main(clean_temp=True):
    prepare_toml()

    download_background_video()
    download_background_audio()

    quotes = get_quotes()

    process_quotes(quotes, clean_temp)

    print("Finished assembling ALL videos!!!")


if __name__ == "__main__":
    main(True)
