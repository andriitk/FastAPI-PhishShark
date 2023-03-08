from fastapi import APIRouter, Depends, HTTPException
from .schemas import UrlCheck
from logic import redirects, google_check, vt_check, url_research
import asyncio

router = APIRouter(
    tags=['main check'],
    prefix="/api/v1.0"
)


@router.get("/")
async def get_start():
    return {"Hello": "I am PhishShark"}


@router.post('/check-url')
async def main_check(url: UrlCheck):
    redirectsURL = await redirects.check_redirects(url.url)

    if isinstance(redirectsURL, list):
        url = redirectsURL[0] if redirectsURL else url.url
    else:
        url = url.url

    google = asyncio.create_task(google_check.check_url(url))
    vt = asyncio.create_task(vt_check.check_vt(url))

    research = asyncio.create_task(url_research.main(url))

    results = await asyncio.gather(research, google, vt, return_exceptions=True)

    return {
        'urlInfo': {'redirects': redirectsURL, **results[0]},
        'googleSafe': results[1],
        'virusTotal': results[2]
    }
