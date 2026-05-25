from pydantic import BaseModel, Field
from typing import Optional


class ApiKeyRequest(BaseModel):
    access_key: str


class ApiKeyStatus(BaseModel):
    configured: bool


class SearchRequest(BaseModel):
    query: str = ""
    count: int = Field(default=20, ge=1, le=50)
    orientation: str = ""
    featured: bool = False
    collection_url: str = ""


class PhotoResult(BaseModel):
    id: str
    description: Optional[str] = None
    width: int
    height: int
    thumb_url: str
    full_url: str
    raw_url: str
    photographer: str
    photographer_url: str
    color: str = ""


class SearchResponse(BaseModel):
    success: bool
    total: int
    photos: list[PhotoResult] = []
    error: Optional[str] = None


class DownloadRequest(BaseModel):
    photo_ids: list[str]
    name_scheme: int = 0
    width: Optional[int] = None
    save_credits: bool = True
    output_format: str = ""
    quality: Optional[int] = Field(default=None, ge=1, le=100)
    resize_width: Optional[int] = None
    resize_height: Optional[int] = None


class DownloadResponse(BaseModel):
    success: bool
    downloaded: int = 0
    failed: list[str] = []
    files: list[str] = []
    credits_file: Optional[str] = None
    error: Optional[str] = None


class BrowserDownloadRequest(BaseModel):
    photo_ids: list[str]
    output_format: str = ""
    quality: Optional[int] = Field(default=None, ge=1, le=100)
    resize_width: Optional[int] = None
    resize_height: Optional[int] = None
