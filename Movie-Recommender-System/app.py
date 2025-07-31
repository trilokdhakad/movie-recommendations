import streamlit as st
import pickle
import pandas as pd
import requests

# Function to download file from Google Drive
def download_file_from_google_drive(url, filename):
    response = requests.get(url)
    with open(filename, 'wb') as f:
        f.write(response.content)

# Direct download links
movies_url = "https://drive.google.com/uc?export=download&id=1UaPI3VrmLAikh-7G90hCa_UMj9vygzXF"
similarity_url = "https://drive.google.com/uc?export=download&id=1deakAkH-TeHzsb9ybeBaBNKLkbs6CoJb"

# Download the files
download_file_from_google_drive(movies_url, "movies.pkl")
download_file_from_google_drive(similarity_url, "similarity.pkl")

# Load the data
movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# --- Streamlit UI ---
st.set_page_config(page_title="🎬 Movie Recommender", layout="centered")
st.title("🎬 Movie Recommender System")
st.markdown("Get recommendations for your favorite movie.")

# Movie selection dropdown
selected_movie = st.selectbox("Choose a movie to get recommendations:", movies['title'].values)

# Recommendation logic
def recommend(movie):
    idx = movies[movies['title'] == movie].index[0]
    distances = similarity[idx]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    return [movies.iloc[i[0]].title for i in movie_list]

# Show recommendations
if st.button("Show Recommendations"):
    st.subheader("🎥 Recommended Movies:")
    recommended_names = recommend(selected_movie)

    for i, name in enumerate(recommended_names, start=1):
        st.markdown(f"**{i}. {name}**")
