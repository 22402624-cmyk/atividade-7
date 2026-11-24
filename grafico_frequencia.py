"""Frequência: quantidade de chamados por tipo de atendimento."""
import seaborn as sns

from estilo import COR_APAGADA, COR_PRINCIPAL, ler_dados, nova_figura, salvar, titulo

df = ler_dados("frequencia")
freq = df["tipo_atendimento"].value_counts().reset_index()
freq.columns = ["tipo", "frequencia"]
total = freq["frequencia"].sum()

fig, ax = nova_figura()
cores = [COR_PRINCIPAL] + [COR_APAGADA] * (len(freq) - 1)  # destaca o mais frequente
sns.barplot(data=freq, y="tipo", x="frequencia", hue="tipo", palette=cores,
            legend=False, orient="h", ax=ax)
for barra, valor in zip(ax.patches, freq["frequencia"]):
    ax.text(barra.get_width() + total * 0.005, barra.get_y() + barra.get_height() / 2,
            f"{valor}  ({valor / total:.1%})", va="center", fontsize=12)

titulo(ax, "Frequência de chamados por tipo de atendimento",
       f"{freq.loc[0, 'tipo']} é o motivo mais comum: {freq.loc[0, 'frequencia'] / total:.0%} "
       f"dos {total} chamados")
ax.set_xlim(0, freq["frequencia"].max() * 1.22)
ax.set_xlabel("Número de chamados")
ax.set_ylabel("")
ax.grid(axis="y", visible=False)
sns.despine(left=True)
salvar(fig, "frequencia")
