import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load word frequency results
word_frequency_df = pd.read_csv('word_frequency_results.csv')
df = pd.read_csv('review.csv')

# Get user input (query)
user_query = "The coffee was bad"  # Replace this with actual user input

# Assuming 'review' is the column containing the text in your dataset
reviews = df['review']

# Combine the user query with your existing reviews
combined_reviews = list(reviews) + [user_query]

# Initialize CountVectorizer
vectorizer = CountVectorizer()

# Fit and transform the text data to get the word frequency matrix
word_frequency_matrix = vectorizer.fit_transform(combined_reviews)

# Get the word frequency vector for the user query
user_query_vector = word_frequency_matrix[-1]

# Calculate cosine similarity with existing reviews
cosine_similarities = cosine_similarity(word_frequency_matrix[:-1], user_query_vector)

# Find the most similar review
most_similar_review_index = cosine_similarities.argmax()

# Get the corresponding review and its cosine similarity score
most_similar_review = reviews.iloc[most_similar_review_index]
similarity_score = cosine_similarities[most_similar_review_index][0]

# Set a threshold for similarity (you can adjust this)
threshold = 0.5

# Check if the similarity score is above the threshold
if similarity_score > threshold:
    print(f"The user query is relevant. Most similar review: {most_similar_review}")
else:
    print("The user query is not relevant.")
