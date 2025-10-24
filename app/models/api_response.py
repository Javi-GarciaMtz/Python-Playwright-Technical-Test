from typing import Dict, Any, Optional
from pydantic import BaseModel


class ApiResponse(BaseModel):
    """Modelo base para respuestas de la API"""
    code: int = 200
    success: bool = True
    message: str
    data: Optional[Dict[str, Any]] = None
