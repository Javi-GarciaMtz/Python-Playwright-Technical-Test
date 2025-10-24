from fastapi import APIRouter
from app.models.api_response import ApiResponse

router = APIRouter(prefix="/hello", tags=["hello world"])

@router.get("/", summary="Hello world endpoint", response_model=ApiResponse)
def hello_world():
    return ApiResponse(
        message="hello world! :)",
    )
