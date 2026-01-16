# Makefile - Excel Sales Automation

.PHONY: help install dev test format lint docker-build docker-up docker-down clean

# Cores
CYAN := \033[0;36m
GREEN := \033[0;32m
YELLOW := \033[0;33m
NC := \033[0m

# Configurações
POETRY := poetry
PYTEST := $(POETRY) run pytest
BLACK := $(POETRY) run black
ISORT := $(POETRY) run isort
MYPY := $(POETRY) run mypy
FLAKE8 := $(POETRY) run flake8
APP_DIR := app
TESTS_DIR := tests
DOCKER_DIR := docker

help: ## Mostra comandos disponíveis
	@echo "$(CYAN)Excel Sales Automation - Comandos$(NC)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "$(GREEN)%-20s$(NC) %s\n", $$1, $$2}'

# Setup & Instalação
install: ## Instala dependências
	@echo "$(CYAN)Instalando dependências...$(NC)"
	$(POETRY) install
	@echo "$(GREEN)Dependências instaladas$(NC)"

install-dev: ## Instala dependências + dev
	@echo "$(CYAN)Instalando dependências de dev...$(NC)"
	$(POETRY) install --with dev
	@echo "$(GREEN)Dependências de dev instaladas$(NC)"

setup: install ## Setup inicial
	@echo "$(CYAN)Configurando projeto...$(NC)"
	@if [ ! -f .env ]; then \
		cp ENV_TEMPLATE.txt .env; \
		echo "$(YELLOW)Arquivo .env criado. Configure suas variáveis$(NC)"; \
	else \
		echo "$(GREEN)Arquivo .env já existe$(NC)"; \
	fi
	@echo "$(GREEN)Setup concluído$(NC)"

# Desenvolvimento
dev: ## Inicia API + UI
	@echo "$(CYAN)Iniciando ambiente de desenvolvimento...$(NC)"
	@$(MAKE) -j2 dev-api dev-ui

dev-api: ## Inicia API
	@echo "$(CYAN)Iniciando API na porta 8000...$(NC)"
	$(POETRY) run uvicorn $(APP_DIR).api.routes:app --reload --host 0.0.0.0 --port 8000

dev-ui: ## Inicia UI
	@echo "$(CYAN)Iniciando UI na porta 8501...$(NC)"
	$(POETRY) run streamlit run $(APP_DIR)/ui/main.py --server.port 8501

shell: ## Abre shell Poetry
	@echo "$(CYAN)Abrindo shell...$(NC)"
	$(POETRY) shell

# Testes
test: ## Executa testes
	@echo "$(CYAN)Executando testes...$(NC)"
	$(PYTEST) -v

test-cov: ## Testes com cobertura
	@echo "$(CYAN)Testes com cobertura...$(NC)"
	$(PYTEST) --cov=$(APP_DIR) --cov-report=term-missing --cov-report=html
	@echo "$(GREEN)Relatório em htmlcov/index.html$(NC)"

test-watch: ## Testes em modo watch
	@echo "$(CYAN)Testes em modo watch...$(NC)"
	$(PYTEST) -f

# Qualidade de Código
format: ## Formata código
	@echo "$(CYAN)Formatando código...$(NC)"
	$(BLACK) $(APP_DIR) $(TESTS_DIR)
	$(ISORT) $(APP_DIR) $(TESTS_DIR)
	@echo "$(GREEN)Código formatado$(NC)"

format-check: ## Verifica formatação
	@echo "$(CYAN)Verificando formatação...$(NC)"
	$(BLACK) --check $(APP_DIR) $(TESTS_DIR)
	$(ISORT) --check-only $(APP_DIR) $(TESTS_DIR)

lint: ## Executa linting
	@echo "$(CYAN)Executando linting...$(NC)"
	$(FLAKE8) $(APP_DIR) $(TESTS_DIR)
	@echo "$(GREEN)Flake8 passou$(NC)"
	$(MYPY) $(APP_DIR)
	@echo "$(GREEN)MyPy passou$(NC)"

check: format-check lint test ## Verifica tudo
	@echo "$(GREEN)Todas verificações passaram$(NC)"

# Docker
docker-build: ## Build Docker
	@echo "$(CYAN)Building Docker images...$(NC)"
	cd $(DOCKER_DIR) && docker-compose build
	@echo "$(GREEN)Imagens criadas$(NC)"

docker-up: ## Inicia containers
	@echo "$(CYAN)Iniciando containers...$(NC)"
	cd $(DOCKER_DIR) && docker-compose up -d
	@echo "$(GREEN)Containers iniciados$(NC)"
	@echo "$(YELLOW)API: http://localhost:8000$(NC)"
	@echo "$(YELLOW)UI:  http://localhost:8501$(NC)"

docker-down: ## Para containers
	@echo "$(CYAN)Parando containers...$(NC)"
	cd $(DOCKER_DIR) && docker-compose down
	@echo "$(GREEN)Containers parados$(NC)"

docker-logs: ## Mostra logs
	@echo "$(CYAN)Logs dos containers...$(NC)"
	cd $(DOCKER_DIR) && docker-compose logs -f

docker-clean: docker-down ## Para e remove volumes
	@echo "$(CYAN)Limpando containers e volumes...$(NC)"
	cd $(DOCKER_DIR) && docker-compose down -v
	@echo "$(GREEN)Cleanup concluído$(NC)"

docker-rebuild: docker-clean docker-build docker-up ## Rebuild completo

# Limpeza
clean: ## Remove arquivos temporários
	@echo "$(CYAN)Limpando temporários...$(NC)"
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	rm -rf htmlcov/ .coverage 2>/dev/null || true
	@echo "$(GREEN)Limpeza concluída$(NC)"

clean-data: ## Remove dados (CUIDADO)
	@echo "$(RED)ATENÇÃO: Remove TODOS os dados$(NC)"
	@read -p "Confirma? (y/N): " confirm; \
	if [ "$$confirm" = "y" ] || [ "$$confirm" = "Y" ]; then \
		rm -rf data/raw/* data/processed/*; \
		echo "$(GREEN)Dados removidos$(NC)"; \
	else \
		echo "$(YELLOW)Cancelado$(NC)"; \
	fi

# Utilitários
deps-update: ## Atualiza dependências
	@echo "$(CYAN)Atualizando dependências...$(NC)"
	$(POETRY) update
	@echo "$(GREEN)Dependências atualizadas$(NC)"

deps-show: ## Lista dependências
	@echo "$(CYAN)Dependências instaladas:$(NC)"
	$(POETRY) show --tree

info: ## Informações do projeto
	@echo "$(CYAN)Informações do Projeto$(NC)"
	@echo "$(GREEN)Python:$(NC) $$($(POETRY) run python --version)"
	@echo "$(GREEN)Poetry:$(NC) $$($(POETRY) --version)"
	@echo ""
	@echo "$(CYAN)Portas$(NC)"
	@echo "$(GREEN)API:$(NC) http://localhost:8000"
	@echo "$(GREEN)UI:$(NC)  http://localhost:8501"

# CI/CD
ci: install format-check lint test ## Pipeline CI
	@echo "$(GREEN)Pipeline CI concluído$(NC)"
