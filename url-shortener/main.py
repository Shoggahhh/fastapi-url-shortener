from fastapi import (
    FastAPI,
    Request,
    HTTPException,
    status,
    Depends,
)
from fastapi.responses import RedirectResponse
from typing import Annotated
from schemas.short_url import ShortUrl
from schemas.movie import Movie


app = FastAPI(title="URL Shortener")


@app.get("/")
def read_root(
    requests: Request,
    name: str = "World",
):
    docs_url = requests.url.replace(
        path="/docs",
        query="",
    )
    return {
        "message": f"Hello {name}!",
        "docs": str(docs_url),
    }


SHORT_URLS = [
    ShortUrl(
        target_url="https://example.com/",
        slug="example",
    ),
    ShortUrl(
        target_url="https://google.com/",
        slug="search",
    ),
]


@app.get("/short-urls/", response_model=list[ShortUrl])
def read_short_url_list():
    return SHORT_URLS


def prefetch_short_url(
    slug: str,
) -> ShortUrl:
    url: ShortUrl | None = next(
        (url for url in SHORT_URLS if url.slug == slug),
        None,
    )
    if url:
        return url

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"URL {slug!r} not found",
    )


@app.get("/r/{slug}")
@app.get("/r/{slug}/")
def redirect_short_url(
    url: Annotated[
        ShortUrl,
        Depends(prefetch_short_url),
    ],
):
    return RedirectResponse(
        url=url.target_url,
    )


@app.get("/short-urls/{slug}/", response_model=ShortUrl)
def read_short_url_detail(
    url: Annotated[
        ShortUrl,
        Depends(prefetch_short_url),
    ],
) -> ShortUrl:
    return url


MOVIES = [
    Movie(
        movie_id=301,
        name="Matrix",
        description="some desc",
        rating="9.5",
        age_rating="18+",
        url="https://www.kinopoisk.ru/film/301/",
    ),
    Movie(
        movie_id=328,
        name="Lord of the rings",
        description="some desc",
        rating="10",
        age_rating="18+",
        url="https://www.kinopoisk.ru/film/328/",
    ),
]


@app.get("/movies/", response_model=list[Movie])
def get_all_movies():
    return MOVIES


def prefetch_movie(id: int):
    movie: Movie | None = next(
        (movie for movie in MOVIES if movie.movie_id == id), None
    )
    if movie:
        return movie
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Movie on this id: {id!r} not found",
    )


@app.get("/r/movie/{id}")
@app.get("/r/movie/{id}/")
def redirect_on_movie(
    movie: Annotated[
        Movie,
        Depends(prefetch_movie),
    ],
):
    return RedirectResponse(url=movie.url)


@app.get("/movie/{id}", response_model=Movie)
def get_movie_id(movie: Annotated[Movie, Depends(prefetch_movie)]) -> Movie:
    return movie
