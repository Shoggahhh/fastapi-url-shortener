from pydantic import BaseModel


class MovieBase(BaseModel):
    movie_id: int
    name: str
    description: str
    rating: str
    age_rating: str
    url: str


class Movie(MovieBase):
    """
    Model of Film
    """
