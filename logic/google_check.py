import httpx
from config import GOOGLE

URL = f'https://safebrowsing.googleapis.com/v4/threatMatches:find?key={GOOGLE}'


async def check_url(url):
    data = {
        "threatInfo": {
            "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING", "THREAT_TYPE_UNSPECIFIED", "UNWANTED_SOFTWARE"],
            "platformTypes": ["ALL_PLATFORMS"],
            "threatEntryTypes": ["URL"],
            "threatEntries":
                {
                    "url": f"{url}"}
        }
    }
    async with httpx.AsyncClient() as client:
        req = await client.post(URL, json=data)
        if req.json():
            return {'clear': False}
        else:
            return {'clear': True}
