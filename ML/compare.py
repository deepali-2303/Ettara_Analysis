import pandas as pd
from nltk.sentiment import SentimentIntensityAnalyzer
import streamlit as st
import matplotlib.pyplot as plt

# Load data and perform sentiment analysis (use your actual data paths)
cafe_files = ['./data/dibella_clean.csv', './data/tim_clean.csv', './data/review_zom_clean.csv']
# cafe_dfs = [pd.read_csv(file_path) for file_path in cafe_files]
selected_files = st.multiselect('Select cafe files:', cafe_files)

# Display selected files
if selected_files:

    # Create a DataFrame with selected files
    cafe_toselect = [pd.read_csv(file_path) for file_path in selected_files]

    sia = SentimentIntensityAnalyzer()

    word_sentiments = {'ambience': [], 'service': [], 'food': [], 'clean':[], 'quality':[], 'time':[],
                    'hospitality':[], 'delivery':[], 'packaging':[], 'wrong order':[], 'stale':[],}

    for i, cafe_df in enumerate(cafe_toselect):
        cafe_df['Sentiment'] = cafe_df['lemma_str'].apply(lambda x: sia.polarity_scores(x)['compound'])

        for word in word_sentiments.keys():
            word_reviews = cafe_df['lemma_str'].apply(lambda x: word in x.lower())
            word_sentiment = cafe_df.loc[word_reviews, 'Sentiment'].mean()
            word_sentiments[word].append(word_sentiment)

    # Streamlit app
    st.title("Cafe Sentiment Analysis")

    # Select a word for sentiment analysis
    selected_word = st.selectbox("Select a word for sentiment analysis", list(word_sentiments.keys()))

    # Plot sentiment scores for the selected word
    plt.figure(figsize=(8, 4))
    plt.bar(range(1, len(word_sentiments[selected_word]) + 1), word_sentiments[selected_word])
    plt.xlabel('Cafe')
    plt.ylabel('Avg Sentiment')
    plt.title(f"Avg Sentiment for '{selected_word}' Across Cafes")
    plt.xticks(range(1, len(word_sentiments[selected_word]) + 1), [f'Cafe {i + 1}' for i in range(len(word_sentiments[selected_word]))])
    st.pyplot(plt)
