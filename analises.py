"""Gera as análises exibidas no dashboard diretamente dos CSVs (sem números fixos no texto)."""
from pathlib import Path

import pandas as pd
from scipy import stats

DADOS = Path(__file__).resolve().parent / "dados"


def _ler(nome: str, **kw) -> pd.DataFrame:
    return pd.read_csv(DADOS / f"dados_{nome}.csv", **kw)


def _br(v: float, casas: int = 0) -> str:
    return f"{v:,.{casas}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def barras() -> str:
    df = _ler("barras")
    reg, cat = df.groupby("regiao")["vendas_medias"].mean(), df.groupby("categoria")["vendas_medias"].mean()
    mx, mn = df.loc[df["vendas_medias"].idxmax()], df.loc[df["vendas_medias"].idxmin()]
    return (f"A região **{reg.idxmax()}** lidera (média {reg.max():.0f}) e **{reg.idxmin()}** "
            f"tem a menor ({reg.min():.0f}). Entre as categorias, **{cat.idxmax()}** se destaca "
            f"({cat.max():.0f}). Melhor resultado: {mx.categoria} em {mx.regiao} ({mx.vendas_medias:.0f}); "
            f"pior: {mn.categoria} em {mn.regiao} ({mn.vendas_medias:.0f}).")


def linhas() -> str:
    df = _ler("linhas", parse_dates=["data"])
    mes, loja = df.groupby(df["data"].dt.month)["vendas"].mean(), df.groupby("loja")["vendas"].mean()
    return (f"**Forte tendência de alta** no trimestre: a média mensal vai de {mes.iloc[0]:.0f} "
            f"para {mes.iloc[-1]:.0f}. As lojas andam juntas ({loja.index[0]}: {loja.iloc[0]:.0f}; "
            f"{loja.index[1]}: {loja.iloc[1]:.0f}) e se alternam na liderança.")


def pizza() -> str:
    df = _ler("pizza").sort_values("faturamento", ascending=False)
    t, p = df["faturamento"].sum(), df["faturamento"] / df["faturamento"].sum()
    return (f"Do faturamento de R$ {_br(t)}, **{df.iloc[0].canal_venda}** responde por {_br(p.iloc[0]*100,1)}% "
            f"e **{df.iloc[1].canal_venda}** por {_br(p.iloc[1]*100,1)}%: juntos, {p.iloc[:2].sum():.0%}. "
            f"O canal menos relevante é {df.iloc[-1].canal_venda} ({_br(p.iloc[-1]*100,1)}%).")


def frequencia() -> str:
    f = _ler("frequencia")["tipo_atendimento"].value_counts()
    p = f / f.sum()
    return (f"**{f.index[0]}** é o tipo mais comum ({_br(p.iloc[0]*100,1)}% dos {f.sum()} chamados), "
            f"seguido de {f.index[1]} ({_br(p.iloc[1]*100,1)}%). {f.index[-1]} é o menos frequente "
            f"({_br(p.iloc[-1]*100,1)}%). Cancelamentos somam {_br(p.get('Cancelamento', 0)*100,1)}%: "
            "ponto de atenção para retenção.")


def distribuicao() -> str:
    i = _ler("distribuicao")["idade"]
    forma = "assimetria à direita (mais clientes jovens, com cauda de mais velhos)" \
        if i.mean() > i.median() else "distribuição aproximadamente simétrica"
    return (f"Idade média de {_br(i.mean(),1)} anos e mediana {i.median():.0f}: {forma}. "
            f"**{(i <= 35).mean():.0%}** têm até 35 anos e só {(i > 55).mean():.0%} passam de 55.")


def boxplot() -> str:
    df = _ler("boxplot")
    m = df.groupby("departamento")["salario"].median().sort_values(ascending=False)
    return (f"**{m.index[0]}** e **{m.index[1]}** pagam mais (medianas de R$ {_br(m.iloc[0])} e "
            f"R$ {_br(m.iloc[1])}) que {m.index[2]} e {m.index[3]} (cerca de R$ {_br(m.iloc[2:].mean())}). "
            f"O maior salário observado é R$ {_br(df['salario'].max())}.")


def dispersao() -> str:
    df = _ler("dispersao")
    r = df["altura_cm"].corr(df["peso_kg"])
    g = df.groupby("sexo")[["altura_cm", "peso_kg"]].mean()
    return (f"**Correlação positiva forte** (r = {_br(r,2)}): quanto maior a altura, maior o peso. "
            + " ".join(f"{s}: {row.altura_cm:.0f} cm / {row.peso_kg:.0f} kg." for s, row in g.iterrows()))


def regressao() -> str:
    df = _ler("regressao")
    r = stats.linregress(df["renda_mensal"], df["gasto_mensal"])
    return (f"**R² = {_br(r.rvalue**2,2)}**: a renda explica quase toda a variação do gasto. "
            f"Cada R$ 1,00 a mais de renda aumenta o gasto em cerca de R$ {_br(r.slope,2)}; "
            f"em média as pessoas gastam {(df.gasto_mensal.sum()/df.renda_mensal.sum()):.0%} do que ganham.")


def heatmap() -> str:
    df = _ler("heatmap")
    d = df.groupby("dia_semana")["movimento_clientes"].sum().sort_values(ascending=False)
    pico, vale = df.loc[df["movimento_clientes"].idxmax()], df.loc[df["movimento_clientes"].idxmin()]
    return (f"**{d.index[0]} ({d.iloc[0]}) e {d.index[1]} ({d.iloc[1]})** são os dias mais cheios; "
            f"**{d.index[-1]}** é o mais vazio. Pico: {pico.dia_semana} às {pico.horario} "
            f"({pico.movimento_clientes}); menor movimento: {vale.dia_semana} às {vale.horario} "
            f"({vale.movimento_clientes}).")
