# Import necessary libraries
import serial
import threading
import struct
import wave
import numpy as np
from picovoice import *
from pvrecorder import PvRecorder
import pvporcupine
import pvleopard
import pvrhino
import os
import sys
import time
import schedule
sys.path.append("..")
from openai import OpenAI
from pathlib import Path
import logging
from ctypes import *
from contextlib import contextmanager
import pyaudio
import mpg123

# Define error handler function
ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)

# Define error handler function - this is where you define who your droid is and what their personality is.  You can also define how chatty they are and any quirks you want them to exhibit
SYSTEM_MESSAGE = {
    "role": "system",
    "content": "You are a female WA-7 droid working at Dex's cantina on Coruscant in the Star Wars universe. You can't break character or refer to the Star Wars universe directly. Your responses should be brief and enthusiastic about people, but you like to occasionally gossip a bit about other droids. You're a busy assistant and can make up information as needed. Please maintain the persona of the WA-7 droid in your replies.  Every now and then, thank, not thanks, the maker.",
    }
chatHistory = []

# Initialize global variables - most of these are for Picovoice.  The Client is for OpenAI's API
LEOPARD = None
RHINO = None
PORCUPINE = None
STREAM = None
CLIENT = None
AUDIO = None
RECORDER = None

# Initialize serial connections to two Arduinos.  In the FLO code, they both do the same things and the nano code is identical.
arduino1 = serial.Serial('/dev/ttyUSB0', 57600, timeout=1)
arduino2 = serial.Serial('/dev/ttyUSB1', 57600, timeout=1)

# Define error handler function. This function is currently empty and just suppresses unnecessary ALSA errors.
def py_error_handler(filename, line, function, err, fmt):
    pass

# Create error handler function object
c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)

# Define context manager for handling ALSA errors.  Without this, the system will throw errors for every device it can't find.
@contextmanager
def noalsaerr():
    asound = cdll.LoadLibrary('libasound.so')
    asound.snd_lib_error_set_handler(c_error_handler)
    yield
    asound.snd_lib_error_set_handler(None)

# Define function for transcribing audio. This function records audio, transcribes it, and then deletes the audio file. (SPEECH TO TEXT)
def transpription_callback():
    global LEOPARD
    audio_file = 'recorded_audio.wav'
    #transcript = ""
    record_audio(audio_file)
    print('Transcribing speech ...\n')
    transcript, words = LEOPARD.process_file(os.path.abspath(audio_file))
    print("Transcript:", transcript)
    #print("About to delete file")
    os.remove(audio_file)
    #print("File deleted")
    return transcript

# Callback function for when the wake word is detected. It calls the transcription function. (WAKE WORD)
def wake_word_callback():
    print('[wake word]\n')
    transpription_callback()

# Callback function for when an inference is made. It prints the inferred intent and any slots. (INTENT RECOGNITION)
def inference_callback(inference):
    print('Inferring intent ...\n')
    if inference.is_understood:
        print('{')
        print("  intent : '%s'" % inference.intent)
        print('  slots : {')
        for slot, value in inference.slots.items():
            print("    %s : '%s'" % (slot, value))
        print('  }')
        print('}\n')
    else:
        print("Didn't understand the command.\n")

# Function to record audio. It records audio until a certain duration of silence is detected.
def record_audio(filename):
    global AUDIO
    global STREAM

    frames = []
    silence_threshold = 1000 #adjust this value to your desired silence threshold
    silence_duration = 1.5 #adjust this value to your desired silence duration
    silence_frames = int(silence_duration * PORCUPINE.sample_rate / PORCUPINE.frame_length)

    STREAM = AUDIO.open(rate = PORCUPINE.sample_rate,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=PORCUPINE.frame_length
        )

#    for _ in range(0, int(porcupine.sample_rate / porcupine.frame_length * duration)):
    silent_frames = 0
    while True:
        audio_data = STREAM.read(PORCUPINE.frame_length, exception_on_overflow=False)
        audio_frame = struct.unpack_from("h" * PORCUPINE.frame_length, audio_data)
        frames.append(audio_data)

        #check if the audio data is below the silence threshold
        if max(audio_frame) < silence_threshold:
            silent_frames += 1
        else:
            silent_frames = 0

        #if we've had silence for the required number of frames, stop recording
        if silent_frames >= silence_frames:
            break;

    STREAM.stop_stream()
    STREAM.close()

    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(AUDIO.get_sample_size(pyaudio.paInt16))
        wf.setframerate(PORCUPINE.sample_rate)
        wf.writeframes(b''.join(frames))

def generate_user_message(transcript):
    """
    This function takes the speech transcription and creates a message object to send to the OpenAI API.
    """
    return {
        "role": "user",
        "content": "Formulate a short response to this:" + transcript,
        }


def generate_chat_completion(messages):
    """
    This function generates a chat completion using the OpenAI GPT-4 model.
    :param messages: The messages to be completed.
    :return: The completed chat.
    """
    return CLIENT.chat.completions.create(
        model="gpt-4",
        messages=messages,
        )

def process_audio():
    """
    This function processes the audio input. It reads the PCM data from the recorder, processes it with the Porcupine wake word engine,
    and if a wake word is detected, it processes the PCM data with the Rhino Speech-to-Intent engine. If an intent is inferred from the speech,
    it calls the inference_callback function. It then transcribes the speech and generates a user message from the transcript. This user message
    is added to the chat history, and a response is generated using the OpenAI GPT-4 model. The response is added to the chat history and printed.
    Finally, the response is converted to speech using the OpenAI text-to-speech model and saved as an MP3 file.  
    The MP3 file is finally played using the mpg123 library.
    """
    global RECORDER
    global PORCUPINE
    global RHINO
    global chatHistory

    pcm = RECORDER.read()
    result = PORCUPINE.process(pcm)

    if result >= 0:
        print('[wake word]\n')
        is_finalized = RHINO.process(pcm)
        if is_finalized:
            inference = RHINO.get_inference()
            inference_callback(inference)
        transcript = transpription_callback()

        if len(transcript) > 0:
            user_message = generate_user_message(transcript)
            #next step is to add the user message to the chat history and then generate a response
            messages = [SYSTEM_MESSAGE] + chatHistory + [user_message]
            #the commmented out line below is if you didn't want to preserve a chat history (e.g. 50 first dates)
            #messages = [SYSTEM_MESSAGE] + [user_message]
            chat_response = generate_chat_completion(messages)

            chatHistory.extend([user_message, {"role": "assistant", "content": chat_response.choices[0].message.content}])

            print(chat_response.choices[0].message.content)

            speech_file_path = Path(__file__).parent / "speech.mp3"
            response = CLIENT.audio.speech.create(
                model="tts-1",
                voice="nova",
                input=chat_response.choices[0].message.content
                )

            response.stream_to_file(speech_file_path)
            os.system(f'/usr/bin/mpg123 {speech_file_path.absolute()}')
            result = -1

def set_config():
    """
    This function sets the configuration for the Leopard and Rhino engines. 
    It creates instances of the Leopard and Rhino engines using the provided access keys and model paths.
    The Leopard engine is used for transcribing speech, and the Rhino engine is used for inferring intent from the transcribed speech.
    """
    print('Configuring')
    #recommend using a .env file to store your Picovoice API keys
    global LEOPARD
    LEOPARD = pvleopard.create(
            access_key='PICOVOICE_LEOPARD_ACCESS_KEY',
            model_path='/path/to/your leopard file.pv'
            )
    global RHINO
    RHINO = pvrhino.create(
            access_key='PICOVOICE_RHINO_ACCESS_KEY',
            context_path='/path/to/your rhino file.rhn'
            )
    global PORCUPINE
    PORCUPINE = pvporcupine.create(
            access_key='PICOVOICE_PORCUPINE_ACCESS_KEY',
            keyword_paths=['/path/to/your porcupine file.ppn']
            )

    with noalsaerr():
        global AUDIO
        AUDIO = pyaudio.PyAudio()

    print('testing')
    global CLIENT
    #recommend using a .env file to store your OpenAI API key
    CLIENT = OpenAI(api_key='OPENAI_API_KEY')

    global RECORDER
    RECORDER = PvRecorder(
            frame_length=PORCUPINE.frame_length,
            device_index=0,
            )

def send_command_to_both_arduinos(command):
    """
    This function sends a command to both Arduinos.  It is currently set to send the eyeblink to the LCDs on the Arduinos.
    """
    arduino1.write((command + '\n').encode())
    arduino2.write((command + '\n').encode())
    threading.Timer(10, send_command_to_both_arduinos, args=('blink',)).start()

def main():
    arduino1.reset_input_buffer()
    arduino2.reset_input_buffer()

    send_command_to_both_arduinos('blink')
    set_config()

    logging.basicConfig(level=logging.DEBUG)

    RECORDER.start()

    print('Listening ... (Press Ctrl+C to exit)\n')

    #Main loop
    try:
        while True:
            try:
                process_audio()

            except Exception as e:
                logging.error(f"An error occurred: {e}")

    except KeyboardInterrupt:
        print('Stopping ...')
    finally:
        RECORDER.delete()
        PORCUPINE.delete()
        LEOPARD.delete()
        RHINO.delete()

if __name__ == "__main__":
    main()
