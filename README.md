# 🎬 Movie Recommendation App

This is a simple content-based movie recommendation system built with Streamlit.

## How it works
- Uses movie overviews (descriptions) from TMDB 5000 dataset
- Applies TF-IDF vectorization and cosine similarity
- Recommends top 5 similar movies

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
