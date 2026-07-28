import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from rapidfuzz import process

# ==========================================
# Load Dataset
# ==========================================
df = pd.read_csv("data/imdb_clean.csv")

# Remove unnecessary column
if "Unnamed: 0" in df.columns:
    df = df.drop(columns=["Unnamed: 0"])

# ==========================================
# Merge duplicate movies
# ==========================================
movies = (
    df.groupby("title")
    .agg({
        "director": "first",
        "release_year": "first",
        "runtime": "first",
        "genre": lambda x: " ".join(sorted(set(x))),
        "rating": "first",
        "metascore": "first",
        "gross(M)": "first"
    })
    .reset_index()
)

# ==========================================
# Create content
# ==========================================
movies["content"] = (
    movies["genre"].fillna("") + " " +
    movies["director"].fillna("")
)

# ==========================================
# TF-IDF
# ==========================================
tfidf = TfidfVectorizer(stop_words="english")
tfidf_matrix = tfidf.fit_transform(movies["content"])

# ==========================================
# Cosine Similarity
# ==========================================
similarity = cosine_similarity(tfidf_matrix)


# ==========================================
# Recommendation Function
# ==========================================
def recommend_movies(movie_name, top_n=10):

    # Fuzzy search
    match = process.extractOne(movie_name, movies["title"])

    if match is None:
        return [], None

    matched_title = match[0]

    movie_index = movies[movies["title"] == matched_title].index[0]

    similarity_scores = list(enumerate(similarity[movie_index]))

    similarity_scores = sorted(
        similarity_scores,
        key=lambda x: x[1],
        reverse=True
    )

    recommendations = []

    for i in similarity_scores[1:top_n+1]:

        movie = movies.iloc[i[0]]

        recommendations.append({
            "title": movie["title"],
            "genre": movie["genre"],
            "director": movie["director"],
            "rating": movie["rating"],
            "year": movie["release_year"],
            "runtime": movie["runtime"],
            "metascore": movie["metascore"],
            "gross": movie["gross(M)"],
            "similarity": round(i[1] * 100, 2)
        })

    return recommendations, matched_title


# ==========================================
# Autocomplete Function
# ==========================================
def get_movie_titles():
    return sorted(movies["title"].tolist())