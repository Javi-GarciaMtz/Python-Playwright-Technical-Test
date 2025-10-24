from pydantic import BaseModel

class AmazonLoginResponse(BaseModel):
    status: str
    page_title: str