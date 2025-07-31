import streamlit as st
import pickle
import pandas as pd
import requests
import os
from huggingface_hub import hf_hub_download

# --- Page config ---
st.set_page_config(page_title="🎬 Movie Recommender", layout="wide")
st.title("🎬 Movie Recommender System")

# --- Download .pkl files from Hugging Face (only once) ---
@st.cache_resource
def load_pickles():
    try:
        movies_path = hf_hub_download(repo_id="tt49139/assets", filename="movies.pkl")
        similarity_path = hf_hub_download(repo_id="tt49139/assets", filename="similarity.pkl")

        with open(movies_path, 'rb') as f:
            movies = pickle.load(f)

        with open(similarity_path, 'rb') as f:
            similarity = pickle.load(f)

        return movies, similarity
    except Exception as e:
        st.error(f"❌ Failed to load pickle files: {e}")
        st.stop()

movies, similarity = load_pickles()

# --- Convert movies to DataFrame if needed ---
if isinstance(movies, pd.DataFrame):
    movie_list = movies['title'].values
else:
    movie_list = [movie['title'] for movie in movies]

# --- TMDB API Setup ---
API_KEY = os.getenv("TMDB_API_KEY")

def fetch_poster(movie_id):
    if not API_KEY:
        return ""
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return f"https://image.tmdb.org/t/p/w500{data['poster_path']}"
    return ""

def recommend(movie):
    if movie not in movie_list:
        return [], [], []
    index = list(movie_list).index(movie)
    distances = similarity[index]
    movie_indices = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_posters = []
    recommended_ids = []

    for i in movie_indices:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))
        recommended_ids.append(movie_id)

    return recommended_movies, recommended_posters, recommended_ids

# --- UI ---
selected_movie_name = st.selectbox("Search a movie", movie_list)

if st.button("Show Recommendation"):
    names, posters, ids = recommend(selected_movie_name)

    if not names:
        st.warning("No recommendations found.")
    else:
        cols = st.columns(5)
        for i in range(5):
            with cols[i]:
                st.text(names[i])
                if posters[i]:
                    st.image(posters[i])
                else:
                    st.write("Poster not found.")
