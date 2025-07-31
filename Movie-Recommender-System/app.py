import streamlit as st
import pickle
import pandas as pd
import requests
import os

# ---- Hugging Face file URLs ----
movies_url = "https://huggingface.co/tt49139/assets/resolve/main/movies.pkl"
similarity_url = "https://huggingface.co/tt49139/assets/resolve/main/similarity.pkl"

# ---- Downloader ----
def download_file(url, destination):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(destination, "wb") as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
    else:
        st.error(f"Failed to download {url}")
        st.stop()

# ---- Download if not already present ----
if not os.path.exists("movies.pkl"):
    download_file(movies_url, "movies.pkl")
if not os.path.exists("similarity.pkl"):
    download_file(similarity_url, "similarity.pkl")

# ---- Load data ----
try:
    with open("movies.pkl", "rb") as f:
        movies = pickle.load(f)
    with open("similarity.pkl", "rb") as f:
        similarity = pickle.load(f)
except Exception as e:
    st.error(f"Failed to load pickle files: {e}")
    st.stop()

# ---- Streamlit UI ----
st.set_page_config(page_title="🎬 Movie Recommender", layout="centered")
st.title("🎬 Movie Recommender System")
st.markdown("Get recommendations for your favorite movie.")

# ---- Movie selection ----
selected_movie = st.selectbox("Choose a movie to get recommendations:", movies['title'].values)

# ---- Recommendation logic ----
def recommend(movie):
    idx = movies[movies['title'] == movie].index[0]
    distances = similarity[idx]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    return [movies.iloc[i[0]].title for i in movie_list]

# ---- Show recommendations ----
if st.button("Show Recommendations"):
    st.subheader("🎥 Recommended Movies:")
    recommended_names = recommend(selected_movie)
    for i, name in enumerate(recommended_names, start=1):
        st.markdown(f"**{i}. {name}**")
