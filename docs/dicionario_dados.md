# Dicionário de Dados

## clientes.csv

- `cliente_id`: identificador único do cliente
- `cliente_nome`: nome fictício do cliente
- `segmento`: tipo de cliente (supermercado, atacarejo, mercearia, restaurante, distribuidor regional)
- `estado`: UF do cliente
- `regiao`: região geográfica
- `data_cadastro`: data de cadastro do cliente
- `status_ativo`: indica se o cliente está ativo no período final da base

## produtos.csv

- `produto_id`: identificador único do produto
- `produto_nome`: nome fictício do produto
- `categoria`: categoria do produto
- `subcategoria`: agrupamento secundário
- `preco_unitario`: preço médio unitário
- `custo_unitario`: custo estimado

## pedidos.csv

- `pedido_id`: identificador do pedido
- `data_pedido`: data do pedido
- `cliente_id`: chave do cliente
- `produto_id`: chave do produto
- `quantidade`: quantidade vendida
- `preco_unitario`: preço unitário praticado na venda
- `valor_total`: faturamento do item no pedido
- `canal_venda`: canal comercial
- `vendedor`: responsável pela venda
- `estado_entrega`: UF da entrega

## metas_mensais.csv

- `ano_mes`: competência mensal
- `meta_vendas`: meta comercial total do mês
