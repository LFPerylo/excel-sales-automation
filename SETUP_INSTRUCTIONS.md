# Instruções de Setup

## Pré-requisitos

- Python 3.11+
- Docker e Docker Compose (opcional)
- Poetry (opcional)

## Setup Local (sem Docker)

### 1. Instalar Poetry

```bash
# Windows (PowerShell)
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -

# Linux/macOS
curl -sSL https://install.python-poetry.org | python3 -
```

### 2. Configurar Projeto

```bash
cd excel-sales-automation

# Com Poetry
poetry install

# OU com pip
pip install -r requirements.txt
```

### 3. Configurar Variáveis

```bash
cp ENV_TEMPLATE.txt .env
# Edite .env e adicione OPENAI_API_KEY
```

### 4. Executar

```bash
# Terminal 1: API
uvicorn app.api.routes:app --reload --host 0.0.0.0 --port 8000

# Terminal 2: UI
streamlit run app/ui/main.py --server.port 8501
```

Acesse:
- API: http://localhost:8000
- Docs: http://localhost:8000/docs
- UI: http://localhost:8501

## Setup com Docker (Recomendado)

### 1. Configurar

```bash
cp ENV_TEMPLATE.txt .env
# Edite .env
```

### 2. Build e Executar

```bash
cd docker
docker-compose build
docker-compose up -d

# Ver logs
docker-compose logs -f

# Parar
docker-compose down
```

Acesse:
- API: http://localhost:8000
- Docs: http://localhost:8000/docs
- UI: http://localhost:8501

### 3. Hot Reload

Volumes mapeados permitem hot-reload:
- Edite arquivos em `app/`
- Mudanças refletidas automaticamente

## Testes

```bash
# Com Poetry
poetry run pytest

# Com pip
pytest

# Com cobertura
pytest --cov=app --cov-report=html
```

## Ferramentas de Dev

### Formatação

```bash
black app/ tests/
isort app/ tests/
```

### Type Checking

```bash
mypy app/
```

### Linting

```bash
flake8 app/ tests/
```

## Opções de LLM

### OpenAI Cloud

```env
OPENAI_API_KEY=sk-proj-your-key
OPENAI_MODEL=gpt-4o-mini
```

### LM Studio Local

1. Instale: https://lmstudio.ai
2. Carregue modelo (ex: llama-3.1-8b-instruct)
3. Inicie servidor (porta 1234)
4. Configure:

```env
OPENAI_API_KEY=lm-studio
OPENAI_API_BASE=http://localhost:1234/v1
OPENAI_MODEL=llama-3.1-8b-instruct
```

### Ollama Local

```bash
ollama pull llama3
ollama serve
```

```env
OPENAI_API_KEY=ollama
OPENAI_API_BASE=http://localhost:11434/v1
OPENAI_MODEL=llama3
```

## Troubleshooting

### OPENAI_API_KEY obrigatória

```bash
cp ENV_TEMPLATE.txt .env
# Configure a chave no .env
```

### Module not found

```bash
poetry install
# ou
pip install -r requirements.txt
```

### Docker não encontra volumes

```bash
docker-compose down -v
docker-compose up --build
```

### Hot Reload não funciona

Certifique-se de usar target `development`:

```yaml
build:
  target: development
```

## Próximos Passos

1. Configure o ambiente
2. Implemente ingestion.py
3. Implemente engine.py
4. Configure agente LLM
5. Desenvolva UI
6. Escreva testes
