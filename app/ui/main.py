"""Interface Streamlit para Excel Sales Automation."""

import streamlit as st

from app.core.config import settings

# Configuração da página
st.set_page_config(
    page_title="Excel Sales Automation",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Sidebar
with st.sidebar:
    st.title("Excel Automation")
    st.markdown("---")
    
    st.subheader("Configurações")
    st.info(f"**Ambiente:** {settings.environment}")
    st.info(f"**Modelo LLM:** {settings.openai_model}")
    st.info(f"**Temperatura:** {settings.llm_temperature}")
    
    st.markdown("---")
    st.caption(f"Versão 0.1.0")

# Main Page
st.title("Excel Sales Automation")
st.markdown("Sistema de automação de planilhas Excel com processamento determinístico")

st.markdown("---")

# Seção de boas-vindas
col1, col2 = st.columns([2, 1])

with col1:
    st.header("Bem-vindo")
    st.markdown("""
    Este sistema permite processar planilhas Excel desorganizadas e gerar:
    
    - Dados limpos processados com Pandas
    - Sub-planilhas organizadas
    - Gráficos automáticos
    - Interpretação de colunas via LLM
    
    ### Como usar:
    1. Faça upload da planilha Excel
    2. O sistema identifica as colunas automaticamente
    3. Processa os dados deterministicamente
    4. Gera resultados e visualizações
    """)
    
with col2:
    st.info("""
    **Regra de Ouro:**
    
    O LLM é usado APENAS para:
    - Interpretação de intenção
    - Mapeamento de colunas
    
    NUNCA para cálculos com dados.
    
    Todos os cálculos são feitos via Pandas.
    """)

st.markdown("---")

# Seção de upload
st.header("Upload de Planilha")

with st.expander("Fazer Upload", expanded=True):
    uploaded_file = st.file_uploader(
        "Escolha um arquivo Excel",
        type=settings.allowed_extensions,
        help=f"Tamanho máximo: {settings.max_file_size_mb}MB"
    )
    
    if uploaded_file is not None:
        st.success(f"Arquivo carregado: {uploaded_file.name}")
        st.info("Funcionalidade de processamento em desenvolvimento")
        
        st.subheader("Preview")
        st.markdown("_Em desenvolvimento..._")
    else:
        st.warning("Nenhum arquivo selecionado")

st.markdown("---")

# Status da API
st.header("Status da API")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="Ambiente",
        value=settings.environment.upper(),
        delta="Operacional" if settings.debug else "Produção"
    )

with col2:
    st.metric(
        label="Limite de Arquivo",
        value=f"{settings.max_file_size_mb} MB",
    )

with col3:
    st.metric(
        label="Modelo LLM",
        value=settings.openai_model.split("-")[0].upper(),
        delta="Online"
    )

# Debug info (apenas em development)
if settings.environment == "development":
    with st.expander("Debug Info"):
        st.json({
            "data_raw_dir": str(settings.data_raw_dir),
            "data_processed_dir": str(settings.data_processed_dir),
            "api_host": settings.api_host,
            "api_port": settings.api_port,
        })

st.markdown("---")
st.caption("Sistema local (Docker) | Python 3.11+")
