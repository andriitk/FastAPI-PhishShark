from fastapi import FastAPI
from phishark import routers
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from security.middleware import api_key_middleware

app = FastAPI(
    title="PhishShark",
    description="Author - CyberSword",
    version="1.0.0",
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    error_messages = []
    for error in exc.errors():
        if error["type"] == "value_error.missing":
            error_messages.append(f"Missing required field '{error['loc'][0]}'")
        else:
            error_messages.append(error["msg"])
    error_message = ", ".join(error_messages)
    return JSONResponse(
        status_code=422,
        content={"detail": f"Validation error: {error_message}"}
    )


app.include_router(routers.router)
app.middleware("http")(api_key_middleware)
