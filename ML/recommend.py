import streamlit as st
import matplotlib.pyplot as plt
from surprise import Dataset, Reader, KNNWithMeans
from surprise.model_selection import train_test_split
import pandas as pd

# Load the data
data = pd.read_csv("./data/ETTARRA Jan'24  FOR TST - Recommender_final_data.csv")  

# Configure Surprise
reader = Reader(rating_scale=(0, 10))
data_surprise = Dataset.load_from_df(data[['Invoice No.', 'Item Name', 'Qty.']], reader)

trainset, testset = train_test_split(data_surprise, test_size=0.2, random_state=42)

sim_options = {'name': 'cosine', 'user_based': True}
algo = KNNWithMeans(sim_options=sim_options)

algo.fit(trainset)

# Streamlit App
st.title('Recommender System App')

# Dropdown to select user_id
selected_user_id = st.selectbox('Select User ID', data['Invoice No.'].unique())

# Generate recommendations
purchased_items = data[data['Invoice No.'] == selected_user_id]['Item Name'].tolist()
purchased_items = list(set(purchased_items))
unpurchased_items = [item for item in data['Item Name'].unique() if item not in purchased_items]

st.write(f"Previously Purchased Items for User {selected_user_id}:")
for i, item in enumerate(purchased_items, 1):
    st.write(f"{i}. {item}")

predictions = [algo.predict(selected_user_id, item) for item in unpurchased_items]
predictions.sort(key=lambda x: x.est, reverse=True)
top_recommendations = [pred.iid for pred in predictions[:3]]

# Display recommendations
st.write(f"Top 3 recommended items for User {selected_user_id}:")
for i, item in enumerate(top_recommendations, 1):
    st.write(f"{i}. {item}")

# Plotting
item_names = [pred.iid for pred in predictions[:3]]
predicted_ratings = [pred.est for pred in predictions[:3]]

fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(item_names, predicted_ratings, color='skyblue')
ax.set_xlabel('Item Name')
ax.set_ylabel('Predicted Rating')
ax.set_title(f'Top 3 Recommended Items for User {selected_user_id}')
ax.set_xticklabels(item_names, rotation=45, ha='right')
st.pyplot(fig)
