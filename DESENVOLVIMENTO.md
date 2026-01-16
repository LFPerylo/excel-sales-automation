# Guia de Desenvolvimento

## Status

Pronto para desenvolvimento | Última atualização: 2026-01-16

## Estrutura Configurada

### Arquivos de Configuração
- `pyproject.toml` - Dependências (Poetry)
- `requirements.txt` - Alternativa (pip)
- `.env` - Variáveis de ambiente
- `.vscode/settings.json` - Configuração do editor
- `Makefile` - Comandos úteis

### Aplicação
- `app/core/config.py` - Configurações (Pydantic Settings)
- `app/api/routes.py` - Endpoints FastAPI
- `app/api/dependencies.py` - Injeção de dependências
- `app/ui/main.py` - Interface Streamlit

### Docker
- `docker/Dockerfile` - Multi-stage build
- `docker/docker-compose.yml` - Orquestração

## Comandos

### Make
```bash
make help      # Lista comandos
make install   # Instala dependências
make dev       # Inicia API + UI
make test      # Testes
make format    # Formata código
make lint      # Linting
```

### Docker
```bash
docker-compose -f docker/docker-compose.yml up --build
docker-compose -f docker/docker-compose.yml down
docker-compose -f docker/docker-compose.yml logs -f
```

### Local
```bash
uvicorn app.api.routes:app --reload    # API
streamlit run app/ui/main.py           # UI
pytest                                  # Testes
```

## Portas

- API: http://localhost:8000
- Docs: http://localhost:8000/docs
- UI: http://localhost:8501

## Próximos Passos

### Fase 2: Core
1. `app/core/ingestion.py` - Leitura de Excel
2. `app/core/engine.py` - Processamento Pandas
3. `app/core/security.py` - Validações

### Fase 3: LLM
1. `app/llm/agent.py` - Interpretação
2. `app/llm/prompts.py` - Templates
3. `app/llm/tools.py` - Functions

### Fase 4: API & UI
1. Endpoint de upload
2. Endpoint de processamento
3. Interface de upload
4. Visualização de resultados

### Fase 5: Testes
1. Testes unitários (pytest)
2. Cobertura mínima 80%
3. Testes de integração

## Regras

### Regra de Ouro
LLM NUNCA toca dados brutos. Use APENAS Pandas para cálculos.

### Padrões
- Type hints obrigatórios
- Docstrings no padrão Google
- Formatação: Black + isort
- Linting: Flake8 + MyPy
- Comentários minimalistas

### Git
- Commits em português
- Mensagens descritivas
- Branches: `feature/nome`, `fix/nome`

## Troubleshooting

### OPENAI_API_KEY não configurada
```bash
cp ENV_TEMPLATE.txt .env
# Edite .env
```

### Module not found
```bash
poetry install
# ou
pip install -r requirements.txt
```

### Docker não inicia
```bash
docker-compose -f docker/docker-compose.yml down -v
docker-compose -f docker/docker-compose.yml up --build
```

## Estrutura de Dados

### Diretórios
- `data/raw/` - Planilhas originais
- `data/processed/` - Resultados

### Formatos Suportados
- `.xlsx` - Excel moderno
- `.xls` - Excel legado
- `.xlsm` - Excel com macros

## Segurança

- Validação de tamanho (50MB padrão)
- Whitelist de extensões
- CORS configurável
- Usuário não-root no Docker
- Paths validados
