# Análise de Dados Comerciais — Distribuidora de Alimentos

Projeto completo de análise de dados comerciais com **dados fictícios e ilustrativos** de uma **distribuidora brasileira de alimentos de grande porte**. O objetivo é simular um cenário real de tomada de decisão comercial a partir de indicadores estratégicos amplamente utilizados por equipes de vendas, controladoria e inteligência comercial.

## Objetivo do projeto

Este projeto foi desenvolvido para demonstrar, de forma prática, como analisar a performance comercial de uma distribuidora de alimentos por meio de métricas essenciais para gestão:

- **Meta vs Realizado**
- **Curva ABC de Clientes**
- **Churn de Clientes**
- **Ticket Médio**
- **Previsão de Vendas**
- **Mix de Produtos**

## Contexto de negócio

A empresa simulada atua na distribuição de alimentos em larga escala, atendendo supermercados, atacarejos, mercearias, redes regionais e pequenos varejistas em diversas regiões do Brasil. O projeto busca responder perguntas como:

- A equipe comercial está batendo a meta?
- Quais clientes concentram maior parte da receita?
- Qual é a taxa de perda de clientes ao longo do tempo?
- Qual é o valor médio por pedido?
- Como prever vendas futuras com base no histórico?
- Qual é a participação de cada categoria no faturamento?

## Estrutura do repositório

```bash
projeto_comercial_distribuicao_alimentos/
│
├── data/
│   ├── raw/                    # Base sintética original
│   └── processed/              # Bases tratadas / outputs analíticos
│
├── notebooks/
│   └── analise_comercial.ipynb # Notebook principal
│
├── src/
│   ├── generate_data.py        # Geração dos dados fictícios
│   └── analysis.py             # Cálculo das métricas e exportações
│
├── reports/
│   └── insights.md             # Resumo executivo com principais achados
│
├── docs/
│   └── dicionario_dados.md     # Dicionário dos campos
│
├── requirements.txt
├── .gitignore
└── README.md
```

## Tecnologias utilizadas

- Python 3.11+
- pandas
- numpy
- matplotlib
- openpyxl
- jupyter

## Como executar o projeto

### 1) Clone o repositório

```bash
git clone https://github.com/seu-usuario/projeto_comercial_distribuicao_alimentos.git
cd projeto_comercial_distribuicao_alimentos
```

### 2) Crie e ative um ambiente virtual

```bash
python -m venv .venv
```

**Windows:**
```bash
.venv\Scripts\activate
```

**Linux / macOS:**
```bash
source .venv/bin/activate
```

### 3) Instale as dependências

```bash
pip install -r requirements.txt
```

### 4) Gere os dados fictícios

```bash
python src/generate_data.py
```

### 5) Execute a análise

```bash
python src/analysis.py
```

### 6) Abra o notebook

```bash
jupyter notebook notebooks/analise_comercial.ipynb
```

## Métricas analisadas

### 1. Meta vs Realizado
Compara o valor planejado de vendas por mês com o valor efetivamente vendido, permitindo identificar desvios de performance.

### 2. Curva ABC de Clientes
Classifica os clientes de acordo com sua participação no faturamento acumulado:
- **Classe A**: clientes que representam a maior fatia da receita
- **Classe B**: clientes intermediários
- **Classe C**: clientes de menor participação

### 3. Churn
Calcula a taxa de clientes que deixaram de comprar em determinado período, auxiliando a gestão de retenção.

### 4. Ticket Médio
Mostra o valor médio por pedido, ajudando a acompanhar rentabilidade comercial e comportamento de compra.

### 5. Previsão de Vendas
Aplica uma projeção simples baseada em tendência histórica mensal para estimar vendas futuras.

### 6. Mix de Produtos
Avalia a participação das categorias e produtos no faturamento total, permitindo decisões sobre portfólio, sortimento e foco comercial.

## Fontes de dados

Os dados deste projeto são **100% fictícios**, criados apenas para fins educacionais e de portfólio.

Arquivos principais gerados:
- `data/raw/clientes.csv`
- `data/raw/produtos.csv`
- `data/raw/pedidos.csv`
- `data/raw/metas_mensais.csv`

## Exemplos de insights possíveis

- A empresa pode estar vendendo bem, mas abaixo da meta em regiões específicas.
- Poucos clientes podem concentrar grande parte do faturamento.
- O churn pode estar aumentando em carteiras com ticket menor.
- Certas categorias podem ter grande participação no volume, mas baixa margem.
- A previsão de vendas pode indicar sazonalidade em determinados meses.

## Possíveis evoluções do projeto

- Criar dashboard no Power BI
- Adicionar segmentação por região e vendedor
- Incluir análise de margem por cliente
- Aplicar modelos estatísticos ou machine learning para previsão
- Simular campanhas comerciais e impacto nas vendas
