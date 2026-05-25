import requests
from typing import Optional

from fastapi import APIRouter
from pydantic import BaseModel

from backend.config import VERSION, GITHUB_REPO

router = APIRouter(prefix="/api/update", tags=["update"])


class UpdateCheckResponse(BaseModel):
    update_available: bool
    current_version: str
    latest_version: Optional[str] = None
    download_url: Optional[str] = None


@router.get("/check", response_model=UpdateCheckResponse)
async def check_update():
    try:
        resp = requests.get(
            f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest",
            timeout=5,
            headers={"Accept": "application/vnd.github+json"},
        )
        if resp.status_code == 200:
            data = resp.json()
            latest = data["tag_name"].lstrip("v")
            current = VERSION.lstrip("v")
            if latest != current:
                return UpdateCheckResponse(
                    update_available=True,
                    current_version=VERSION,
                    latest_version=data["tag_name"],
                    download_url=data["html_url"],
                )
    except Exception:
        pass

    return UpdateCheckResponse(update_available=False, current_version=VERSION)
