from fastapi import (
    FastAPI,
    Request,
)

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
