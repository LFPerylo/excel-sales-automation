# Excel Sales Automation

Sistema de automação de planilhas Excel com processamento determinístico e interpretação por LLM.

## Visão Geral

Sistema local (Docker) que:
1. Ingere planilhas Excel desorganizadas
2. Limpa dados deterministicamente com Pandas
3. Gera sub-planilhas e gráficos automaticamente

### Regra de Ouro: LLM ≠ Cálculos

O componente LLM é estritamente restrito a:
- Interpretação de intenção do usuário
- Mapeamento de colunas do Excel
- NUNCA toca nos dados brutos para cálculos

Todos os cálculos são feitos via Pandas de forma determinística e auditável.

## Quick Start

### Com Docker (Recomendado)

```bash
cp ENV_TEMPLATE.txt .env
# Edite .env e adicione sua OPENAI_API_KEY

cd docker
docker-compose up -d

# Acesse:
# API: http://localhost:8000/docs
# UI:  http://localhost:8501
```

### Local com Poetry

```bash
poetry install
cp ENV_TEMPLATE.txt .env
# Edite .env

# Terminal 1
poetry run uvicorn app.api.routes:app --reload

# Terminal 2
poetry run streamlit run app/ui/main.py
```

## Estrutura do Projeto

```
excel-sales-automation/
├── app/
│   ├── api/              # API REST (FastAPI)
│   ├── core/             # Motor de processamento
│   ├── llm/              # Componente LLM (limitado)
│   └── ui/               # Interface Streamlit
├── data/
│   ├── raw/              # Planilhas originais
│   └── processed/        # Resultados
├── docker/               # Configuração Docker
├── tests/                # Testes unitários
└── pyproject.toml        # Dependências
```

## Stack Tecnológico

- Python 3.11+
- Poetry (gerenciamento de dependências)
- FastAPI (backend)
- Streamlit (frontend)
- Pandas (processamento de dados)
- OpenPyXL (leitura/escrita Excel)
- LangChain Core (LLM - interpretação apenas)
- Docker (containerização)

## Configuração

Todas as configurações via arquivo `.env`:

```env
OPENAI_API_KEY=sk-your-key-here
OPENAI_MODEL=gpt-4o-mini
MAX_FILE_SIZE_MB=50
ALLOWED_EXTENSIONS=.xlsx,.xls,.xlsm
```

Veja `ENV_TEMPLATE.txt` para referência completa.

## Desenvolvimento

```bash
# Testes
make test

# Formatação
make format

# Linting
make lint

# Todos os comandos
make help
```

## Roadmap

### Fase 1: Setup (Concluída)
- [x] Estrutura de pastas
- [x] Configuração com Pydantic Settings
- [x] Docker multi-stage
- [x] Documentação

### Fase 2: Core
- [ ] Implementar ingestion.py
- [ ] Implementar engine.py
- [ ] Implementar security.py

### Fase 3: LLM
- [ ] Implementar agent.py
- [ ] Definir prompts.py
- [ ] Criar tools.py

### Fase 4: API & UI
- [ ] Endpoints de upload e processamento
- [ ] Interface completa Streamlit
- [ ] Integração end-to-end

### Fase 5: Testes
- [ ] Testes unitários (>80% coverage)
- [ ] Testes de integração
- [ ] Documentação de API

## Licença

MIT License

## Contribuindo

Princípios do projeto:
1. LLM NUNCA toca dados brutos (apenas interpretação)
2. Type hints estritos em todo código
3. Docstrings no padrão Google
4. Clareza sobre "cleverness"
5. Testes com cobertura mínima de 80%
