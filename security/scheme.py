from fastapi.security import APIKeyHeader
from config import API_KEY_NAME

api_key_scheme = APIKeyHeader(name=API_KEY_NAME, auto_error=False)
