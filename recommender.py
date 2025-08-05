import pandas as pd
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load data
df = pd.read_csv('data/tmdb_5000_movies.csv')

# Fill empty overviews with empty string
df['overview'] = df['overview'].fillna('')

# 1. Convert movie overviews to TF-IDF matrix
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(df['overview'])

# 2. Compute similarity between movies using cosine similarity
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# 3. Create a reverse mapping from movie title to index
title_to_index = pd.Series(df.index, index=df['title']).drop_duplicates()

# 4. Recommendation function
def recommend(title, num_recommendations=10):
    if title not in title_to_index:
        return [], [], [], []

    idx = title_to_index[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:num_recommendations + 1]

    names, posters, descriptions, links = [], [], [], []

    for i in sim_scores:
        movie_title = df['title'].iloc[i[0]]
        poster, desc, url, rating = fetch_movie_details(movie_title)

        names.append(movie_title)
        posters.append(poster)
        descriptions.append({'text': desc, 'rating': rating})
        links.append(url)

    return names, posters, descriptions, links


import requests

API_KEY = st.secrets["TMDB_API_KEY"]

def fetch_movie_details(title):
    search_url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={title}"
    response = requests.get(search_url)
    data = response.json()

    if data['results']:
        movie = data['results'][0]
        poster_path = movie.get('poster_path')
        overview = movie.get('overview', 'No description available.')
        tmdb_id = movie.get('id')
        rating = movie.get('vote_average', 'N/A')

        full_poster = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else "https://via.placeholder.com/200x300"
        tmdb_url = f"https://www.themoviedb.org/movie/{tmdb_id}"

        return full_poster, overview, tmdb_url, rating

    return "https://via.placeholder.com/200x300", "No description found.", "#", "N/A"


