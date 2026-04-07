from fastapi import FastAPI, HTTPException
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from db import SessionLocal
from models import Movie

app = FastAPI()


@app.post("/add_movie")
def add_movie(movie_name: str, hero: str, heroine: str):
    db = SessionLocal()
    try:
        current_max_id = db.query(func.max(Movie.id)).scalar()
        next_id = (current_max_id or 0) + 1

        new_movie = Movie(
            id=next_id,
            movie_name=movie_name,
            hero=hero,
            heroine=heroine,
        )
        db.add(new_movie)
        db.commit()
        return {"message": "Movie added successfully", "id": next_id}
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(exc)}")
    finally:
        db.close()


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