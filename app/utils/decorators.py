import functools
from app.core.logger import logger

def catch_exceptions(func):
    """
    Decorador simple que captura excepciones en metodos.
    """
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error en {func.__name__}: {str(e)}")
            raise
    return wrapper