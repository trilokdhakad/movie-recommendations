import streamlit as st
import pickle
import pandas as pd
from huggingface_hub import hf_hub_download

# --- Page setup ---
st.set_page_config(page_title="🎬 Movie Recommender", layout="wide")
st.title("🎬 Movie Recommender System")

# --- Load pickles from Hugging Face ---
@st.cache_resource
def load_data():
    try:
        movies_path = hf_hub_download(repo_id="tt49139/assets", filename="movies.pkl")
        similarity_path = hf_hub_download(repo_id="tt49139/assets", filename="similarity.pkl")

        with open(movies_path, "rb") as f:
            movies = pickle.load(f)

        with open(similarity_path, "rb") as f:
            similarity = pickle.load(f)

        return movies, similarity
    except Exception as e:
        st.error(f"❌ Failed to load data: {e}")
        st.stop()

movies, similarity = load_data()

# --- Movie list ---
movie_list = movies['title'].values

# --- Recommendation logic ---
def recommend(movie):
    if movie not in movie_list:
        return []

    index = list(movie_list).index(movie)
    distances = similarity[index]
    movie_indices = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommendations = [movies.iloc[i[0]].title for i in movie_indices]
    return recommendations

# --- UI ---
selected_movie = st.selectbox("Choose a movie to get recommendations:", movie_list)

if st.button("Show Recommendations"):
    recommendations = recommend(selected_movie)

    if not recommendations:
        st.warning("No recommendations found.")
    else:
        st.subheader("Top 5 Recommended Movies:")
        for movie in recommendations:
            st.write("•", movie)
