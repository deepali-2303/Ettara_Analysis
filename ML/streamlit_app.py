import streamlit as st

st.title("Streamlit with React App")

# Embed the React app using an iframe
st.write(f'<iframe src="http://localhost:3001/" width="1200" height="1200"></iframe>', unsafe_allow_html=True)
