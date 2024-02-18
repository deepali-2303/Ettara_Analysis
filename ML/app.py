import streamlit as st
import pandas as pd
from langchain_helper import get_few_shot_db_chain

# Function to initialize session state
def initialize_session_state():
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []

csv_file_path = "../data/detailed-reviews-of-ettarra-coffee-house.csv"
df = pd.read_csv(csv_file_path)
st.set_page_config(layout="wide")
left_sidebar, right_sidebar = st.columns(2)

left_sidebar.header("Filter Options")
selected_column = left_sidebar.selectbox("Select Column to Filter", df.columns)
filter_value = left_sidebar.text_input(f"Enter {selected_column} to filter:", "")
filtered_df = df[df[selected_column].astype(str).str.contains(filter_value, case=False, na=False)]

left_sidebar.dataframe(filtered_df)

# Initialize session state
initialize_session_state()

right_sidebar.header("Chatbot")

# Display chat history in the right sidebar
right_sidebar.header("Chat History")
for history_item in st.session_state['chat_history']:
    right_sidebar.write(f"Q: {history_item['question']}")
    right_sidebar.write(f"A: {history_item['answer']}")
    right_sidebar.write("------------")

question = right_sidebar.text_input("Question: ")

if question:
    chain = get_few_shot_db_chain()
    response = chain.run(question)

    # Add the current interaction to the chat history
    st.session_state['chat_history'].append({'question': question, 'answer': response})

    right_sidebar.header("Answer")
    right_sidebar.write(response)
