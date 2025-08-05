#import pandas as pd
#
## Load the dataset
#df = pd.read_csv('data/tmdb_5000_movies.csv')
#
## Show basic info
#print("Shape of the dataset:", df.shape)
#print("\nFirst 5 rows:")
#print(df.head())
#
## Show column names
#print("\nColumn names:")
#print(df.columns)
#
#from recommender import recommend
#
#movie_name = "2012"
#recommendations = recommend(movie_name)
#
#print(f"\nMovies similar to '{movie_name}':")
#for i, movie in enumerate(recommendations, 1):
#    print(f"{i}. {movie}")

import streamlit as st
import pandas as pd
from recommender import recommend

# Load the dataset just to show dropdown options
df = pd.read_csv("data/tmdb_5000_movies.csv")

st.set_page_config(page_title="🎬 Movie Recommender", layout="centered")
st.title("🎬 Movie Recommendation App")
st.write("Select a movie, and we'll show you 5 similar ones!")

# Movie selection box
movie_list = df['title'].values
selected_movie = st.selectbox("Choose a movie:", movie_list)

if st.button("Recommend"):
    recommendations = recommend(selected_movie)
    st.subheader(f"Movies similar to '{selected_movie}':")
    for i, movie in enumerate(recommendations, 1):
        st.write(f"{i}. {movie}")
