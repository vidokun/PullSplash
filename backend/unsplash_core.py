"""
Unsplash API client — ported from MehediH/PullSplash.
Uses Unsplash Official API (free tier: 50 req/hour).
"""

import json
import os
from typing import Optional

import requests

from backend.config import API_KEY_FILE

UNSPLASH_API = "https://api.unsplash.com"


def load_api_key() -> Optional[str]:
    key = os.getenv("UNSPLASH_ACCESS_KEY")
    if key:
        return key
    try:
        with open(API_KEY_FILE) as f:
            return f.read().strip()
    except FileNotFoundError:
        return None


def save_api_key(access_key: str):
    with open(API_KEY_FILE, "w") as f:
        f.write(access_key.strip())


def _client_id() -> str:
    key = load_api_key()
    if not key:
        raise ValueError("No API key configured.")
    return key


def search_photos(
    query: str,
    count: int = 20,
    orientation: str = "",
    featured: bool = False,
) -> list[dict]:
    client_id = _client_id()
    params: dict = {
        "query": query,
        "client_id": client_id,
        "count": min(count, 30),
    }
    if featured:
        params["featured"] = "true"
    if orientation in ("landscape", "portrait", "squarish"):
        params["orientation"] = orientation

    resp = requests.get(f"{UNSPLASH_API}/photos/random", params=params)
    resp.raise_for_status()
    return resp.json()


def search_collection(
    collection_url: str,
    count: int = 20,
    orientation: str = "",
) -> list[dict]:
    client_id = _client_id()
    parts = collection_url.rstrip("/").split("/")
    try:
        idx = parts.index("collections")
        collection_id = parts[idx + 1]
    except (ValueError, IndexError):
        collection_id = parts[-1]

    params: dict = {
        "client_id": client_id,
        "per_page": min(count, 30),
    }
    if orientation in ("landscape", "portrait", "squarish"):
        params["orientation"] = orientation

    resp = requests.get(
        f"{UNSPLASH_API}/collections/{collection_id}/photos",
        params=params,
    )
    resp.raise_for_status()
    return resp.json()


def track_download(photo_id: str):
    try:
        requests.get(
            f"{UNSPLASH_API}/photos/{photo_id}/download",
            params={"client_id": _client_id()},
        )
    except Exception:
        pass


def download_photo(
    photo: dict,
    dest_dir: str,
    name_scheme: int = 0,
    width: Optional[int] = None,
) -> str:
    image_url = photo["urls"]["raw"] if width else photo["urls"]["full"]
    if width:
        image_url += f"&w={width}"

    ext = ".jpg"
    if "png" in photo.get("content_type", ""):
        ext = ".png"

    if name_scheme == 0:
        username = photo["user"]["username"]
        filename = f"pullsplash-{username}-{photo['id']}{ext}"
    else:
        filename = f"pullsplash-{photo['id']}{ext}"

    filepath = os.path.join(dest_dir, filename)
    os.makedirs(dest_dir, exist_ok=True)

    resp = requests.get(image_url)
    resp.raise_for_status()

    with open(filepath, "wb") as f:
        f.write(resp.content)

    track_download(photo["id"])
    return filepath


def save_credits(photos: list[dict], dest_dir: str) -> str:
    credits = []
    seen: set[str] = set()
    for p in photos:
        user = p["user"]
        if user["username"] not in seen:
            seen.add(user["username"])
            credits.append({
                "name": user["name"],
                "username": user["username"],
                "link": user["links"]["html"],
            })

    credits_path = os.path.join(dest_dir, "pullsplash-credits.json")
    with open(credits_path, "w") as f:
        json.dump(credits, f, indent="\t")
    return credits_path
