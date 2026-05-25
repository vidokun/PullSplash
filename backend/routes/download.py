import io
import os
import zipfile

import requests
from fastapi import APIRouter, HTTPException
from fastapi.responses import Response, StreamingResponse

from backend.config import DOWNLOADS_DIR
from backend.models import DownloadRequest, DownloadResponse, BrowserDownloadRequest
from backend.unsplash_core import download_photo, save_credits, _client_id, UNSPLASH_API
from backend.image_processor import process_image

router = APIRouter(prefix="/api/download", tags=["download"])


def _fetch_photo_data(photo_id: str) -> dict:
    resp = requests.get(
        f"{UNSPLASH_API}/photos/{photo_id}",
        params={"client_id": _client_id()},
    )
    resp.raise_for_status()
    return resp.json()


def _download_raw(photo: dict) -> bytes:
    url = photo["urls"]["raw"]
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.content


def _has_processing(request: DownloadRequest) -> bool:
    return bool(request.output_format or request.quality or request.resize_width or request.resize_height)


@router.post("", response_model=DownloadResponse)
async def download(request: DownloadRequest):
    downloaded = []
    failed = []
    photo_data_list = []

    for photo_id in request.photo_ids:
        try:
            photo = _fetch_photo_data(photo_id)
            photo_data_list.append(photo)

            if _has_processing(request):
                raw_bytes = _download_raw(photo)
                processed, ct, ext = process_image(
                    raw_bytes,
                    output_format=request.output_format,
                    quality=request.quality,
                    width=request.resize_width,
                    height=request.resize_height,
                )
                username = photo["user"]["username"]
                filename = f"pullsplash-{username}-{photo_id}{ext}" if request.name_scheme == 0 else f"pullsplash-{photo_id}{ext}"
                filepath = os.path.join(str(DOWNLOADS_DIR), filename)
                os.makedirs(str(DOWNLOADS_DIR), exist_ok=True)
                with open(filepath, "wb") as f:
                    f.write(processed)
            else:
                filepath = download_photo(
                    photo,
                    dest_dir=str(DOWNLOADS_DIR),
                    name_scheme=request.name_scheme,
                    width=request.width,
                )

            downloaded.append(filepath)
        except Exception:
            failed.append(photo_id)

    credits_file = None
    if request.save_credits and photo_data_list:
        credits_file = save_credits(photo_data_list, str(DOWNLOADS_DIR))

    return DownloadResponse(
        success=len(failed) == 0,
        downloaded=len(downloaded),
        failed=failed,
        files=downloaded,
        credits_file=credits_file,
    )


@router.post("/browser")
async def browser_download(request: BrowserDownloadRequest):
    if not request.photo_ids:
        raise HTTPException(status_code=400, detail="No photo IDs provided.")

    has_processing = bool(
        request.output_format or request.quality or request.resize_width or request.resize_height
    )

    if len(request.photo_ids) == 1:
        photo = _fetch_photo_data(request.photo_ids[0])
        raw = _download_raw(photo)

        if has_processing:
            processed, content_type, ext = process_image(
                raw,
                output_format=request.output_format,
                quality=request.quality,
                width=request.resize_width,
                height=request.resize_height,
            )
        else:
            processed, content_type, ext = raw, "image/jpeg", ".jpg"

        username = photo["user"]["username"]
        filename = f"pullsplash-{username}-{photo['id']}{ext}"

        return Response(
            content=processed,
            media_type=content_type,
            headers={"Content-Disposition": f'attachment; filename="{filename}"'},
        )

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        for photo_id in request.photo_ids:
            try:
                photo = _fetch_photo_data(photo_id)
                raw = _download_raw(photo)

                if has_processing:
                    processed, _, ext = process_image(
                        raw,
                        output_format=request.output_format,
                        quality=request.quality,
                        width=request.resize_width,
                        height=request.resize_height,
                    )
                else:
                    processed, ext = raw, ".jpg"

                username = photo["user"]["username"]
                filename = f"pullsplash-{username}-{photo_id}{ext}"
                zf.writestr(filename, processed)
            except Exception:
                pass

    zip_buffer.seek(0)
    return StreamingResponse(
        zip_buffer,
        media_type="application/zip",
        headers={"Content-Disposition": "attachment; filename=pullsplash-download.zip"},
    )
