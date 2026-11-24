"""Estilo compartilhado por todos os gráficos (paleta, tema, tamanho e salvamento)."""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap

RAIZ = Path(__file__).resolve().parent.parent
PASTA_DADOS = RAIZ / "dados"
PASTA_GRAFICOS = RAIZ / "graficos"

# Paleta única para o projeto inteiro
CORES = ["#4F46E5", "#0EA5A4", "#F59E0B", "#EF4444", "#8B5CF6", "#64748B"]
COR_PRINCIPAL = CORES[0]
COR_DESTAQUE = "#EF4444"
COR_APAGADA = "#C7CBE0"
COR_TEXTO = "#1F2340"
COR_TEXTO_SUAVE = "#6B7080"
COR_GRADE = "#E6E8F0"
MAPA_CALOR = LinearSegmentedColormap.from_list(
    "indigo", ["#F4F5FF", "#B9BDF5", "#4F46E5", "#1E1B6B"])

FIGSIZE = (11, 6.5)  # mesmo tamanho para todos: a grade do dashboard fica alinhada


def aplicar_tema() -> None:
    sns.set_theme(style="whitegrid", context="talk", palette=CORES, rc={
        "axes.edgecolor": COR_GRADE,
        "axes.labelcolor": COR_TEXTO_SUAVE,
        "axes.titlecolor": COR_TEXTO,
        "axes.titleweight": "bold",
        "axes.titlesize": 19,
        "axes.titlelocation": "left",
        "axes.titlepad": 26,
        "axes.labelsize": 13,
        "grid.color": COR_GRADE,
        "grid.linewidth": 1,
        "text.color": COR_TEXTO,
        "xtick.color": COR_TEXTO_SUAVE,
        "ytick.color": COR_TEXTO_SUAVE,
        "xtick.labelsize": 12,
        "ytick.labelsize": 12,
        "legend.fontsize": 12,
        "legend.title_fontsize": 12,
    })


aplicar_tema()


def ler_dados(nome: str, **kwargs) -> pd.DataFrame:
    return pd.read_csv(PASTA_DADOS / f"dados_{nome}.csv", **kwargs)


def nova_figura(**kwargs):
    fig, ax = plt.subplots(figsize=FIGSIZE, **kwargs)
    return fig, ax


def titulo(ax, texto: str, subtitulo: str | None = None) -> None:
    """Título à esquerda com um subtítulo (a conclusão do gráfico) logo abaixo."""
    ax.set_title(texto, loc="left")
    if subtitulo:
        ax.text(0, 1.02, subtitulo, transform=ax.transAxes, fontsize=12.5,
                color=COR_TEXTO_SUAVE, va="bottom")


def formatar_milhar(v: float, _=None) -> str:
    return f"{v:,.0f}".replace(",", ".")


def salvar(fig, nome: str) -> None:
    PASTA_GRAFICOS.mkdir(exist_ok=True)
    fig.tight_layout()
    saida = PASTA_GRAFICOS / f"{nome}.png"
    fig.savefig(saida, dpi=150, facecolor="white")
    plt.close(fig)
    print(f"Gráfico salvo em {saida}")
