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

# import pickle
# import streamlit as st
# import requests
#
# def fetch_poster(movie_id):
#     url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
#     data = requests.get(url)
#     data = data.json()
#     poster_path = data['poster_path']
#     full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
#     return full_path
#
# def recommend(movie):
#     index = movies[movies['title'] == movie].index[0]
#     distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
#     recommended_movie_names = []
#     recommended_movie_posters = []
#     for i in distances[1:6]:
#         # fetch the movie poster
#         movie_id = movies.iloc[i[0]].movie_id
#         recommended_movie_posters.append(fetch_poster(movie_id))
#         recommended_movie_names.append(movies.iloc[i[0]].title)
#
#     return recommended_movie_names,recommended_movie_posters
#
#
# st.header('Movie Recommender System')
# movies = pickle.load(open('model/movie_list.pkl','rb'))
# similarity = pickle.load(open('model/similarity.pkl','rb'))
#
# movie_list = movies['title'].values
# selected_movie = st.selectbox(
#     "Type or select a movie from the dropdown",
#     movie_list
# )
#
# if st.button('Show Recommendation'):
#     recommended_movie_names,recommended_movie_posters = recommend(selected_movie)
#     col1, col2, col3, col4, col5 = st.columns(5)
#     with col1:
#         st.text(recommended_movie_names[0])
#         st.image(recommended_movie_posters[0])
#     with col2:
#         st.text(recommended_movie_names[1])
#         st.image(recommended_movie_posters[1])
#
#     with col3:
#         st.text(recommended_movie_names[2])
#         st.image(recommended_movie_posters[2])
#     with col4:
#         st.text(recommended_movie_names[3])
#         st.image(recommended_movie_posters[3])
#     with col5:
#         st.text(recommended_movie_names[4])
#         st.image(recommended_movie_posters[4])
#



