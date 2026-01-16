"""Configurações da aplicação usando Pydantic Settings.

Gerencia variáveis de ambiente e configurações do sistema.
Garante paths absolutos e validação de tipos.
"""

from pathlib import Path
from typing import Literal

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configurações globais da aplicação.
    
    Carrega configurações do .env ou variáveis de ambiente.
    Paths são convertidos para absolutos automaticamente.
    """
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )
    
    # Configurações de Ambiente
    environment: Literal["development", "production", "test"] = Field(
        default="development",
        description="Ambiente de execução"
    )
    debug: bool = Field(default=True, description="Modo debug")
    
    # Configurações da API
    api_host: str = Field(default="0.0.0.0", description="Host da API")
    api_port: int = Field(default=8000, description="Porta da API")
    api_reload: bool = Field(default=True, description="Hot reload da API")
    
    # Configurações da UI
    ui_host: str = Field(default="0.0.0.0", description="Host da UI")
    ui_port: int = Field(default=8501, description="Porta da UI")
    
    # Configurações de Paths
    project_root: Path = Field(
        default_factory=lambda: Path(__file__).parent.parent.parent.resolve(),
        description="Raiz do projeto (path absoluto)"
    )
    
    data_raw_dir: Path = Field(
        default=Path("data/raw"),
        description="Diretório de dados brutos (relativo à raiz)"
    )
    
    data_processed_dir: Path = Field(
        default=Path("data/processed"),
        description="Diretório de dados processados (relativo à raiz)"
    )
    
    # Configurações do LLM
    openai_api_key: str = Field(
        default="",
        description="Chave API da OpenAI (ou servidor compatível)"
    )
    
    openai_api_base: str | None = Field(
        default=None,
        description="URL base customizada para API OpenAI (ex: LM Studio)"
    )
    
    openai_model: str = Field(
        default="gpt-4o-mini",
        description="Modelo LLM a ser usado"
    )
    
    llm_temperature: float = Field(
        default=0.0,
        ge=0.0,
        le=2.0,
        description="Temperatura do LLM (0=determinístico)"
    )
    
    llm_max_tokens: int = Field(
        default=2000,
        ge=100,
        description="Máximo de tokens na resposta do LLM"
    )
    
    # Configurações de Processamento
    max_file_size_mb: int = Field(
        default=50,
        ge=1,
        description="Tamanho máximo de arquivo Excel (MB)"
    )
    
    chunk_size: int = Field(
        default=1000,
        ge=100,
        description="Tamanho do chunk para processamento em lote"
    )
    
    # Configurações de Segurança
    allowed_extensions: str | list[str] = Field(
        default=".xlsx,.xls,.xlsm",
        description="Extensões de arquivo permitidas (CSV ou JSON list)"
    )
    
    cors_origins: str | list[str] = Field(
        default="http://localhost:8501,http://localhost:3000",
        description="Origens permitidas para CORS (CSV ou JSON list)"
    )
    
    @field_validator("data_raw_dir", "data_processed_dir", mode="after")
    @classmethod
    def make_absolute_path(cls, v: Path, info) -> Path:
        """Converte paths relativos em absolutos baseados na raiz do projeto.
        
        Args:
            v: Path a ser validado
            info: Contexto de validação do Pydantic
            
        Returns:
            Path absoluto garantido
        """
        # Pega o project_root do contexto se já foi definido
        if hasattr(info, 'data') and 'project_root' in info.data:
            project_root = info.data['project_root']
        else:
            # Fallback: calcula a raiz do projeto
            project_root = Path(__file__).parent.parent.parent.resolve()
        
        if not v.is_absolute():
            v = project_root / v
        
        # Garante que o diretório existe
        v.mkdir(parents=True, exist_ok=True)
        
        return v.resolve()
    
    @field_validator("allowed_extensions", "cors_origins", mode="before")
    @classmethod
    def parse_csv_or_list(cls, v: str | list[str]) -> list[str]:
        """Converte string CSV ou JSON list para lista de strings.
        
        Args:
            v: Valor a ser convertido (CSV string ou list)
            
        Returns:
            Lista de strings
            
        Example:
            ".xlsx,.xls" -> [".xlsx", ".xls"]
            [".xlsx", ".xls"] -> [".xlsx", ".xls"]
        """
        if isinstance(v, str):
            # Remove espaços e split por vírgula
            return [item.strip() for item in v.split(",") if item.strip()]
        return v
    
    @field_validator("openai_api_key", mode="after")
    @classmethod
    def validate_api_key(cls, v: str, info) -> str:
        """Valida se a API key foi fornecida quando não está em modo de teste.
        
        Args:
            v: API key a ser validada
            info: Contexto de validação
            
        Returns:
            API key validada
            
        Raises:
            ValueError: Se API key estiver vazia em ambiente não-test
        """
        environment = info.data.get("environment", "development")
        
        if environment != "test" and not v:
            raise ValueError(
                "OPENAI_API_KEY é obrigatória para ambientes development/production. "
                "Configure no arquivo .env ou use LM Studio local."
            )
        
        return v
    
    @property
    def max_file_size_bytes(self) -> int:
        """Retorna o tamanho máximo de arquivo em bytes.
        
        Returns:
            Tamanho em bytes
        """
        return self.max_file_size_mb * 1024 * 1024
    
    def get_openai_config(self) -> dict[str, str | float | int]:
        """Retorna configuração formatada para cliente OpenAI.
        
        Returns:
            Dicionário com configurações do OpenAI
        """
        config: dict[str, str | float | int] = {
            "api_key": self.openai_api_key,
            "model": self.openai_model,
            "temperature": self.llm_temperature,
            "max_tokens": self.llm_max_tokens,
        }
        
        if self.openai_api_base:
            config["base_url"] = self.openai_api_base
        
        return config


# Singleton global - importar de qualquer lugar com `from app.core.config import settings`
settings = Settings()


def get_settings() -> Settings:
    """Factory function para dependency injection (FastAPI).
    
    Returns:
        Instância singleton das configurações
        
    Example:
        ```python
        @app.get("/config")
        def read_config(settings: Settings = Depends(get_settings)):
            return {"data_dir": str(settings.data_raw_dir)}
        ```
    """
    return settings
