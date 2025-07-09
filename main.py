from fastapi import FastAPI, WebSocket
from twilio.twiml.voice_response import VoiceResponse, Connect, Stream
import os
from dotenv import load_dotenv
from audio_processor import process_audio
from orchestrator import handle_conversation

load_dotenv()
app = FastAPI()

@app.get("/voice")
async def voice_webhook():
    response = VoiceResponse()
    connect = Connect()
    connect.stream(url=f"wss://{os.getenv('SERVER_HOST', 'voice-ai-agent-xxx.a.run.app')}/twilio-websocket")
    response.append(connect)
    return str(response)

@app.websocket("/twilio-websocket")
async def twilio_websocket(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()
            if data["event"] == "media":
                audio_chunk = data["media"]["payload"]
                transcription = await process_audio(audio_chunk)
                response_text = await handle_conversation(transcription)
                audio_response = await text_to_speech(response_text)
                await websocket.send_json({"event": "media", "media": {"payload": audio_response}})
            elif data["event"] == "stop":
                break
    except Exception as e:
        print(f"WebSocket error: {e}")
    await websocket.close()