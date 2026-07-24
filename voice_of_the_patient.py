try:
    import sounddevice as sd
    import soundfile as sf
    SOUND_AVAILABLE = True
except Exception:
    SOUND_AVAILABLE = False

import speech_recognition as sr

def record_patient_voice(
    language,
    audio_file="patient_voice.wav",
    duration=5
):

    if not SOUND_AVAILABLE:
        return "Voice input is not available on this server."

    sample_rate = 44100

    print("Patient: Speak now...")

    audio = sd.rec(
        int(duration * sample_rate),
        samplerate=sample_rate,
        channels=1,
        dtype="int16"
    )

    sd.wait()

    sf.write(
        audio_file,
        audio,
        sample_rate
    )

    print("Audio saved:", audio_file)


    recognizer = sr.Recognizer()


    with sr.AudioFile(audio_file) as source:

        audio_data = recognizer.record(source)


    try:

        if language == "English 🇺🇸":
            speech_language = "en-US"

        elif language == "हिन्दी 🇮🇳":
            speech_language = "hi-IN"

        else:
            speech_language = "bn-IN"

        patient_text = recognizer.recognize_google(
            audio_data,
            language=speech_language
        )

        return patient_text


    except sr.UnknownValueError:

        return "Could not understand audio"


    except sr.RequestError:

        return "Speech recognition service unavailable"