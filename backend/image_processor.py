from io import BytesIO
from typing import Optional, Tuple

from PIL import Image


FORMAT_MAP = {
    "jpg": ("JPEG", "image/jpeg", ".jpg"),
    "jpeg": ("JPEG", "image/jpeg", ".jpg"),
    "png": ("PNG", "image/png", ".png"),
    "webp": ("WEBP", "image/webp", ".webp"),
}


def process_image(
    image_bytes: bytes,
    output_format: str = "",
    quality: Optional[int] = None,
    width: Optional[int] = None,
    height: Optional[int] = None,
) -> Tuple[bytes, str, str]:
    img = Image.open(BytesIO(image_bytes))
    orig_w, orig_h = img.size

    # Resize: if only one dimension given, auto-calculate the other
    if width and not height:
        height = round(width * orig_h / orig_w)
    elif height and not width:
        width = round(height * orig_w / orig_h)

    if width and height:
        img = img.resize((width, height), Image.LANCZOS)

    fmt = output_format.lower() if output_format else ""
    if fmt in FORMAT_MAP:
        pil_format, content_type, ext = FORMAT_MAP[fmt]
    else:
        pil_format = img.format or "JPEG"
        content_type = f"image/{pil_format.lower()}"
        ext = f".{pil_format.lower()}"

    # Handle RGBA → RGB for JPEG (JPEG doesn't support alpha)
    if pil_format == "JPEG" and img.mode in ("RGBA", "P"):
        img = img.convert("RGB")

    save_kwargs: dict = {}
    if quality is not None and pil_format in ("JPEG", "WEBP"):
        save_kwargs["quality"] = quality
    if pil_format == "PNG":
        save_kwargs["optimize"] = True

    out = BytesIO()
    img.save(out, format=pil_format, **save_kwargs)
    return out.getvalue(), content_type, ext
