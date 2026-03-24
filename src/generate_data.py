from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = BASE_DIR / 'data' / 'raw'
RAW_DIR.mkdir(parents=True, exist_ok=True)

RNG = np.random.default_rng(42)


ESTADOS_REGIOES = {
    'SP': 'Sudeste', 'RJ': 'Sudeste', 'MG': 'Sudeste', 'ES': 'Sudeste',
    'PR': 'Sul', 'SC': 'Sul', 'RS': 'Sul',
    'BA': 'Nordeste', 'PE': 'Nordeste', 'CE': 'Nordeste', 'AL': 'Nordeste',
    'GO': 'Centro-Oeste', 'DF': 'Centro-Oeste', 'MT': 'Centro-Oeste',
    'PA': 'Norte', 'AM': 'Norte'
}

SEGMENTOS = ['Supermercado', 'Atacarejo', 'Mercearia', 'Restaurante', 'Distribuidor Regional']
CANAIS = ['Representante Comercial', 'Televendas', 'Key Account', 'E-commerce B2B']
VENDEDORES = ['Ana Souza', 'Bruno Lima', 'Carlos Silva', 'Daniela Rocha', 'Eduarda Melo', 'Felipe Santos']

CATEGORIAS = {
    'Arroz': ['Arroz Branco 5kg', 'Arroz Integral 1kg'],
    'Feijão': ['Feijão Carioca 1kg', 'Feijão Preto 1kg'],
    'Macarrão': ['Macarrão Espaguete 500g', 'Macarrão Parafuso 500g'],
    'Óleo': ['Óleo de Soja 900ml', 'Óleo de Girassol 900ml'],
    'Açúcar': ['Açúcar Cristal 1kg', 'Açúcar Refinado 1kg'],
    'Café': ['Café Torrado 500g', 'Café Premium 250g'],
    'Biscoitos': ['Biscoito Cream Cracker', 'Biscoito Recheado Chocolate'],
    'Lácteos': ['Leite UHT Integral 1L', 'Leite Condensado 395g'],
    'Molhos': ['Extrato de Tomate 340g', 'Molho de Tomate Tradicional'],
    'Enlatados': ['Milho Verde 170g', 'Ervilha 170g']
}

PRECOS = {
    'Arroz Branco 5kg': (22.5, 18.0),
    'Arroz Integral 1kg': (8.8, 6.4),
    'Feijão Carioca 1kg': (7.9, 5.7),
    'Feijão Preto 1kg': (8.3, 6.0),
    'Macarrão Espaguete 500g': (4.2, 2.9),
    'Macarrão Parafuso 500g': (4.4, 3.1),
    'Óleo de Soja 900ml': (7.6, 5.5),
    'Óleo de Girassol 900ml': (9.9, 7.2),
    'Açúcar Cristal 1kg': (4.8, 3.5),
    'Açúcar Refinado 1kg': (5.2, 3.8),
    'Café Torrado 500g': (16.9, 12.0),
    'Café Premium 250g': (14.6, 10.5),
    'Biscoito Cream Cracker': (4.9, 3.4),
    'Biscoito Recheado Chocolate': (3.8, 2.6),
    'Leite UHT Integral 1L': (5.6, 4.1),
    'Leite Condensado 395g': (6.8, 5.0),
    'Extrato de Tomate 340g': (3.3, 2.2),
    'Molho de Tomate Tradicional': (2.9, 2.0),
    'Milho Verde 170g': (3.9, 2.8),
    'Ervilha 170g': (4.1, 2.9),
}


def gerar_clientes(n: int = 180) -> pd.DataFrame:
    estados = list(ESTADOS_REGIOES.keys())
    clientes = []
    for i in range(1, n + 1):
        uf = RNG.choice(estados)
        clientes.append(
            {
                'cliente_id': f'C{i:04d}',
                'cliente_nome': f'Cliente {i:03d} Alimentos Ltda',
                'segmento': RNG.choice(SEGMENTOS, p=[0.35, 0.20, 0.20, 0.15, 0.10]),
                'estado': uf,
                'regiao': ESTADOS_REGIOES[uf],
                'data_cadastro': pd.Timestamp('2023-01-01') + pd.to_timedelta(int(RNG.integers(0, 730)), unit='D'),
                'status_ativo': True,
            }
        )
    return pd.DataFrame(clientes)


def gerar_produtos() -> pd.DataFrame:
    produtos = []
    idx = 1
    for categoria, nomes in CATEGORIAS.items():
        for nome in nomes:
            preco, custo = PRECOS[nome]
            produtos.append(
                {
                    'produto_id': f'P{idx:03d}',
                    'produto_nome': nome,
                    'categoria': categoria,
                    'subcategoria': categoria,
                    'preco_unitario': preco,
                    'custo_unitario': custo,
                }
            )
            idx += 1
    return pd.DataFrame(produtos)


def gerar_metas_mensais() -> pd.DataFrame:
    meses = pd.date_range('2024-01-01', '2025-12-01', freq='MS')
    base = 4_800_000
    sazonalidade = np.array([0.94, 0.96, 0.98, 1.01, 1.02, 1.05, 1.03, 1.02, 1.00, 1.04, 1.08, 1.15] * 2)
    tendencia = np.linspace(1.00, 1.18, len(meses))
    meta = base * sazonalidade * tendencia
    return pd.DataFrame({'ano_mes': meses.strftime('%Y-%m'), 'meta_vendas': np.round(meta, 2)})


def gerar_pedidos(clientes: pd.DataFrame, produtos: pd.DataFrame, n_pedidos: int = 7200) -> pd.DataFrame:
    datas = pd.date_range('2024-01-01', '2025-12-31', freq='D')
    pesos_clientes = RNG.pareto(a=2.2, size=len(clientes)) + 1
    pesos_clientes = pesos_clientes / pesos_clientes.sum()

    pesos_produtos = RNG.pareto(a=2.5, size=len(produtos)) + 1
    pesos_produtos = pesos_produtos / pesos_produtos.sum()

    clientes_prob = dict(zip(clientes['cliente_id'], pesos_clientes))
    produtos_base = produtos.set_index('produto_id')

    churn_pool = set(RNG.choice(clientes['cliente_id'], size=28, replace=False))
    cutoff_churn = pd.Timestamp('2025-08-31')

    registros = []
    for i in range(1, n_pedidos + 1):
        while True:
            cliente_id = RNG.choice(clientes['cliente_id'], p=pesos_clientes)
            data = pd.Timestamp(RNG.choice(datas))
            if cliente_id in churn_pool and data > cutoff_churn:
                continue
            break

        produto_id = RNG.choice(produtos['produto_id'], p=pesos_produtos)
        qtd = int(RNG.integers(5, 180))
        preco_base = float(produtos_base.loc[produto_id, 'preco_unitario'])
        variacao = RNG.uniform(0.94, 1.06)
        preco_venda = round(preco_base * variacao, 2)
        valor_total = round(qtd * preco_venda, 2)
        estado = clientes.loc[clientes['cliente_id'] == cliente_id, 'estado'].iloc[0]

        registros.append(
            {
                'pedido_id': f'PV{i:06d}',
                'data_pedido': data,
                'cliente_id': cliente_id,
                'produto_id': produto_id,
                'quantidade': qtd,
                'preco_unitario': preco_venda,
                'valor_total': valor_total,
                'canal_venda': RNG.choice(CANAIS, p=[0.30, 0.25, 0.20, 0.25]),
                'vendedor': RNG.choice(VENDEDORES),
                'estado_entrega': estado,
            }
        )
    pedidos = pd.DataFrame(registros).sort_values('data_pedido').reset_index(drop=True)

    ult_compra = pedidos.groupby('cliente_id')['data_pedido'].max()
    clientes['status_ativo'] = clientes['cliente_id'].map(ult_compra).ge(pd.Timestamp('2025-10-01'))
    return pedidos, clientes


if __name__ == '__main__':
    clientes = gerar_clientes()
    produtos = gerar_produtos()
    metas = gerar_metas_mensais()
    pedidos, clientes = gerar_pedidos(clientes, produtos)

    clientes.to_csv(RAW_DIR / 'clientes.csv', index=False)
    produtos.to_csv(RAW_DIR / 'produtos.csv', index=False)
    pedidos.to_csv(RAW_DIR / 'pedidos.csv', index=False)
    metas.to_csv(RAW_DIR / 'metas_mensais.csv', index=False)

    print('Arquivos gerados com sucesso em data/raw/')
