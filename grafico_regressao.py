"""Regressão linear: gasto mensal em função da renda mensal."""
import seaborn as sns
from scipy import stats

from estilo import (COR_DESTAQUE, COR_PRINCIPAL, COR_TEXTO, formatar_milhar,
                    ler_dados, nova_figura, salvar, titulo)

df = ler_dados("regressao")
res = stats.linregress(df["renda_mensal"], df["gasto_mensal"])

fig, ax = nova_figura()
sns.regplot(data=df, x="renda_mensal", y="gasto_mensal", ci=95,
            scatter_kws={"alpha": 0.6, "s": 60, "color": COR_PRINCIPAL, "edgecolor": "white"},
            line_kws={"color": COR_DESTAQUE, "linewidth": 3}, ax=ax)

ax.text(0.97, 0.06, f"gasto = {res.slope:.2f} × renda + {res.intercept:.0f}\nR² = {res.rvalue ** 2:.3f}",
        transform=ax.transAxes, ha="right", va="bottom", fontsize=13, color=COR_TEXTO,
        bbox={"boxstyle": "round,pad=0.6", "facecolor": "white", "edgecolor": "#E6E8F0"})

titulo(ax, "Regressão linear: gasto × renda",
       f"A renda explica {res.rvalue ** 2:.0%} da variação do gasto: "
       f"cada R\\$ 1 a mais gera R\\$ {res.slope:.2f} de gasto")
ax.set_xlabel("Renda mensal (R$)")
ax.set_ylabel("Gasto mensal (R$)")
ax.xaxis.set_major_formatter(formatar_milhar)
ax.yaxis.set_major_formatter(formatar_milhar)
sns.despine(left=True)
salvar(fig, "regressao")
