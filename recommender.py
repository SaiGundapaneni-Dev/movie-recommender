# recommender.py (Real-time TMDb version)

import requests
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st

API_KEY = st.secrets["TMDB_API_KEY"]

# Fetch real-time movie data from TMDb API
def fetch_popular_movies(pages=3):
    all_movies = []
    for page in range(1, pages + 1):
        url = f"https://api.themoviedb.org/3/movie/popular?api_key={API_KEY}&language=en-US&page={page}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            for movie in data["results"]:
                all_movies.append({
                    "id": movie["id"],
                    "title": movie["title"],
                    "overview": movie.get("overview", ""),
                    "poster_path": movie.get("poster_path", ""),
                    "vote_average": movie.get("vote_average", "N/A")
                })
    return pd.DataFrame(all_movies)

# Build similarity model
def build_similarity_matrix(df):
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(df["overview"])
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    return cosine_sim

# Initialize data and similarity
@st.cache_data(show_spinner=False)
def get_data():
    df = fetch_popular_movies(pages=5)
    sim_matrix = build_similarity_matrix(df)
    return df, sim_matrix

df, cosine_sim = get_data()

title_to_index = pd.Series(df.index, index=df['title'])

# Generate recommendation list
def recommend(title, num_recommendations=10):
    if title not in title_to_index:
        return [], [], [], []

    idx = title_to_index[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:num_recommendations+1]

    names, posters, descriptions, links = [], [], [], []
    for i in sim_scores:
        movie = df.iloc[i[0]]
        movie_id = movie['id']
        poster_url = f"https://image.tmdb.org/t/p/w500{movie['poster_path']}"
        overview = movie['overview']
        rating = movie['vote_average']
        link = f"https://www.themoviedb.org/movie/{movie_id}"

        names.append(movie['title'])
        posters.append(poster_url)
        descriptions.append({"text": overview, "rating": rating})
        links.append(link)

    return names, posters, descriptions, links
