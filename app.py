import streamlit as st
import pickle as pk
import requests

def fetch_poster(movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=b0dd36515d50b6fabda89cbef57d184c&language=en-US'
    response = requests.get(url)
    data = response.json()

    if 'poster_path' in data and data['poster_path']:
        return "https://image.tmdb.org/t/p/w500" + data['poster_path']
    else:
        return "https://via.placeholder.com/500x750?text=No+Image"

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:11]

    recommended_movies = []
    movie_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]]['movie_id']  # ✅ real TMDB ID from DataFrame
        recommended_movies.append(movies.iloc[i[0]]['title'])
        movie_posters.append(fetch_poster(movie_id))  # 🔁 now with correct ID

    return recommended_movies, movie_posters

movies=pk.load(open('movies.pkl','rb')) # its a dataframe
similarity=pk.load(open('similarity.pkl','rb'))

movie_titles = movies['title'].values

st.title('Movie Recommender System')

selected_movie=st.selectbox(
    '🎞️ Select a movie to get recommendations:',
    movie_titles
)

if st.button('Recommend'):
    names, posters = recommend(selected_movie)

    st.subheader("🎬 Recommended Movies:")

    # First row - 5 movies
    row1 = st.columns(5)
    for i in range(5):
        with row1[i]:
            st.image(posters[i], use_container_width=True)
            st.markdown(
                f"<div style='text-align: center; font-size: 16px; font-weight: bold; margin-top: 8px;'>{names[i]}</div>",
                unsafe_allow_html=True
            )

    # Add vertical spacing between rows
    st.markdown("<br>", unsafe_allow_html=True)

    # Second row - 5 movies
    row2 = st.columns(5)
    for i in range(5, 10):
        with row2[i - 5]:
            st.image(posters[i], use_container_width=True)
            st.markdown(
                f"<div style='text-align: center; font-size: 16px; font-weight: bold; margin-top: 8px;'>{names[i]}</div>",
                unsafe_allow_html=True
            )