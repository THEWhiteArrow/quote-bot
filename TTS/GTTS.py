import random
from gtts import gTTS
 


class GTTS:
    def __init__(self):
        self.max_chars = 5000
        self.voices = []

    def run(self, text, filepath,slow=False, random_voice=False):
        tts = gTTS(
            text=text,
            lang="en",
            slow=slow,
        ) 
        tts.save(filepath)

    def randomvoice(self):
        return random.choice(self.voices)
