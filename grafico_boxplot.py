"""Boxplot: distribuição salarial por departamento."""
import seaborn as sns

from estilo import (COR_TEXTO, CORES, formatar_milhar, ler_dados, nova_figura,
                    salvar, titulo)

df = ler_dados("boxplot")
mediana = df.groupby("departamento")["salario"].median().sort_values(ascending=False)
ordem = list(mediana.index)

fig, ax = nova_figura()
sns.boxplot(data=df, x="departamento", y="salario", order=ordem, hue="departamento",
            palette=CORES[:len(ordem)], legend=False, showfliers=False, width=0.55,
            boxprops={"alpha": 0.85}, medianprops={"color": "white", "linewidth": 2.5},
            ax=ax)
sns.stripplot(data=df, x="departamento", y="salario", order=ordem,
              color=COR_TEXTO, alpha=0.3, size=3.5, jitter=0.18, ax=ax)

for i, dep in enumerate(ordem):
    ax.text(i, df["salario"].max() * 1.03, f"mediana\nR$ {formatar_milhar(mediana[dep])}",
            ha="center", va="bottom", fontsize=11, color=COR_TEXTO)

titulo(ax, "Distribuição salarial por departamento")
ax.set_ylim(0, df["salario"].max() * 1.2)
ax.set_xlabel("")
ax.set_ylabel("Salário (R$)")
ax.yaxis.set_major_formatter(formatar_milhar)
ax.grid(axis="x", visible=False)
sns.despine(left=True)
salvar(fig, "boxplot")
