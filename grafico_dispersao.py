"""Dispersão: altura × peso, colorido por sexo."""
import seaborn as sns

from estilo import CORES, ler_dados, nova_figura, salvar, titulo

df = ler_dados("dispersao")
r = df["altura_cm"].corr(df["peso_kg"])

fig, ax = nova_figura()
sns.scatterplot(data=df, x="altura_cm", y="peso_kg", hue="sexo", style="sexo",
                s=90, alpha=0.75, palette=CORES[:2], edgecolor="white", ax=ax)

titulo(ax, "Relação entre altura e peso",
       f"Correlação positiva forte (r = {r:.2f}): quem é mais alto tende a pesar mais")
ax.set_xlabel("Altura (cm)")
ax.set_ylabel("Peso (kg)")
ax.legend(title="Sexo", frameon=False, loc="lower right")
sns.despine(left=True)
salvar(fig, "dispersao")
