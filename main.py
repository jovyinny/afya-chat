"""Main entry point for the API server."""

from src.api import app

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
