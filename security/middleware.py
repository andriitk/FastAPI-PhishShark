from fastapi import HTTPException, Request, Response, status
from config import API_KEY_NAME, API_KEY
from fastapi.responses import JSONResponse


def verify_api_key(api_key: str, expected_api_key: str):
    if not api_key or api_key != expected_api_key:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key.")


async def api_key_middleware(request: Request, call_next):
    api_key = request.headers.get(API_KEY_NAME)
    try:
        verify_api_key(api_key, API_KEY)
    except HTTPException as exc:
        response = JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})
        return response
    response = await call_next(request)
    return response
