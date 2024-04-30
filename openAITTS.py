from pathlib import Path
from pydub import AudioSegment
from pydub.generators import Sine
import json
from openai import OpenAI
import tempfile

def speak_with_pauses(segments_json, rate=150):
    segments = json.loads(segments_json)

    # Initialize the result array
    result = []

    audio_segments = []
    durations = []
    asset_list = []

    client = OpenAI()

    for i in range(1, len(segments)):
        sentence = segments[i-1].get('sentence')
        pause_duration = segments[i-1].get('pause')
        asset = segments[i-1].get('asset')

        if sentence:
            response = client.audio.speech.create(
                model="tts-1",
                voice="alloy",
                input=sentence
            )
            with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as temp_audio_file:
                temp_audio_file.write(response.content)
                temp_audio_file.close()
                audio_segment = AudioSegment.from_file(temp_audio_file.name)
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

    return ['final_audio_with_pauses.mp3', asset_list]

# Example usage
# test_text = """[
#     {"sentence": "Welcome back folks!", "asset": "welcome.mp4", "pause": 100},
#     {"sentence": "Today, we're going to discuss a fundamental aspect of game development: collision detection.", "asset": "collision_detection.mp4", "pause": 100},
#     {"sentence": "Now, you might be wondering, what exactly is collision detection?", "pause": 1000},
#     {"sentence": "Well, it's the process of determining when two objects in a game world intersect or come into contact with each other.", "pause": 200},
#     {"sentence": "This might sound straightforward, but trust me, there's a bit more to it than meets the eye.", "pause": 300},
#     {"sentence": "Let's delve deeper into this topic and explore how we can implement collision detection in our game.", "pause": 300}
# ]"""
# output_ = speak_with_pauses(test_text, 150)
# print("Asset list:", output_[1])
