import re
import time
import pyttsx3

def speak(text, rate=150):
  engine = pyttsx3.init()
  engine.setProperty('rate', rate)
  engine.say(text)
  engine.runAndWait()

def speak_and_save(text, output_filename, rate=150):
  engine = pyttsx3.init()
  engine.setProperty('rate', rate)

  # Regular expression for pause keyword and duration
  pause_regex = r"PAUSE\s+(\d+)"

  # Process text and replace pause keywords with SSML breaks
  modified_text = ""
  for sentence in text.splitlines():  # Split into sentences for better handling
    # Find all pause occurrences in the sentence
    pauses = re.findall(pause_regex, sentence)
    print(pauses)
    # Process each word and pause
    for word in sentence.split():
      if word.upper() == "PAUSE":
        # Extract pause duration from next word (assuming integer in milliseconds)
        try:
          pause_duration = int(pauses.pop(0))
          modified_text += f"<break time='{pause_duration}'/> "  # Insert SSML break
        except (IndexError, ValueError):
          print("Warning: Invalid PAUSE keyword format. Ignoring.")
          modified_text += word + " "
      else:
        modified_text += word + " "  # Append normal words

  # Speak and save
  engine.say(modified_text)
  # engine.save_to_file(modified_text, output_filename)
  engine.runAndWait()


import re
import time
import pyttsx3
from pydub import AudioSegment
import os

def speak_with_pauses(text, rate=150):
    engine = pyttsx3.init()
    engine.setProperty('rate', rate)
    pause_regex = r"(?:PAUSE\s*(\d+)\s*)"
    sentences = []
    pause_durations = []
    parts = re.split(pause_regex, text)
    i = 0
    while i < len(parts):
        part = parts[i].strip()
        if part:
            sentences.append(part)
        if i + 1 < len(parts) and parts[i + 1]:
            pause_durations.append(int(parts[i + 1]))
        else:
            pause_durations.append(0)
        i += 2

    audio = AudioSegment.empty()
    for i, sentence in enumerate(sentences):
        engine.say(sentence)
        engine.runAndWait()
        sentence_audio = AudioSegment.empty()
        if i < len(sentences) - 1:
            pause_duration = pause_durations[i]
            if pause_duration > 0:
                silence_segment = AudioSegment.silent(duration=pause_duration)
                sentence_audio += silence_segment
        audio += sentence_audio

    output_file = "final_audio_with_pauses.mp3"
    audio.export(output_file, format="mp3")

    if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
        print("Audio exported successfully.")
    else:
        print("Error exporting audio.")

    return sentences, pause_durations

# Example usage
text = """The challenges have forged our skills, and we're thrilled to share the fruits of our labor. PAUSE 100 Our latest creation is a testament to the passion and dedication that drives us. PAUSE 1000 Stay tuned as we unveil more updates and behind-the-scenes glimpses. Thank you for joining us on this incredible adventure."""
sentences, pause_durations = speak_with_pauses(text)

print("Sentences:", sentences)
print("Pause Durations (ms):", pause_durations)
