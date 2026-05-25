from fastapi import APIRouter, HTTPException

from backend.models import SearchRequest, SearchResponse, PhotoResult
from backend.unsplash_core import search_photos, search_collection

router = APIRouter(prefix="/api/search", tags=["search"])


def _build_photo(item: dict) -> PhotoResult:
    return PhotoResult(
        id=item["id"],
        description=item.get("description") or item.get("alt_description"),
        width=item["width"],
        height=item["height"],
        thumb_url=item["urls"]["thumb"],
        full_url=item["urls"]["full"],
        raw_url=item["urls"]["raw"],
        photographer=item["user"]["name"],
        photographer_url=item["user"]["links"]["html"],
        color=item.get("color", ""),
    )


@router.post("", response_model=SearchResponse)
async def search(request: SearchRequest):
    try:
        if request.collection_url:
            items = search_collection(
                collection_url=request.collection_url,
                count=request.count,
                orientation=request.orientation,
            )
        else:
            items = search_photos(
                query=request.query,
                count=request.count,
                orientation=request.orientation,
                featured=request.featured,
            )
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    photos = [_build_photo(item) for item in items]

    return SearchResponse(
        success=True,
        total=len(photos),
        photos=photos,
    )
