from pydantic import BaseModel, Field, EmailStr, field_validator

class AmazonLoginRequest(BaseModel):
    """
        Modelo para hacer login en Amazon.
    """
    headless: bool = Field(default=True, description="Si es True, el navegador se ejecutará en segundo plano")
    user_email: EmailStr = Field(default="", description="Correo electrónico del usuario de Amazon")
    user_pwd: str = Field(default="", description="Contraseña del usuario de Amazon")
    
    @field_validator('headless')
    @classmethod
    def validate_headless(cls, v):
        if not isinstance(v, bool):
            raise ValueError('El campo headless debe ser un booleano (True/False)')
        return v
        
    @field_validator('user_pwd')
    @classmethod
    def validate_password(cls, v):
        if not v:
            raise ValueError('La contraseña no puede estar vacía')
        return v
        