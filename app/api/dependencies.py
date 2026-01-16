"""Dependências para injeção no FastAPI.

Factories e dependências reutilizáveis para uso nos endpoints.
"""

from typing import Annotated

from fastapi import Depends, Header, HTTPException, status

from app.core.config import Settings, get_settings


async def get_api_key(
    x_api_key: Annotated[str | None, Header()] = None,
    settings: Settings = Depends(get_settings),
) -> str:
    """Valida API key do header (para uso futuro).
    
    Args:
        x_api_key: API key do header X-API-Key
        settings: Configurações da aplicação
        
    Returns:
        API key validada
        
    Raises:
        HTTPException: Se API key for inválida ou ausente
        
    Example:
        ```python
        @app.get("/protected")
        async def protected_route(api_key: str = Depends(get_api_key)):
            return {"message": "Access granted"}
        ```
    """
    # Por enquanto, desabilitado - implementar quando necessário
    # if not x_api_key:
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="API key missing"
    #     )
    
    return x_api_key or "development"


# Outras dependências podem ser adicionadas aqui conforme necessário
