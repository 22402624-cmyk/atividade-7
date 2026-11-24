"""Mapa de calor: movimento de clientes por dia da semana e horário."""
import seaborn as sns

from estilo import MAPA_CALOR, ler_dados, nova_figura, salvar, titulo

DIAS = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]

df = ler_dados("heatmap")
matriz = df.pivot(index="dia_semana", columns="horario",
                  values="movimento_clientes").loc[DIAS]
total_dia = matriz.sum(axis=1)

fig, ax = nova_figura()
sns.heatmap(matriz, annot=True, fmt="d", cmap=MAPA_CALOR, linewidths=2,
            linecolor="white", annot_kws={"fontsize": 12}, square=False,
            cbar_kws={"label": "Clientes", "shrink": 0.85}, ax=ax)

titulo(ax, "Movimento de clientes por dia e horário",
       f"{total_dia.idxmax()} e {total_dia.drop(total_dia.idxmax()).idxmax()} "
       "concentram o maior movimento")
ax.set_xlabel("Horário")
ax.set_ylabel("")
ax.tick_params(axis="y", rotation=0, left=False)
ax.tick_params(axis="x", bottom=False)
ax.grid(False)
salvar(fig, "heatmap")
