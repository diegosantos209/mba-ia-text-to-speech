
import os
from pathlib import Path
from dotenv import load_dotenv
import openai
import asyncio

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = api_key

with open("texto.txt", "r", encoding="utf-8") as file:
    text_content = file.read()

async def textTranslate():
  response = openai.chat.completions.create(
    model="gpt-4o-mini",
    messages=[       
      {"role": "user", "content": f"Traduza somente o texto para inglês: {text_content} "}
    ],
    stream= False
  )
  message = response.choices[0].message.content
  
  with open("texto_traduzido.txt", "w", encoding="utf-8") as file:
        file.write(message)
        
  return message
  
async def textToSpeech():
  message = await textTranslate()  
  with openai.audio.speech.with_streaming_response.create(
    model="tts-1",
    voice="alloy",
    input=message,
  ) as response:   
      response.stream_to_file("speecht.mp3")
      
def speechToText():
    with open("speechtotext.mp3", "rb") as audio_file:
        transcription = openai.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
    
    audioToText = transcription.text
    
    with open("audioToText.txt", "w", encoding="utf-8") as text_file:
        text_file.write(audioToText)
  
async def main():
  await textToSpeech()
  speechToText()
  
if __name__ == "__main__":
  asyncio.run(main())
