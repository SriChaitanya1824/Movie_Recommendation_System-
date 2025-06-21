import streamlit as st
import pickle
import pandas as pd
import requests
def fetchPoster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    response = requests.get(url)
    data = response.json()
    if 'poster_path' in data:
        return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    else:
        return "https://via.placeholder.com/500x750?text=No+Image"
def recommend(title):
    index = movies[movies['title'] == title].index[0]
    distances = similarity[index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_titles = []
    recommended_posters = []
    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_titles.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetchPoster(movie_id))
    return recommended_titles, recommended_posters
movies_dict = pickle.load(open('MoviesDict1.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))
st.title("🎬 MOVIES!!!")
selected_movie = st.selectbox("Which Movie Do You Like ??", movies['title'].values)
if st.button("Recommend"):
    titles, posters = recommend(selected_movie)
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.text(titles[i])
            st.image(posters[i])
