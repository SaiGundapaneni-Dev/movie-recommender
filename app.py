import streamlit as st
import pandas as pd
from recommender import recommend

# ✅ Add custom CSS for background image
st.markdown(
    """
    <style>
    .stApp {
        background-image: url("");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
        background-position: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)



# Load the dataset just to show dropdown options
df = pd.read_csv("data/tmdb_5000_movies.csv")

st.set_page_config(page_title="🎬 Movie Recommender", layout="centered")

st.markdown(
    "<h1 style='text-align: center; color: #f4d35e;'>🎬 Movie2Day AI: Find Your Next Favorite Film</h1>",
    unsafe_allow_html=True
)


st.write("Select a movie, and we'll show you 10 similar ones!")

# Movie selection box
movie_list = df['title'].values
selected_movie = st.selectbox("Choose a movie:", movie_list)

if st.button("Recommend"):
    names, posters, descriptions, links = recommend(selected_movie)
    st.subheader(f"🎬 Top 10 Similar Movies to '{selected_movie}'")

    # Add global CSS for hover effects and rating badges
    st.markdown("""
        <style>
        .movie-card {
            position: relative;
            transition: transform 0.2s;
            border-radius: 10px;
        }
        .movie-card:hover {
            transform: scale(1.05);
            box-shadow: 0px 4px 20px rgba(255, 255, 255, 0.4);
        }
        .rating-badge {
            position: absolute;
            top: 8px;
            left: 8px;
            background-color: rgba(0, 0, 0, 0.7);
            color: #FFD700;
            padding: 4px 8px;
            border-radius: 5px;
            font-size: 14px;
            font-weight: bold;
        }
        </style>
    """, unsafe_allow_html=True)

    cols = st.columns(5)

    for i in range(10):
        with cols[i % 5]:
            st.markdown(f"""
                <div class="movie-card">
                    <a href="{links[i]}" target="_blank">
                        <div class="rating-badge">⭐ {descriptions[i]['rating']}</div>
                        <img src="{posters[i]}" width="150" style="border-radius:10px;">
                    </a>
                </div>
            """, unsafe_allow_html=True)




