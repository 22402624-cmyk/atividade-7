"""Histograma + densidade: distribuição de idade dos clientes."""
import seaborn as sns

from estilo import (COR_DESTAQUE, COR_PRINCIPAL, CORES, ler_dados, nova_figura,
                    salvar, titulo)

df = ler_dados("distribuicao")
media, mediana = df["idade"].mean(), df["idade"].median()

fig, ax = nova_figura()
sns.histplot(data=df, x="idade", bins=15, kde=True, color=COR_PRINCIPAL,
             edgecolor="white", ax=ax)
ax.axvline(media, color=COR_DESTAQUE, linestyle="--", linewidth=2,
           label=f"Média: {media:.1f} anos")
ax.axvline(mediana, color=CORES[1], linestyle=":", linewidth=2.5,
           label=f"Mediana: {mediana:.1f} anos")

forma = "assimetria à direita" if media > mediana else "distribuição simétrica"
titulo(ax, "Distribuição de idade dos clientes",
       f"Média acima da mediana indica {forma}" if media > mediana else forma.capitalize())
ax.set_xlabel("Idade (anos)")
ax.set_ylabel("Número de clientes")
ax.legend(frameon=False)
ax.grid(axis="x", visible=False)
sns.despine(left=True)
salvar(fig, "distribuicao")
