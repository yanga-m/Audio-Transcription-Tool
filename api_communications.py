import requests
from api_secrets import API_KEY_ASSEMBLYAI
import time

# Define the endpoints for uploading audio and requesting transcription
UPLOAD_ENDPOINT = "https://api.assemblyai.com/v2/upload"
TRANSCRIPT_ENDPOINT = "https://api.assemblyai.com/v2/transcript"

# Headers for authentication using the AssemblyAI API key
HEADERS = {'authorization': API_KEY_ASSEMBLYAI}


# Function to upload an audio file to AssemblyAI
def upload(filename):
    """
    Uploads an audio file to AssemblyAI and returns the generated audio URL.

    :param filename: Path to the audio file to be uploaded.
    :return: URL of the uploaded audio file.
    """

    def read_file(filename, chunk_size=5242880):
        """
        Reads the file in chunks to handle large files.

        :param filename: Path to the file.
        :param chunk_size: Size of chunks to read the file in bytes.
        :yield: File data in chunks.
        """
        with open(filename, 'rb') as _file:
            while True:
                data = _file.read(chunk_size)
                if not data:
                    break
                yield data

    # Send the file data to the upload endpoint
    upload_response = requests.post(UPLOAD_ENDPOINT, headers=HEADERS, data=read_file(filename))

    # Extract and return the URL of the uploaded audio
    audio_url = upload_response.json().get('upload_url')
    return audio_url


# Function to initiate transcription of the uploaded audio
def transcribe(audio_url):
    """
    Requests transcription for the uploaded audio file.

    :param audio_url: URL of the uploaded audio file.
    :return: ID of the transcription job.
    """
    transcript_request = {"audio_url": audio_url}
    transcript_response = requests.post(TRANSCRIPT_ENDPOINT, json=transcript_request, headers=HEADERS)

    # Extract and return the transcription job ID
    job_id = transcript_response.json().get('id')
    return job_id


# Function to poll the transcription status
def poll(transcript_id):
    """
    Polls the transcription job status.

    :param transcript_id: ID of the transcription job.
    :return: JSON response containing the job's status and details.
    """
    polling_endpoint = f"{TRANSCRIPT_ENDPOINT}/{transcript_id}"
    polling_response = requests.get(polling_endpoint, headers=HEADERS)
    return polling_response.json()


# Function to get the final transcription result
def get_transcription_result_url(audio_url):
    """
    Waits for the transcription to complete and fetches the result.

    :param audio_url: URL of the uploaded audio file.
    :return: Transcription data and error (if any).
    """
    transcript_id = transcribe(audio_url)
    while True:
        # Poll for transcription status
        data = poll(transcript_id)
        if data['status'] == 'completed':
            # Return the transcription result if completed
            return data, None
        elif data['status'] == 'error':
            # Return the error message if an error occurred
            return data, data['error']

        # Wait before polling again
        print('Waiting 30 seconds...')
        time.sleep(30)


# Function to save the transcription to a file
def save_transcript(audio_url, filename):
    """
    Saves the transcription of an audio file to a text file.

    :param audio_url: URL of the uploaded audio file.
    :param filename: Base filename to save the transcription.
    """
    data, error = get_transcription_result_url(audio_url)

    if data:
        # Write the transcription text to a file
        text_filename = f"{filename}.txt"
        with open(text_filename, "w") as f:
            f.write(data['text'])
        print('Transcription saved!')
    elif error:
        # Print the error if the transcription failed
        print("Error!!", error)
