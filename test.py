import pyttsx3
import re
from pydub import AudioSegment
from pydub.generators import Sine
import json

def speak_with_pauses(text, rate=150):
    # Regular expression for pause keyword and duration
    pause_regex = r"PAUSE\s+(\d+)"

    sentences = []
    pause_durations = []

    # Split the text into sentences
    parts = re.split(pause_regex, text)

    # Iterate over the parts
    i = 0
    while i < len(parts):
        part = parts[i].strip()

        # Check if it's not empty
        if part:
            sentences.append(part)

        # Check if there's a pause duration following the part
        if i + 1 < len(parts) and parts[i + 1]:
            pause_durations.append(int(parts[i + 1]))
        else:
            pause_durations.append(0)  # No pause for non-pause parts

        # Move to the next part
        i += 2

    audio_segments = []
    durations = []  # to store the duration of each segment

    engine = pyttsx3.init()
    engine.setProperty('rate', rate)

    for sentence, pause_duration in zip(sentences, pause_durations):
        engine.save_to_file(sentence, 'temp.wav')
        engine.runAndWait()

        audio_segment = AudioSegment.from_wav("temp.wav")
        audio_segments.append(audio_segment)
        duration = len(audio_segment) / 1000  # convert milliseconds to seconds
        durations.append(duration)

        if pause_duration > 0:
            silence_segment = Sine(0).to_audio_segment(duration=pause_duration)  # Convert to milliseconds
            audio_segments.append(silence_segment)
            durations.append(pause_duration / 1000)  # convert milliseconds to seconds

    # Concatenate audio segments
    output_audio = audio_segments[0]
    for segment in audio_segments[1:]:
        output_audio = output_audio.append(segment, crossfade=0)

    # Create JSON object to store duration data
    duration_json = {}
    for i, dur in enumerate(durations):
        duration_json[f"Segment {i+1}"] = dur

    with open('pause_durations.json', 'w') as json_file:
        json.dump(duration_json, json_file, indent=4)

    return output_audio

# Example usage
text = """The challenges have forged our skills. [PAUSE 1000] Our latest creation is a testament to the passion and dedication that drives us. [PAUSE 2000] Stay tuned as we unveil more updates and behind-the-scenes glimpses."""
output_audio = speak_with_pauses(text, 150)
output_audio.export("final_audio_with_pauses.mp3", format="mp3")
print("Audio exported successfully.")
