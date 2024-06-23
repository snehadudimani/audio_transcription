import speech_recognition as sr
from pydub import AudioSegment

def transcribe_audio(file_path: str) -> str:
    # Convert MP3 to WAV if file is MP3
    if file_path.lower().endswith('.mp3'):
        audio = AudioSegment.from_mp3(file_path)
        wav_file_path = file_path[:-4] + '.wav'  # Change extension to WAV
        audio.export(wav_file_path, format='wav')
        file_path = wav_file_path

    # Transcribe the audio file
    recognizer = sr.Recognizer()
    audio_file = sr.AudioFile(file_path)

    with audio_file as source:
        audio_data = recognizer.record(source)

    try:
        transcription = recognizer.recognize_google(audio_data)
        return transcription
    except Exception as e:
        raise Exception(f"Transcription failed: {str(e)}")
