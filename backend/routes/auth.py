from fastapi import APIRouter

from backend.models import ApiKeyRequest, ApiKeyStatus
from backend.unsplash_core import save_api_key, load_api_key

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.get("/status", response_model=ApiKeyStatus)
async def auth_status():
    key = load_api_key()
    return ApiKeyStatus(configured=key is not None and len(key) > 0)


@router.post("/key")
async def set_api_key(request: ApiKeyRequest):
    save_api_key(request.access_key)
    return {"success": True}


@router.delete("/key")
async def reset_api_key():
    import os
    from backend.config import API_KEY_FILE
    try:
        os.remove(API_KEY_FILE)
    except FileNotFoundError:
        pass
    return {"success": True}
