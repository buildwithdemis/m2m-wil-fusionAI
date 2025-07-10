from deepgram import Deepgram
from google.cloud import texttospeech
import os
import base64
from dotenv import load_dotenv
import websockets
import json

load_dotenv()
deepgram = Deepgram(os.getenv("DEEPGRAM_API_KEY"))
tts_client = texttospeech.TextToSpeechClient()
'''
async def process_audio(audio_chunk: str) -> str:
    audio_data = base64.b64decode(audio_chunk)
    response = await deepgram.transcription.live(audio_data)
    return response.get("transcript", "")
'''
async def process_audio(audio_chunk: str) -> str:
    try:
        audio_data = base64.b64decode(audio_chunk)
        async with websockets.connect(
            "wss://api.deepgram.com/v1/listen",
            extra_headers={"Authorization": f"Token {os.getenv('DEEPGRAM_API_KEY')}"}
        ) as ws:
            await ws.send(audio_data)
            response = await ws.recv()
            return json.loads(response).get("channel", {}).get("alternatives", [{}])[0].get("transcript", "")
    except Exception as e:
        print(f"Error in process_audio: {e}")
        return ""

async def text_to_speech(text: str) -> str:
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Wavenet-D"
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )
    response = tts_client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    return base64.b64encode(response.audio_content).decode("utf-8")

