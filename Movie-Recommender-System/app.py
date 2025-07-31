import streamlit as st
import pickle
import pandas as pd
import requests
import os

# --- Download from Hugging Face if not already present ---
def download_from_huggingface(url, filename):
    if not os.path.exists(filename):
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(filename, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
        else:
            st.error(f"Failed to download {filename} from Hugging Face.")
            st.stop()

# --- Hugging Face URLs ---
movies_url = "https://huggingface.co/tt49139/assets/resolve/main/movies.pkl"
similarity_url = "https://huggingface.co/tt49139/assets/resolve/main/similarity.pkl"

# --- Download files ---
download_from_huggingface(movies_url, "movies.pkl")
download_from_huggingface(similarity_url, "similarity.pkl")

# --- Load data ---
try:
    movies = pickle.load(open("movies.pkl", "rb"))
    similarity = pickle.load(open("similarity.pkl", "rb"))
except Exception as e:
    st.error(f"Failed to load pickle files: {e}")
    st.stop()

# --- Streamlit UI ---
st.set_page_config(page_title="🎬 Movie Recommender", layout="centered")
st.title("🎬 Movie Recommender System")
st.markdown("Get recommendations for your favorite movie.")

# --- Movie selection ---
selected_movie = st.selectbox("Choose a movie to get recommendations:", movies['title'].values)

# --- Recommendation logic ---
def recommend(movie):
    idx = movies[movies['title'] == movie].index[0]
    distances = similarity[idx]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    return [movies.iloc[i[0]].title for i in movie_list]

# --- Show recommendations ---
if st.button("Show Recommendations"):
    st.subheader("🎥 Recommended Movies:")
    recommended_names = recommend(selected_movie)
    for i, name in enumerate(recommended_names, start=1):
        st.markdown(f"**{i}. {name}**")
