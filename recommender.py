import pandas as pd
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
def recommend(title, num_recommendations=5):
    if title not in title_to_index:
        return f"Movie '{title}' not found in the dataset."

    idx = title_to_index[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:num_recommendations + 1]  # Skip the first one (itself)

    recommended_titles = [df['title'].iloc[i[0]] for i in sim_scores]
    return recommended_titles
