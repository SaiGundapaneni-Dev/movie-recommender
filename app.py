# Final version of app.py with trending + recommendations only (date and latest logic removed)

import streamlit as st
from recommender import recommend, df
import random
import pandas as pd

# Custom styles
st.set_page_config(page_title="Movie2Day", layout="wide")

st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://media.istockphoto.com/id/1077169030/photo/lens-flare-and-bokeh-black-background.jpg?s=612x612&w=0&k=20&c=T0MuZ3gpzz1K425PUS6Q8rb7JNZGu5jfHevellX1MZc=");
        background-size: cover;
        background-attachment: fixed;
        background-position: center;
        background-repeat: no-repeat;
    }
    .movie-card {
        position: relative;
        transition: transform 0.3s ease-in-out;
        border-radius: 15px;
        overflow: hidden;
        backdrop-filter: blur(8px);
        background-color: rgba(255, 255, 255, 0.05);
        padding: 5px;
    }
    .movie-card:hover {
        transform: scale(1.07);
        box-shadow: 0px 6px 25px rgba(255, 255, 255, 0.2);
    }
    .rating-badge {
        position: absolute;
        top: 8px;
        left: 8px;
        background-color: rgba(0, 0, 0, 0.7);
        color: #FFD700;
        padding: 4px 8px;
        border-radius: 5px;
        font-size: 13px;
        font-weight: bold;
        z-index: 2;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title Header
st.markdown(
    """
    <div style='text-align: center; padding: 20px; background-color: rgba(0, 0, 0, 0.5); border-radius: 12px; margin-bottom: 30px;'>
        <h1 style='font-size: 48px; color: #FFD700;'>🍿 Movie2Day</h1>
        <h4 style='color: #f0f0f0;'>Your AI-Powered Movie Companion</h4>
    </div>
    """,
    unsafe_allow_html=True
)

# Movie search form
st.markdown("### 🎬 Search for a Movie")
with st.form("search_form", clear_on_submit=False):
    movie_query = st.text_input("Enter a movie name to search:")
    submitted = st.form_submit_button("Recommend")

# Show Trending Now only when no search has been submitted
if not movie_query:
    st.markdown("### 🔥 Trending Now")
    sample_movies = df.sample(10) if len(df) >= 10 else df
    sample_movies = sample_movies.reset_index(drop=True)
    cols = st.columns(5)
    for i in range(len(sample_movies)):
        with cols[i % 5]:
            poster_url = f"https://image.tmdb.org/t/p/w500{sample_movies['poster_path'][i]}"
            rating = sample_movies['vote_average'][i]
            title = sample_movies['title'][i]
            link = f"https://www.themoviedb.org/movie/{sample_movies['id'][i]}"
            st.markdown(f"""
                <div class="movie-card">
                    <a href="{link}" target="_blank">
                        <div class="rating-badge">⭐ {rating}</div>
                        <img src="{poster_url}" width="160" style="border-radius:15px;">
                    </a>
                </div>
            """, unsafe_allow_html=True)

# Recommendation logic after form submission
if movie_query and submitted:
    matches = [title for title in df['title'].values if movie_query.lower() in title.lower()]
    if not matches:
        st.warning("No movie found. Please check your spelling.")
    else:
        selected_movie = matches[0]
        st.success(f"Showing results for: **{selected_movie}**")

        names, posters, descriptions, links = recommend(selected_movie)

        st.subheader(f"🎯 Top 10 Similar Movies to '{selected_movie}'")
        cols = st.columns(5)
        for i in range(10):
            with cols[i % 5]:
                st.markdown(f"""
                    <div class="movie-card">
                        <a href="{links[i]}" target="_blank">
                            <div class="rating-badge">⭐ {descriptions[i]['rating']}</div>
                            <img src="{posters[i]}" width="160" style="border-radius:15px;">
                        </a>
                    </div>
                """, unsafe_allow_html=True)
