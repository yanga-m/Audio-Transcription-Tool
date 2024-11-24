# Audio Transcription Tool

This project provides a streamlined approach to transcribing audio files using **AssemblyAI's API**. It automates the upload, transcription, and result-saving processes, making it easy to convert speech into text with minimal setup.

---

## Project Overview

The project automates the transcription of audio files into text by:
1. Uploading an audio file to AssemblyAI's API.
2. Polling the API to track transcription progress.
3. Saving the transcription as a `.txt` file.

---

## Project Structure

### Files and Directories:
- **`api_communications.py`**: Handles all interactions with AssemblyAI's API, including:
  - Uploading audio files.
  - Initiating transcription requests.
  - Polling the transcription status.
  - Saving the final transcription to a file.
- **`api_secrets.py`**: Stores the AssemblyAI API key for authentication.
- **`main.py`**: The main script to execute the transcription process. Includes options for running sentiment analysis or topic classification.
- **`analysis_tools.py`**: Contains tools for sentiment analysis and topic classification using the transcription.
- **`README.md`**: Documentation for the project.

---

## Requirements

- **Python 3.x**  
- Required libraries:
  - `requests`
  - `transformers`
  - `matplotlib`
  - `scikit-learn`

---

## Installation

To install the required dependencies, run:

```bash
pip install requests transformers matplotlib scikit-learn
```

---

## Setup

1. **Get an AssemblyAI API Key**:  
   - Sign up at [AssemblyAI](https://www.assemblyai.com/) and obtain your API key.

2. **Store the API Key**:  
   - Open `api_secrets.py` and replace the placeholder with your API key:  
     ```python
     API_KEY_ASSEMBLYAI = "your_assemblyai_api_key_here"
     ```

---

## Usage

### Transcription
1. Place your audio file (e.g., `audio.wav`) in the project directory.
2. Run the transcription process from the command line:
   ```bash
   python main.py <mode> <filename>
   ```
   Replace `<mode>` with one of the following:
   - `sentiment`: Perform sentiment analysis on the transcription.
   - `topic`: Classify the transcription's content into topics.

   Replace `<filename>` with the name of your audio file.

---

## Features

1. **Audio Transcription**: Converts speech in audio files to text using AssemblyAI's API.
2. **Sentiment Analysis**:
   - Uses a sentiment analysis pipeline to assess emotional tone (positive, neutral, or negative).
   - Visualizes sentiment distribution in a bar chart.
3. **Topic Classification**:
   - Classifies text into predefined topics (e.g., Technology, Health, Business).
   - Includes an "Other" category for sentences that don't fit into predefined topics.
   - Visualizes topic distribution in a pie chart.

---

## Error Handling

- If an error occurs during transcription (e.g., invalid file, API issues), the script will:
  - Print a clear error message.
  - Stop further processing to avoid incomplete results.

---

## Example

### Transcription Example
For an audio file named `audio.wav`, running:
```bash
python main.py sentiment audio.wav
```
will:
1. Upload the file to AssemblyAI.
2. Transcribe the audio.
3. Save the transcription in `audio.txt`.
4. Perform sentiment analysis and save a bar chart as `sentiment_analysis.png`.

---

## Additional Notes

- Ensure your audio files are in a supported format (e.g., `.wav`, `.mp3`).
- Keep your API key secure. Avoid sharing or exposing it in public repositories.
