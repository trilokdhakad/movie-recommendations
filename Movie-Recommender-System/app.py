import streamlit as st
import pickle
import pandas as pd
import requests
import os

# ---- Hugging Face File URLs ----
MOVIES_URL = "https://huggingface.co/tt49139/assets/resolve/main/movies.pkl"
SIMILARITY_URL = "https://huggingface.co/tt49139/assets/resolve/main/similarity.pkl"

# ---- Download and cache files locally ----
def download_file(url, filename):
    if not os.path.exists(filename):
        response = requests.get(url, stream=True)
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

download_file(MOVIES_URL, "movies.pkl")
download_file(SIMILARITY_URL, "similarity.pkl")

# ---- Load data ----
movies = pickle.load(open("movies.pkl", "rb"))
similarity = pickle.load(open("similarity.pkl", "rb"))

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
