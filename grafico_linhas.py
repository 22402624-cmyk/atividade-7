"""Linhas: vendas diárias por loja, com média móvel de 7 dias."""
import matplotlib.dates as mdates
import seaborn as sns

from estilo import (COR_DESTAQUE, COR_TEXTO, CORES, ler_dados, nova_figura,
                    salvar, titulo)

MESES = ["jan", "fev", "mar", "abr", "mai", "jun",
         "jul", "ago", "set", "out", "nov", "dez"]

df = ler_dados("linhas", parse_dates=["data"]).sort_values("data")
df["media_movel"] = df["vendas"].rolling(7, min_periods=3, center=True).mean()
primeiro, ultimo = df.groupby(df["data"].dt.month)["vendas"].mean().iloc[[0, -1]]

fig, ax = nova_figura()
sns.scatterplot(data=df, x="data", y="vendas", hue="loja", palette=CORES[:2],
                s=55, alpha=0.7, edgecolor="white", ax=ax)
ax.plot(df["data"], df["media_movel"], color=COR_TEXTO, linewidth=3,
        label="Média móvel (7 dias)")

titulo(ax, "Evolução diária das vendas por loja",
       f"Tendência de alta: média mensal sobe de {primeiro:.0f} para {ultimo:.0f} no trimestre")
ax.set_xlabel("")
ax.set_ylabel("Vendas")
ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(
    lambda v, _: (lambda d: f"{MESES[d.month - 1]}/{d.year}")(mdates.num2date(v)))
ax.legend(frameon=False, loc="upper left")
sns.despine(left=True)
salvar(fig, "linhas")
