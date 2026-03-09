from fastapi import APIRouter
from fastapi.responses import FileResponse, Response

router = APIRouter()


@router.get("/robots.txt", response_class=Response)
async def robots() -> Response:
    content = "User-agent: *\nAllow: /\nSitemap: https://probresolve.com/sitemap.xml\n"
    return Response(content, media_type="text/plain")


@router.get("/sitemap.xml")
async def sitemap() -> FileResponse:
    return FileResponse("sitemap.xml", media_type="application/xml")
