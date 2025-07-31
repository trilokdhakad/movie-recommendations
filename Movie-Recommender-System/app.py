import streamlit as st
import pandas as pd
import pickle
import os
import gdown

st.set_page_config(page_title="🎬 Movie Recommender", layout="centered")
st.title("🎬 Movie Recommender System")

# --- Google Drive File IDs ---
MOVIES_FILE_ID = "1UaPI3VrmLAikh-7G90hCa_UMj9vygzXF"
SIMILARITY_FILE_ID = "1deakAkH-TeHzsb9ybeBaBNKLkbs6CoJb"

# --- Download Function ---
def download_from_gdrive(file_id, output):
    if not os.path.exists(output):
        url = f"https://drive.google.com/uc?id={file_id}"
        gdown.download(url, output, quiet=False)

# --- Download files if not present ---
download_from_gdrive(MOVIES_FILE_ID, "movies.pkl")
download_from_gdrive(SIMILARITY_FILE_ID, "similarity.pkl")

# --- Safety Checks ---
if not os.path.exists("movies.pkl") or os.path.getsize("movies.pkl") < 10000:
    st.error("❌ Error downloading or corrupt movies.pkl")
    st.stop()

if not os.path.exists("similarity.pkl") or os.path.getsize("similarity.pkl") < 10000:
    st.error("❌ Error downloading or corrupt similarity.pkl")
    st.stop()

# --- Load Pickle Files ---
try:
    with open("movies.pkl", "rb") as f:
        movies = pickle.load(f)
    with open("similarity.pkl", "rb") as f:
        similarity = pickle.load(f)
except Exception as e:
    st.error(f"❌ Failed to load pickle files: {e}")
    st.stop()

# --- UI & Recommendation ---
selected_movie = st.selectbox("Choose a movie:", movies['title'].values)

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = similarity[index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    return [movies.iloc[i[0]].title for i in movie_list]

if st.button("Recommend"):
    st.subheader("🎥 Top 5 Recommendations:")
    for i, m in enumerate(recommend(selected_movie), 1):
        st.write(f"{i}. {m}")
