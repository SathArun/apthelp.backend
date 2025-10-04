import streamlit as st
import requests

# Adjust this if backend runs elsewhere
BACKEND_URL = "http://127.0.0.1:8080/query"

st.set_page_config(page_title="Tamil Nadu Bye-laws Q&A", layout="wide")
st.title("🏢 Tamil Nadu Apartment Bye-laws Q&A")

query = st.text_area("Enter your question:", placeholder="e.g., What is the minimum parking requirement under TN Apartment Rules?")

if st.button("Ask"):
    if not query.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Fetching answer..."):
            try:
                res = requests.post(BACKEND_URL, json={"question": query})
                res.raise_for_status()
                data = res.json()
                st.subheader("Answer:")
                st.write(data.get("answer", "No answer found."))
            except Exception as e:
                st.error(f"Error: {e}")
