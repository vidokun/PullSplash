import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from backend.config import HOST, PORT, DOWNLOADS_DIR, BACKEND_DIR
from backend.routes.search import router as search_router
from backend.routes.download import router as download_router
from backend.routes.auth import router as auth_router
from backend.routes.update import router as update_router

app = FastAPI(title="PullSplash")

app.include_router(search_router)
app.include_router(download_router)
app.include_router(auth_router)
app.include_router(update_router)

app.mount("/downloads", StaticFiles(directory=str(DOWNLOADS_DIR)), name="downloads")


def _load_html() -> str:
    html_path = BACKEND_DIR / "templates" / "index.html"
    with open(html_path) as f:
        return f.read()


@app.get("/", response_class=HTMLResponse)
async def index():
    return _load_html()


@app.get("/api/health")
async def health_check():
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run("backend.main:app", host=HOST, port=PORT, reload=True)
