import sys
from api_communications import *

# Get the filename of the audio file from command-line arguments
filename = sys.argv[1]

# Upload the file and get the audio URL
audio_url = upload(filename)

# Save the transcription of the audio to a text file
save_transcript(audio_url, filename)
