import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from apyori import apriori

# Load the dataset
dataset = pd.read_csv('./data/output1_final.csv', header=None)
transactions = []
for i in range(0, 302):
    transactions.append([str(dataset.values[i, j]) for j in range(0, 10)])

# Run Apriori algorithm
rules = apriori(transactions=transactions, min_support=0.003, min_confidence=0.2, min_lift=3, min_length=2, max_length=2)
results = list(rules)

def inspect(results):
    lhs = [tuple(result[2][0][0])[0] for result in results]
    rhs = [tuple(result[2][0][1])[0] for result in results]
    supports = [result[1] for result in results]
    confidences = [result[2][0][2] for result in results]
    lifts = [result[2][0][3] for result in results]
    return list(zip(lhs, rhs, supports, confidences, lifts))

resultDataFrame = pd.DataFrame(inspect(results), columns=['Left Hand Side', 'Right Hand Side', 'Support', 'Confidence', 'Lift'])

# Streamlit App
st.title('Apriori Results Explorer')

# Dropdown to select item from the Left Hand Side (lhs) column
selected_lhs = st.selectbox('Select item from Left Hand Side (lhs) column', resultDataFrame['Left Hand Side'].unique())

# Filter rows based on selected lhs
filtered_rows = resultDataFrame[resultDataFrame['Left Hand Side'] == selected_lhs]

# Display filtered results
if not filtered_rows.empty:
    st.write(f"Association rules for {selected_lhs}:")

    # Display rhs values in new lines
    st.write("Right Hand Side Values:")
    for rhs_value in filtered_rows['Right Hand Side']:
        st.write(rhs_value)

    
else:
    st.warning(f"No results found for {selected_lhs}. Try selecting another item.")
