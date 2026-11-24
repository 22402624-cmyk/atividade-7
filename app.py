"""Dashboard Streamlit com os gráficos da atividade 06.

Execute com:  streamlit run app.py
"""
import re
from pathlib import Path

import streamlit as st

import analises

# ---------------------------------------------------------------------------
# DADOS DO ALUNO  -> edite estas três linhas com as suas informações
# ---------------------------------------------------------------------------
NOME_ALUNO = "Heitor Alves Cardoso"
NUMERO_CHAMADA = "00"  # <-- coloque o seu número da chamada
TURMA = "Sua Turma"  # <-- coloque a sua turma
# ---------------------------------------------------------------------------

PASTA_GRAFICOS = Path(__file__).resolve().parent / "graficos"

GRAFICOS = [
    ("Vendas por categoria e região", "barras", "Comparação", analises.barras),
    ("Evolução diária das vendas", "linhas", "Tendência", analises.linhas),
    ("Faturamento por canal", "pizza", "Composição", analises.pizza),
    ("Chamados por tipo", "frequencia", "Frequência", analises.frequencia),
    ("Idade dos clientes", "distribuicao", "Distribuição", analises.distribuicao),
    ("Salário por departamento", "boxplot", "Distribuição", analises.boxplot),
    ("Altura × peso", "dispersao", "Relação", analises.dispersao),
    ("Gasto × renda", "regressao", "Relação", analises.regressao),
    ("Movimento por dia e horário", "heatmap", "Padrão", analises.heatmap),
]

CSS = """
<style>
.block-container {padding-top: 4rem; max-width: 1500px;}
.hero {background: linear-gradient(135deg,#4F46E5,#0EA5A4); color: white;
       padding: 1.6rem 2rem; border-radius: 16px; margin-bottom: 1.5rem;}
.hero h1 {color: white; margin: 0; font-size: 2rem; padding: 0;}
.hero p {margin: .3rem 0 0; opacity: .9;}
.tag {display:inline-block; font-size:.72rem; font-weight:600; letter-spacing:.04em;
      text-transform:uppercase; color:#4F46E5; background:#EEF0FF;
      padding:.15rem .55rem; border-radius:999px;}
div[data-testid="stVerticalBlockBorderWrapper"] {border-radius: 14px;}
.analise {min-height: 7.5rem; font-size: .88rem; color: #555B70;}
</style>
"""


@st.dialog("Gráfico ampliado", width="large")
def ampliar(titulo: str, arquivo: str) -> None:
    st.subheader(titulo)
    st.image(str(PASTA_GRAFICOS / f"{arquivo}.png"))


def cartao(titulo: str, arquivo: str, tag: str, analise) -> None:
    with st.container(border=True):
        st.markdown(f'<span class="tag">{tag}</span>', unsafe_allow_html=True)
        st.markdown(f"**{titulo}**")
        caminho = PASTA_GRAFICOS / f"{arquivo}.png"
        if caminho.exists():
            st.image(str(caminho))
        else:
            st.error(f"Imagem não encontrada: {caminho.name}. Rode scripts/gerar_todos.py.")
        html = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", analise())
        st.markdown(f'<div class="analise">{html}</div>', unsafe_allow_html=True)
        if caminho.exists() and st.button("🔍 Ampliar", key=f"b_{arquivo}", use_container_width=True):
            ampliar(titulo, arquivo)


def main() -> None:
    st.set_page_config(page_title="Dashboard de Gráficos", page_icon="📊", layout="wide")
    st.markdown(CSS, unsafe_allow_html=True)

    with st.sidebar:
        st.header("👤 Aluno")
        st.markdown(f"**Nome:** {NOME_ALUNO}  \n**Nº da chamada:** {NUMERO_CHAMADA}  \n**Turma:** {TURMA}")
        st.divider()
        tipos = sorted({g[2] for g in GRAFICOS})
        filtro = st.multiselect("Filtrar por tipo de análise", tipos, default=tipos)
        colunas_n = st.radio("Gráficos por linha", [1, 2, 3], index=2, horizontal=True)

    st.markdown(
        '<div class="hero"><h1>📊 Visualização de Dados</h1>'
        "<p>Atividade 06 · 9 gráficos gerados a partir de 9 arquivos CSV, "
        "com análises calculadas automaticamente dos dados.</p></div>",
        unsafe_allow_html=True)

    itens = [g for g in GRAFICOS if g[2] in filtro]
    if not itens:
        st.info("Selecione ao menos um tipo de análise na barra lateral.")
    for ini in range(0, len(itens), colunas_n):
        cols = st.columns(colunas_n, gap="medium")
        for col, item in zip(cols, itens[ini:ini + colunas_n]):
            with col:
                cartao(*item)


if __name__ == "__main__":
    main()
