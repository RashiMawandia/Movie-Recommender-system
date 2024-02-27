import streamlit as st
import pandas as pd
import requests
import pickle

movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl','rb'))


def  recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    recommended_movies_posters=[]
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies_posters.append(fetch_poster(movie_id))
        # fetch poster from API
        recommended_movies.append(movies.iloc[i[0]].title)
    return recommended_movies,recommended_movies_posters
def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/"+data['poster_path']



st.title('Movie Recommender System')
selected_movie_name = st.selectbox(
"Type or select a movie from the dropdown",
movies['title'].values)
if st.button('Show Recommendation'):
    names,posters = recommend(selected_movie_name)
    columns = st.columns(5)
    with columns[0]:
        st.text(names[0])
        st.image(posters[0])
    with columns[1]:
        st.text(names[1])
        st.image(posters[1])
    with columns[2]:
        st.text(names[2])
        st.image(posters[2])
    with columns[3]:
        st.text(names[3])
        st.image(posters[3])
    with columns[4]:
        st.text(names[4])
        st.image(posters[4])
