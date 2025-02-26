import streamlit as st
import pickle
import requests
import os
import gdown

def fetch_poster(movie_id):
    res = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=05a466e366948748d62f443ebef8b792&language=en-US'.format(movie_id))
    data = res.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie):
    rec = []
    poster = []
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    sim_movies = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    for i in sim_movies:
        rec.append(movies.iloc[i[0]].title)
        poster.append(fetch_poster(movies.iloc[i[0]].id))
    return rec,poster

# Load the DataFrame
with open("movies.pkl", "rb") as f:
    movies = pickle.load(f)


# Google Drive File ID
file_id = "1PToi2bgCzjndWifOs3i_zzasrBpqzz1M"

# Path where similarity.pkl will be saved
output_path = "similarity.pkl"

# Download from Google Drive if the file doesn't exist locally
if not os.path.exists(output_path):
    file_url = f"https://drive.google.com/uc?id={file_id}"
    gdown.download(file_url, output_path, quiet=False)

# Load the similarity matrix after downloading
with open("similarity.pkl", "rb") as f:
    similarity = pickle.load(f)


st.title("Movie Recommender System")

selected_movie = st.selectbox(
    "What's on your mind ",
    (movies['title'].values)
)

if st.button('Recommend'):
    name,poster = recommend(selected_movie)

    # Create columns (2 columns: 30% width for text, 70% for image)
    col1, col2,col3, col4,col5,  = st.columns(5)

    # Display Movie Name in col1
    with col1:
        st.image(poster[0])
        st.write(name[0])  # Movie title
    with col2:
        st.image(poster[1])
        st.write(name[1])  # Movie title
    with col3:
        st.image(poster[2])
        st.write(name[2])  # Movie title
    with col4:
        st.image(poster[3])
        st.write(name[3])  # Movie title
    with col5:
        st.image(poster[4])
        st.write(name[4])  # Movie title


