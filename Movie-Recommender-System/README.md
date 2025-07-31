# 🎬 Movie Recommendation System

This project recommends similar movies using **content-based filtering** on the TMDB 5000 dataset. It provides a Jupyter notebook for building the model and a **Streamlit-based web app** for movie recommendations.

---

## 📂 Files to Download

Download the following files from [Kaggle - TMDB Movie Metadata](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata):

- [`tmdb_5000_movies.csv`](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata)
- [`tmdb_5000_credits.csv`](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata)

Place both files in the **project root directory**.

---

## ⚙️ How It Works

1. The Jupyter notebook `movie-recommendations.ipynb`:
   - Loads and processes the data.
   - Creates movie feature vectors using NLP techniques.
   - Saves processed data as:
     - `movies.pkl`
     - `similarity.pkl`

2. The Streamlit app (`app.py`):
   - Loads the above `.pkl` files.
   - Recommends top 5 similar movies.
   - Fetches posters using the TMDB API.
   - If poster fetch fails, it tries scraping fallback using BeautifulSoup.

---

## 🛠️ Requirements

Install required libraries using:

```bash
pip install -r requirements.txt
