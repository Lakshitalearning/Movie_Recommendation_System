import streamlit as st
import pickle
import pandas as pd
import requests
from pandas import DataFrame


def fetch_poster(movie_id):
    response = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key=a1699cc285d421a97e13c0a34d478cd0&&language=en-US'.format(
            movie_id))
    data = response.json()
    print(data)
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']


# loading dataframe from collab
movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies: DataFrame = pd.DataFrame(movies_dict)
st.title('Movie Recommender System')

# contains all movie names
selected_movie_name = st.selectbox(
    'How would you like to be contacted ?',
    movies['title'].values)

similarity = pickle.load(open("similarity.pkl", 'rb'))


# defining function that recommends 5 movies based on selected movie name
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommend_movies = []
    recommend_movies_poster = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id  #contains movie id
        recommend_movies.append(movies.iloc[i[0]].title)
        #to fetch poster from API
        recommend_movies_poster.append(fetch_poster(movie_id))
    return recommend_movies, recommend_movies_poster


# button created to select movie name and to recommend movie names
if st.button('Recommend'):
    names,posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])


