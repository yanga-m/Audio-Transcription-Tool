from transformers import pipeline
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import re

# Initialize the sentiment analysis pipeline
sentiment_analyzer = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")

def clean_text(text):
    """
    Clean and preprocess the input text for analysis.

    :param text: Raw text input.
    :return: Cleaned text.
    """
    # Remove special characters, numbers, and extra whitespace
    text = re.sub(r'[^a-zA-Z\s]', '', text)  # Keep only letters and spaces
    text = re.sub(r'\s+', ' ', text).strip()  # Remove extra spaces
    text = text.lower()  # Convert to lowercase
    return text

def analyze_sentiment(text):
    """
    Analyze sentiment for each sentence in the text.

    :param text: The transcription text to analyze.
    :return: List of sentiment results.
    """
    cleaned_text = text  # Clean the text before analysis
    sentences = cleaned_text.split('.')
    results = []
    for sentence in sentences:
        if sentence.strip():
            result = sentiment_analyzer(sentence.strip())
            results.append(result[0])  # Append first result
    return results

def visualize_sentiment(sentiment_results, filename="sentiment_analysis.png"):
    """
    Visualize sentiment analysis results as a bar chart and save it as an image.

    :param sentiment_results: List of dictionaries containing sentiment analysis results.
    :param filename: Name of the file to save the image (default is 'sentiment_analysis.png').
    """
    sentiments = [res.get('label', 'unknown') for res in sentiment_results if isinstance(res, dict)]
    sentiment_counts = {label: sentiments.count(label) for label in set(sentiments)}

    plt.figure(figsize=(10, 6))
    plt.bar(sentiment_counts.keys(), sentiment_counts.values(), color=['green', 'red', 'blue'])
    plt.xlabel('Sentiment')
    plt.ylabel('Count')
    plt.title('Sentiment Analysis Results')

    # Save the figure as an image
    plt.savefig(filename)
    print(f"Sentiment analysis bar chart saved as {filename}.")
    plt.show()

def classify_topics_with_other(text):
    """
    Classify topics in the text and include an 'Other' category.

    :param text: The transcription text to classify.
    :return: Tuple containing topics, percentages, and sentences per topic.
    """
    cleaned_text = text  # Clean the text before analysis
    vectorizer = CountVectorizer(stop_words='english')
    X = vectorizer.fit_transform([cleaned_text])

    # Extended predefined topic labels
    predefined_labels = [
        'Technology', 'Health', 'Education', 'Business', 'Environment',
        'Sports', 'Politics', 'Entertainment', 'Science', 'Finance', 'Travel'
    ]

    lda = LatentDirichletAllocation(n_components=len(predefined_labels), random_state=42)
    lda.fit(X)

    words = vectorizer.get_feature_names_out()
    topics = {label: [] for label in predefined_labels}

    # Map top words to each topic
    for topic_idx, topic in enumerate(lda.components_):
        top_words = [words[i] for i in topic.argsort()[:-6:-1]]
        topics[predefined_labels[topic_idx]] = top_words

    # Classify sentences
    sentences = cleaned_text.split('.')
    topic_counts = {label: 0 for label in predefined_labels + ['Other']}
    classified_sentences = []

    for sentence in sentences:
        if not sentence.strip():
            continue
        matched = False
        for topic, words in topics.items():
            if any(word in sentence.lower() for word in words):
                topic_counts[topic] += 1
                classified_sentences.append((sentence.strip(), topic))
                matched = True
                break
        if not matched:
            topic_counts['Other'] += 1
            classified_sentences.append((sentence.strip(), 'Other'))

    # Calculate percentages and remove topics with zero counts
    total_sentences = sum(topic_counts.values())
    percentages = {key: (value / total_sentences) * 100 for key, value in topic_counts.items() if value > 0}

    # Filter out topics that are not present
    topics = {k: v for k, v in topics.items() if topic_counts[k] > 0}

    return topics, percentages, classified_sentences

def visualize_topic_distribution(percentages, filename="topic_classification.png"):
    """
    Visualize topic classification percentages as a pie chart and save as an image.

    :param percentages: Dictionary with topic names and their percentages.
    :param filename: Name of the file to save the pie chart (default is 'topic_classification.png').
    """
    labels = list(percentages.keys())
    sizes = list(percentages.values())

    # Updated color palette for more vibrant and distinct colors
    color_palette = [
        'skyblue', 'lightgreen', 'coral', 'gold', 'violet', 'mediumseagreen',
        'lightcoral', 'slateblue', 'lightpink', 'mediumslateblue', 'mediumturquoise'
    ]
    colors = color_palette[:len(labels)]  # Match colors to the number of labels

    plt.figure(figsize=(8, 8))
    wedges, texts, autotexts = plt.pie(
        sizes,
        labels=labels,
        autopct='%1.1f%%',
        startangle=140,
        colors=colors,
        textprops=dict(color="black"),
    )

    # Improve text size and layout
    for text in texts:
        text.set_fontsize(10)  # Smaller font size for labels
    for autotext in autotexts:
        autotext.set_fontsize(10)  # Smaller font size for percentages

    plt.title('Topic Classification', fontsize=14, pad=20)  # Add padding to the title
    plt.axis('equal')  # Ensure the pie is a circle

    # Adjust layout to prevent overlap
    plt.tight_layout()

    # Save the image
    plt.savefig(filename, bbox_inches="tight")
    print(f"Topic classification pie chart saved as {filename}.")
    plt.show()








