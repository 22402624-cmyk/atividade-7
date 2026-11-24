"""Barras agrupadas: vendas médias por categoria e região."""
import seaborn as sns

from estilo import CORES, ler_dados, nova_figura, salvar, titulo

df = ler_dados("barras")
media_reg = df.groupby("regiao")["vendas_medias"].mean()

fig, ax = nova_figura()
sns.barplot(data=df, x="categoria", y="vendas_medias", hue="regiao",
            palette=CORES[:df["regiao"].nunique()], ax=ax)
for container in ax.containers:
    ax.bar_label(container, fmt="%.0f", padding=3, fontsize=10)

titulo(ax, "Vendas médias por categoria e região",
       f"Região {media_reg.idxmax()} lidera (média {media_reg.max():.0f}); "
       f"{media_reg.idxmin()} tem a menor ({media_reg.min():.0f})")
ax.set_xlabel("")
ax.set_ylabel("Vendas médias")
ax.set_ylim(0, df["vendas_medias"].max() * 1.15)
ax.legend(title="Região", frameon=False, ncol=df["regiao"].nunique(),
          loc="upper center", bbox_to_anchor=(0.5, -0.1))
ax.grid(axis="x", visible=False)
sns.despine(left=True)
salvar(fig, "barras")
