import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.title("🎬 Movie App")

def fetch_movies():
    response = requests.get(f"{API_URL}/get_movies", timeout=5)
    response.raise_for_status()
    return response.json()


def add_movie(movie_name: str, hero: str, heroine: str):
    response = requests.post(
        f"{API_URL}/add_movie",
        params={"movie_name": movie_name, "hero": hero, "heroine": heroine},
        timeout=5,
    )
    response.raise_for_status()
    return response.json()


try:
    movies = fetch_movies()
except requests.exceptions.RequestException:
    st.error(
        "Could not connect to backend API. Start FastAPI first with: "
        "`uvicorn routes:app --reload`"
    )
    st.stop()

movie_names = [m["movie_name"] for m in movies]

# DROPDOWN
selected_movie = st.selectbox("Select Movie", movie_names) if movie_names else None

# SHOW DETAILS
if selected_movie:
    for m in movies:
        if m["movie_name"] == selected_movie:
            st.write(f"Hero: {m['hero']}")
            st.write(f"Heroine: {m['heroine']}")
else:
    st.info("No movies found yet. Add your first movie below.")

st.divider()

# ADD MOVIE
st.subheader("Add New Movie")

movie = st.text_input("Movie Name")
hero = st.text_input("Hero")
heroine = st.text_input("Heroine")

if st.button("Submit"):
    if not movie.strip() or not hero.strip() or not heroine.strip():
        st.warning("Please fill all fields before submitting.")
    else:
        try:
            add_movie(movie.strip(), hero.strip(), heroine.strip())
            st.success("Movie added successfully!")
            st.rerun()
        except requests.exceptions.RequestException:
            st.error("Failed to add movie. Please check backend connection.")