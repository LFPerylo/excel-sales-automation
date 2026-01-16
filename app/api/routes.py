"""Rotas da API FastAPI.

Este módulo contém todos os endpoints HTTP da aplicação.
"""

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import Settings, get_settings

# Cria aplicação FastAPI
app = FastAPI(
    title="Excel Sales Automation",
    description="Sistema de automação de planilhas Excel com processamento determinístico",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configura CORS (deve ser feito ANTES da aplicação iniciar)
settings = get_settings()
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Endpoints

@app.get("/")
async def root() -> dict[str, str]:
    """Endpoint raiz - retorna informações básicas da API.
    
    Returns:
        Dicionário com informações da API
    """
    return {
        "name": "Excel Sales Automation API",
        "version": "0.1.0",
        "status": "operational",
        "docs": "/docs",
    }


@app.get("/health")
async def health_check(settings: Settings = Depends(get_settings)) -> dict[str, str]:
    """Healthcheck endpoint para monitoramento.
    
    Args:
        settings: Configurações injetadas via dependency injection
        
    Returns:
        Status da aplicação
    """
    return {
        "status": "healthy",
        "environment": settings.environment,
        "data_raw_dir": str(settings.data_raw_dir),
        "data_processed_dir": str(settings.data_processed_dir),
    }


@app.get("/config")
async def get_config(settings: Settings = Depends(get_settings)) -> dict[str, str | int | bool]:
    """Retorna configurações públicas (não-sensíveis) da aplicação.
    
    Args:
        settings: Configurações injetadas
        
    Returns:
        Configurações públicas
    """
    return {
        "environment": settings.environment,
        "debug": settings.debug,
        "max_file_size_mb": settings.max_file_size_mb,
        "allowed_extensions": settings.allowed_extensions,
        "llm_model": settings.openai_model,
        "llm_temperature": settings.llm_temperature,
    }


# Rotas a implementar

# @app.post("/upload")
# async def upload_excel():
#     """Faz upload de arquivo Excel para processamento."""
#     pass

# @app.post("/process")
# async def process_excel():
#     """Processa arquivo Excel com Pandas."""
#     pass

# @app.get("/results/{file_id}")
# async def get_results():
#     """Retorna resultados do processamento."""
#     pass
