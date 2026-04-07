from fastapi import FastAPI
from db import SessionLocal
from models import Movie

app = FastAPI()

# POST METHOD (Member 2)
@app.post("/add_movie")
def add_movie(movie_name: str, hero: str, heroine: str):
    db = SessionLocal()
    new_movie = Movie(movie_name=movie_name, hero=hero, heroine=heroine)
    db.add(new_movie)
    db.commit()
    db.close()
    return {"message": "Movie added successfully"}


# GET METHOD (Member 3)
@app.get("/get_movies")
def get_movies():
    db = SessionLocal()
    movies = db.query(Movie).all()
    db.close()

    return [
        {
            "movie_name": m.movie_name,
            "hero": m.hero,
            "heroine": m.heroine
        }
        for m in movies
    ]