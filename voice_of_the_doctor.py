import os
import time
import wave

from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai.errors import ServerError


load_dotenv()


client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def generate_doctor_voice(
    doctor_text,
    language,
    audio_file="doctor_voice.wav"
):

    response = None

    for attempt in range(5):

        try:

            print(
                f"\nGenerating doctor voice (Attempt {attempt + 1}/5)..."
            )

            if language == "English 🇺🇸":
                voice_name = "Charon"

            elif language == "हिन्दी 🇮🇳":
                voice_name = "Charon"

            else:
                voice_name = "Charon"

            response = client.models.generate_content(
                model="gemini-2.5-flash-preview-tts",

                contents=doctor_text,

                config=types.GenerateContentConfig(
                    response_modalities=[
                        "AUDIO"
                    ],

                    speech_config=types.SpeechConfig(
                        voice_config=types.VoiceConfig(
                            prebuilt_voice_config=types.PrebuiltVoiceConfig(
                                voice_name=voice_name
                            )
                        )
                    )
                )
            )

            print("Doctor voice generated.")
            break

        except ServerError as e:

            print(f"\nServer busy: {e}")

            if attempt == 4:
                raise

            print("Retrying in 10 seconds...")
            time.sleep(10)

    audio_data = (
        response
        .candidates[0]
        .content
        .parts[0]
        .inline_data
        .data
    )

    with wave.open(audio_file, "wb") as wav_file:

        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(24000)

        wav_file.writeframes(audio_data)

    return audio_file