import httpx


async def check_redirects(url: str):
    red_urls = []

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, follow_redirects=True)
            if url != response.url:
                red_urls.append(str(response.url))
            for i in response.history:
                red_urls.append(str(i.url))
            return red_urls

        except Exception as error:
            if isinstance(error, httpx.NetworkError):
                return 'Connection error'
            elif isinstance(error, httpx.TimeoutException):
                return 'Timeout error'
            else:
                return 'Unknown error'
