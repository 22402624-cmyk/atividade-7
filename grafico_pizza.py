"""Rosca (pizza): participação de cada canal no faturamento."""
from estilo import COR_TEXTO, COR_TEXTO_SUAVE, CORES, ler_dados, nova_figura, salvar, titulo

df = ler_dados("pizza").sort_values("faturamento", ascending=False).reset_index(drop=True)
total = df["faturamento"].sum()
share = df["faturamento"] / total

fig, ax = nova_figura()
ax.pie(df["faturamento"], colors=CORES[:len(df)], startangle=90, counterclock=False,
       wedgeprops={"width": 0.38, "edgecolor": "white", "linewidth": 3},
       autopct=lambda p: f"{p:.1f}%" if p >= 4 else "", pctdistance=0.81,
       textprops={"color": "white", "fontsize": 13, "fontweight": "bold"})
ax.text(0, 0.07, f"R$ {total / 1000:,.0f} mil".replace(",", "."), ha="center",
        fontsize=26, fontweight="bold", color=COR_TEXTO)
ax.text(0, -0.15, "faturamento total", ha="center", fontsize=12.5, color=COR_TEXTO_SUAVE)

ax.legend(ax.patches, [f"{c}  ·  R$ {v:,.0f}".replace(",", ".")
                       for c, v in zip(df["canal_venda"], df["faturamento"])],
          frameon=False, loc="center left", bbox_to_anchor=(1.0, 0.5), fontsize=14,
          labelspacing=1.1)
titulo(ax, "Faturamento por canal de venda",
       f"{df.loc[0, 'canal_venda']} e {df.loc[1, 'canal_venda']} somam "
       f"{share[:2].sum():.0%} da receita")
ax.grid(False)
ax.axis("equal")
salvar(fig, "pizza")
