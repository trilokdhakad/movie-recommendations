import streamlit as st
import pickle
import pandas as pd
import requests
import os

# ---- Large File Downloader from Google Drive ----
def download_large_file_from_google_drive(file_id, destination):
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()
    response = session.get(URL, params={'id': file_id}, stream=True)
    token = get_confirm_token(response)

    if token:
        params = {'id': file_id, 'confirm': token}
        response = session.get(URL, params=params, stream=True)

    save_response_content(response, destination)


def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith("download_warning"):
            return value
    return None


def save_response_content(response, destination):
    CHUNK_SIZE = 32768
    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk:  # filter out keep-alive chunks
                f.write(chunk)

# ---- Google Drive file IDs ----
movies_id = "1UaPI3VrmLAikh-7G90hCa_UMj9vygzXF"
similarity_id = "1deakAkH-TeHzsb9ybeBaBNKLkbs6CoJb"

# ---- Download files if not already present ----
if not os.path.exists("movies.pkl"):
    download_large_file_from_google_drive(movies_id, "movies.pkl")
if not os.path.exists("similarity.pkl"):
    download_large_file_from_google_drive(similarity_id, "similarity.pkl")

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
