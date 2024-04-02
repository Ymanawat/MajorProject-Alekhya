import pyttsx3
import re
from pydub import AudioSegment
from pydub.generators import Sine
import json

def speak_with_pauses(text, rate=150):
    # Regular expression for asset and pause durations
    asset_pause_regex = r'{(?:\s*"asset"\s*:\s*"([^"]*)"?\s*,)?\s*"pause"\s*:\s*(\d+)\s*}'

    segments = re.split(asset_pause_regex, text)
    print('segments', segments)

    audio_segments = []
    durations = []
    asset_list = []

    engine = pyttsx3.init()
    engine.setProperty('rate', rate)

    for i in range(1, len(segments), 3):
        sentence = segments[i-1].strip()
        pause_duration = int(segments[i+1])
        asset = segments[i] 

        if sentence:
            engine.save_to_file(sentence, 'temp.wav')
            engine.runAndWait()

            audio_segment = AudioSegment.from_wav("temp.wav")
            audio_segments.append(audio_segment)
            duration = len(audio_segment) / 1000  # convert milliseconds to seconds
            durations.append(duration)
        
        asset_list.append({"time": sum(durations), "asset": asset})

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

    # Export the audio
    output_audio.export("final_audio_with_pauses.mp3", format="mp3")
    print("Audio exported successfully.")

    return output_audio, asset_list

# Example usage
text = """The challenges have forged our skills. { "pause": 1000 } Our latest creation is a testament to the passion and dedication that drives us. { "asset": "outro.mp4", "pause": 2000 } Stay tuned as we unveil more updates and behind-the-scenes glimpses."""
output_audio, asset_list = speak_with_pauses(text, 150)
print("Asset list:", asset_list)
