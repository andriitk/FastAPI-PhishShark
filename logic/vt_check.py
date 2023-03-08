import httpx

from config import VIRUS_TOTAL

API_URL = 'https://www.virustotal.com/vtapi/v2/url/report'


async def check_vt(url: str):
    message = dict()

    params = dict(apikey=VIRUS_TOTAL,
                  resource=url, scan=0)

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(API_URL, params=params, timeout=5)
            result = response.json()

            if result:
                message['permalink'] = result['permalink']
                message['countChecks'] = result['total']
                message['maliciousChecks'] = result['positives']
                if not result['positives']:
                    message['clear'] = True
                else:
                    message['clear'] = False

        except KeyError:
            message['result'] = "error"
            message['detail'] = "Resource unavailable."

    return message
