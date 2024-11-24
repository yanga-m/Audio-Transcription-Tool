import sys
from analysis_tools import (
    analyze_sentiment,
    visualize_sentiment,
    classify_topics_with_other,
    visualize_topic_distribution
)
from api_communications import upload, save_transcript


def run_sentiment_analysis(audio_url, filename):
    """
    Perform sentiment analysis and visualize results.
    """
    # Save transcription
    transcription_data, error = save_transcript(audio_url, filename)

    if error:
        print(f"Transcription error: {error}")
        return

    # Get the transcribed text
    transcription_text = transcription_data['text']

    # Analyze sentiment
    sentiment_results = analyze_sentiment(transcription_text)
    visualize_sentiment(sentiment_results, filename="sentiment_analysis.png")


def run_topic_classification(audio_url, filename):
    """
    Perform topic classification and visualize results.
    """
    # Save transcription
    transcription_data, error = save_transcript(audio_url, filename)

    if error:
        print(f"Transcription error: {error}")
        return

    # Get the transcribed text
    transcription_text = transcription_data['text']

    # Classify topics
    topics, percentages, _ = classify_topics_with_other(transcription_text)
    visualize_topic_distribution(percentages, filename="topic_classification.png")

    print("\nIdentified Topics and their Key Words:")
    for topic, words in topics.items():
        print(f"{topic}: {', '.join(words)}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python main.py <mode> <filename>")
        print("<mode> can be 'sentiment' or 'topic'")
        sys.exit(1)

    mode = sys.argv[1].lower()
    filename = sys.argv[2]

    # Upload the file and get the audio URL
    audio_url = upload(filename)

    # Run the chosen mode
    if mode == "sentiment":
        run_sentiment_analysis(audio_url, filename)
    elif mode == "topic":
        run_topic_classification(audio_url, filename)
    else:
        print(f"Invalid mode: {mode}. Choose 'sentiment' or 'topic'.")
