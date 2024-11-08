# Audio Transcription Project

This project provides an automated way to transcribe audio files using AssemblyAI's transcription API. It takes an audio file as input, uploads it to AssemblyAI, retrieves the transcription once processing is complete, and saves the transcript as a .txt file.

## Project Structure

- api_communication.py: Handles all communication with AssemblyAI's API, including uploading audio, requesting transcription, polling for transcription status, and saving the final transcription.
- api_secrets.py: Contains the API key required to authenticate requests to AssemblyAI's API.
- main.py: Main script that initiates the transcription process by taking an audio filename as input, uploading it, and saving the transcription.
- README.md: Documentation for the project.

Requirements:

Python 3.x
requests library to handle HTTP requests.
Installation
To install the required dependencies, run:

### pip install requests

## Setup
1.Get an AssemblyAI API Key:

2.Sign up at AssemblyAI and obtain an API key.

3.Store API Key:
Open api_secrets.py and set the API_KEY_ASSEMBLYAI variable with your API key.
Example:

### API_KEY_ASSEMBLYAI = "your_assemblyai_api_key_here"

## Usage
Place your audio file (e.g., audio.wav) in the project directory.
Run the transcription process from the command line as follows:

### python main.py audio.wav
Here, replace audio.wav with the name of your audio file.

The script will:

1.Upload the audio file to AssemblyAI.

2.Poll the API until the transcription is complete.

3.Save the transcription as a .txt file with the same name as the audio file.

Example
For an audio file named audio.wav, running:

### python main.py audio.wav
will create audio.txt containing the transcription.

## Files

api_communication.py: Contains the following functions:
- upload(filename): Uploads an audio file to AssemblyAI and returns the URL.
- transcribe(audio_url): Initiates transcription and returns a job ID.
- poll(transcript_id): Polls for the transcription status.
- get_transcription_result_url(audio_url): Manages transcription and returns the final result.
- save_transcript(audio_url, filename): Saves the transcription to a text file.
- api_secrets.py: Contains the API key (API_KEY_ASSEMBLYAI) required for authorization.
- main.py: Takes an audio filename as a command-line argument, uploads it, and saves the transcription.
Error Handling

If an error occurs during transcription, the script will display an error message.# Simple-Speech-Recognition
