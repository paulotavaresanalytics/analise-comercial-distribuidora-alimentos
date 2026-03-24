from __future__ import annotations

from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = BASE_DIR / 'data' / 'raw'
PROCESSED_DIR = BASE_DIR / 'data' / 'processed'
REPORTS_DIR = BASE_DIR / 'reports'
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)


def carregar_bases() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    clientes = pd.read_csv(RAW_DIR / 'clientes.csv', parse_dates=['data_cadastro'])
    produtos = pd.read_csv(RAW_DIR / 'produtos.csv')
    pedidos = pd.read_csv(RAW_DIR / 'pedidos.csv', parse_dates=['data_pedido'])
    metas = pd.read_csv(RAW_DIR / 'metas_mensais.csv')
    return clientes, produtos, pedidos, metas


def meta_vs_realizado(pedidos: pd.DataFrame, metas: pd.DataFrame) -> pd.DataFrame:
    mensal = pedidos.assign(ano_mes=pedidos['data_pedido'].dt.to_period('M').astype(str)) \
                   .groupby('ano_mes', as_index=False)['valor_total'].sum() \
                   .rename(columns={'valor_total': 'realizado_vendas'})
    df = metas.merge(mensal, on='ano_mes', how='left').fillna({'realizado_vendas': 0})
    df['atingimento_%'] = np.round((df['realizado_vendas'] / df['meta_vendas']) * 100, 2)
    df['desvio_meta'] = np.round(df['realizado_vendas'] - df['meta_vendas'], 2)
    return df


def curva_abc_clientes(pedidos: pd.DataFrame) -> pd.DataFrame:
    abc = pedidos.groupby('cliente_id', as_index=False)['valor_total'].sum().sort_values('valor_total', ascending=False)
    abc['participacao_%'] = abc['valor_total'] / abc['valor_total'].sum() * 100
    abc['participacao_acumulada_%'] = abc['participacao_%'].cumsum()
    abc['classe_abc'] = pd.cut(
        abc['participacao_acumulada_%'],
        bins=[0, 80, 95, 100],
        labels=['A', 'B', 'C'],
        include_lowest=True,
        right=True,
    )
    return abc


def churn_mensal(pedidos: pd.DataFrame) -> pd.DataFrame:
    pedidos = pedidos.copy()
    pedidos['ano_mes'] = pedidos['data_pedido'].dt.to_period('M').astype(str)
    meses = sorted(pedidos['ano_mes'].unique())
    registros = []

    ativos_por_mes = pedidos.groupby('ano_mes')['cliente_id'].apply(set).to_dict()

    for i in range(1, len(meses)):
        mes_anterior = meses[i - 1]
        mes_atual = meses[i]
        base_anterior = ativos_por_mes[mes_anterior]
        base_atual = ativos_por_mes[mes_atual]
        churn_clientes = len(base_anterior - base_atual)
        base_clientes = len(base_anterior)
        taxa = round((churn_clientes / base_clientes) * 100, 2) if base_clientes else 0
        registros.append({
            'ano_mes': mes_atual,
            'clientes_mes_anterior': base_clientes,
            'clientes_perdidos': churn_clientes,
            'taxa_churn_%': taxa,
        })
    return pd.DataFrame(registros)


def ticket_medio(pedidos: pd.DataFrame) -> pd.DataFrame:
    df = pedidos.copy()
    df['ano_mes'] = df['data_pedido'].dt.to_period('M').astype(str)
    return df.groupby('ano_mes', as_index=False).agg(
        faturamento=('valor_total', 'sum'),
        pedidos=('pedido_id', 'nunique')
    ).assign(ticket_medio=lambda x: np.round(x['faturamento'] / x['pedidos'], 2))


def previsao_vendas(meta_realizado: pd.DataFrame, periodos_futuros: int = 3) -> pd.DataFrame:
    serie = meta_realizado[['ano_mes', 'realizado_vendas']].copy()
    serie['data_ref'] = pd.to_datetime(serie['ano_mes'] + '-01')
    serie['indice'] = np.arange(len(serie))
    coef = np.polyfit(serie['indice'], serie['realizado_vendas'], 1)
    meses_futuros = []
    ultimo_indice = int(serie['indice'].max())
    ultima_data = serie['data_ref'].max()

    for i in range(1, periodos_futuros + 1):
        novo_indice = ultimo_indice + i
        previsao = np.polyval(coef, novo_indice)
        nova_data = ultima_data + pd.DateOffset(months=i)
        meses_futuros.append({
            'ano_mes': nova_data.strftime('%Y-%m'),
            'previsao_vendas': round(float(previsao), 2)
        })
    return pd.DataFrame(meses_futuros)


def mix_produtos(pedidos: pd.DataFrame, produtos: pd.DataFrame) -> pd.DataFrame:
    mix = pedidos.merge(produtos[['produto_id', 'produto_nome', 'categoria']], on='produto_id', how='left')
    resumo = mix.groupby(['categoria', 'produto_nome'], as_index=False).agg(
        faturamento=('valor_total', 'sum'),
        volume=('quantidade', 'sum')
    ).sort_values('faturamento', ascending=False)
    resumo['participacao_faturamento_%'] = np.round(resumo['faturamento'] / resumo['faturamento'].sum() * 100, 2)
    return resumo


def gerar_grafico_meta(df: pd.DataFrame) -> None:
    plt.figure(figsize=(11, 5))
    plt.plot(df['ano_mes'], df['meta_vendas'], marker='o', label='Meta')
    plt.plot(df['ano_mes'], df['realizado_vendas'], marker='o', label='Realizado')
    plt.xticks(rotation=45)
    plt.title('Meta vs Realizado por Mês')
    plt.ylabel('R$')
    plt.legend()
    plt.tight_layout()
    plt.savefig(REPORTS_DIR / 'meta_vs_realizado.png', dpi=150)
    plt.close()


def exportar_insights(meta_df: pd.DataFrame, abc_df: pd.DataFrame, churn_df: pd.DataFrame, ticket_df: pd.DataFrame, previsao_df: pd.DataFrame, mix_df: pd.DataFrame) -> None:
    melhor_mes = meta_df.sort_values('atingimento_%', ascending=False).iloc[0]
    pior_mes = meta_df.sort_values('atingimento_%', ascending=True).iloc[0]
    classe_a = abc_df[abc_df['classe_abc'] == 'A']['cliente_id'].nunique()
    churn_medio = round(churn_df['taxa_churn_%'].mean(), 2)
    ticket_geral = round(ticket_df['ticket_medio'].mean(), 2)
    top_categoria = mix_df.groupby('categoria', as_index=False)['faturamento'].sum().sort_values('faturamento', ascending=False).iloc[0]
    previsao_final = previsao_df.iloc[-1]

    texto = f"""# Resumo Executivo — Insights Comerciais

## Principais achados

- O melhor desempenho de **Meta vs Realizado** ocorreu em **{melhor_mes['ano_mes']}**, com atingimento de **{melhor_mes['atingimento_%']}%**.
- O mês com pior desempenho foi **{pior_mes['ano_mes']}**, com atingimento de **{pior_mes['atingimento_%']}%**.
- A carteira classe **A** da Curva ABC concentra os clientes mais relevantes para o faturamento, totalizando **{classe_a} clientes**.
- A **taxa média de churn mensal** ficou em **{churn_medio}%**.
- O **ticket médio mensal** da operação foi de aproximadamente **R$ {ticket_geral:,.2f}**.
- A categoria com maior participação no faturamento foi **{top_categoria['categoria']}**.
- A previsão indica vendas de aproximadamente **R$ {previsao_final['previsao_vendas']:,.2f}** em **{previsao_final['ano_mes']}**.

## Recomendações analíticas

1. Priorizar ações comerciais com clientes classe A e desenvolver planos de retenção para contas estratégicas.
2. Acompanhar o churn mensal por segmento e região para antecipar perda de clientes.
3. Trabalhar campanhas de aumento de ticket médio em contas com bom potencial de recompra.
4. Cruzar mix de produtos com margem e giro para orientar negociações e promoções.
5. Refinar a previsão de vendas com variáveis de sazonalidade, região e canal de venda.
"""
    (REPORTS_DIR / 'insights.md').write_text(texto, encoding='utf-8')


def main() -> None:
    clientes, produtos, pedidos, metas = carregar_bases()

    meta_df = meta_vs_realizado(pedidos, metas)
    abc_df = curva_abc_clientes(pedidos)
    churn_df = churn_mensal(pedidos)
    ticket_df = ticket_medio(pedidos)
    previsao_df = previsao_vendas(meta_df)
    mix_df = mix_produtos(pedidos, produtos)

    meta_df.to_csv(PROCESSED_DIR / 'meta_vs_realizado.csv', index=False)
    abc_df.to_csv(PROCESSED_DIR / 'curva_abc_clientes.csv', index=False)
    churn_df.to_csv(PROCESSED_DIR / 'churn_mensal.csv', index=False)
    ticket_df.to_csv(PROCESSED_DIR / 'ticket_medio.csv', index=False)
    previsao_df.to_csv(PROCESSED_DIR / 'previsao_vendas.csv', index=False)
    mix_df.to_csv(PROCESSED_DIR / 'mix_produtos.csv', index=False)

    gerar_grafico_meta(meta_df)
    exportar_insights(meta_df, abc_df, churn_df, ticket_df, previsao_df, mix_df)

    print('Análises concluídas com sucesso.')
    print(f'Arquivos salvos em: {PROCESSED_DIR}')


if __name__ == '__main__':
    main()
