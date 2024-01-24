import os
import sys
from functools import partial

import numpy as np
import openai
import sounddevice as sd
from dotenv import load_dotenv
from pynput.keyboard import Controller as KeyboardController
from pynput.keyboard import Key, Listener
from scipy.io import wavfile

from wkey.utils import process_transcript
from wkey.whisper import apply_whisper

load_dotenv()
key_label = os.environ.get("WKEY", "ctrl_r")
RECORD_KEY = Key[key_label]

# This flag determines when to record
recording = False

# This is where we'll store the audio
audio_data = []

# This is the sample rate for the audio
sample_rate = 16000

# Keyboard controller
keyboard_controller = KeyboardController()


def on_press(key):
    global recording
    global audio_data

    if key == RECORD_KEY:
        recording = True
        audio_data = []
        print("Listening...")


def on_release(key, model="cpp"):
    global recording
    global audio_data

    if model not in ("cpp", "api"):
        raise ValueError(f"Invalid mode: {model}")

    if key == RECORD_KEY:
        recording = False
        print("Transcribing...")

        try:
            audio_data_np = np.concatenate(audio_data, axis=0)
        except ValueError as e:
            print(e)
            return

        audio_data_int16 = (audio_data_np * np.iinfo(np.int16).max).astype(np.int16)
        wavfile.write("recording.wav", sample_rate, audio_data_int16)

        transcript = None
        try:
            transcript = apply_whisper("recording.wav", "transcribe")
        except openai.error.InvalidRequestError as e:
            print(e)

        if transcript:
            processed_transcript = process_transcript(transcript)
            print(processed_transcript)
            keyboard_controller.type(processed_transcript)


def callback(indata, frames, time, status):
    if status:
        print(status)
    if recording:
        audio_data.append(indata.copy())  # make sure to copy the indata


def main():
    api = "--api" in sys.argv
    # Setup partial function depending on sys arg.
    on_release_partial = partial(on_release, model="api" if api else "cpp")

    print(
        f"wkey is active using model{' (API)' if api else 'CPP'}"
        f". Hold down {key_label} to start dictating."
    )
    with Listener(on_press=on_press, on_release=on_release_partial) as listener:
        # This is the stream callback
        with sd.InputStream(callback=callback, channels=1, samplerate=sample_rate):
            # Just keep the script running
            listener.join()


if __name__ == "__main__":
    main()
