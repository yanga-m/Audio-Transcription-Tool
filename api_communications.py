import requests
import time
from api_secrets import API_KEY_ASSEMBLYAI

# Endpoints and headers for AssemblyAI API
UPLOAD_ENDPOINT = "https://api.assemblyai.com/v2/upload"
TRANSCRIPT_ENDPOINT = "https://api.assemblyai.com/v2/transcript"
HEADERS = {'authorization': API_KEY_ASSEMBLYAI}


def upload(filename):
    """
    Upload an audio file to AssemblyAI.

    :param filename: Path to the audio file to upload.
    :return: URL of the uploaded audio file.
    """

    def read_file(filename, chunk_size=5242880):
        with open(filename, 'rb') as _file:
            while True:
                data = _file.read(chunk_size)
                if not data:
                    break
                yield data

    response = requests.post(UPLOAD_ENDPOINT, headers=HEADERS, data=read_file(filename))
    return response.json().get('upload_url')


def transcribe(audio_url):
    """
    Request transcription for the uploaded audio file.

    :param audio_url: URL of the uploaded audio file.
    :return: ID of the transcription job.
    """
    transcript_request = {"audio_url": audio_url}
    response = requests.post(TRANSCRIPT_ENDPOINT, json=transcript_request, headers=HEADERS)
    return response.json().get('id')


def poll(transcript_id):
    """
    Poll the transcription job status.

    :param transcript_id: ID of the transcription job.
    :return: JSON response containing the status and details.
    """
    polling_endpoint = f"{TRANSCRIPT_ENDPOINT}/{transcript_id}"
    return requests.get(polling_endpoint, headers=HEADERS).json()


def save_transcript(audio_url, filename):
    """
    Save the transcription of an audio file to a text file.

    :param audio_url: URL of the uploaded audio file.
    :param filename: Base filename to save transcription.
    :return: Transcription data and error (if any).
    """
    transcript_id = transcribe(audio_url)
    while True:
        data = poll(transcript_id)
        if data['status'] == 'completed':
            text_filename = f"{filename}.txt"
            with open(text_filename, "w") as f:
                f.write(data['text'])
            print(f"Transcription saved to {text_filename}")
            return data, None
        elif data['status'] == 'error':
            return None, data['error']
        time.sleep(30)
