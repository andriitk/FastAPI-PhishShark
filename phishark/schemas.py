from pydantic import BaseModel, validator
import requests
import validators


class UrlCheck(BaseModel):
    url: str

    @validator('url')
    def valid_url(cls, v: str) -> str:
        if validators.url(v):
            try:
                result = requests.head(v)
                return v
            except Exception:
                raise ValueError("Your url address is not access!")
        raise ValueError("Your url address is not valid!")

        #     except Exception:
        #         raise HTTPException(
        #             status_code=422,
        #             detail="Your url address is not access."
        #         )
        # raise HTTPException(
        #     status_code=422,
        #     detail="Your url address is not valid!"
        # )
