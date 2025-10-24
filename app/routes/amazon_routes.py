import logging
from app.models.amazon_login_request import AmazonLoginRequest
from app.models.amazon_login_response import AmazonLoginResponse
from app.models.api_response import ApiResponse
from app.modules.amazon.service import main_shopping_flow
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/amazon", tags=["Amazon"])

@router.post("/shopping-flow", response_model=ApiResponse)
async def shopping_flow(request: AmazonLoginRequest):
    """
        Realiza la compra en Amazon utilizando las credenciales proporcionadas.

        Args:
            request (AmazonLoginRequest): Objeto con las credenciales de usuario

        Returns:
            ApiResponse: Objeto de respuesta estandarizada
    """
    try:
        result = await main_shopping_flow(request)
        return ApiResponse(
            message="Proceso finalizado correctamente",
            data = result
        )
    except Exception as e:
        return ApiResponse(
            success=False,
            code=500,
            message=str(e)
        )