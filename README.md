# ANP Combustíveis ETL

Pipeline ETL com dados abertos de preços de combustíveis da ANP (Agência Nacional do Petróleo, Gás Natural e Biocombustíveis), usando Python, pandas e PostgreSQL.

> **Status:** em desenvolvimento. A exploração dos dados está concluída e o pipeline está sendo construído.

## Objetivo

Extrair a série histórica de preços de combustíveis automotivos, tratar os dados e carregá-los em um banco PostgreSQL modelado para análise, com foco em comparar **Manaus/AM** com a média nacional.

## Fonte dos dados

[ANP: Série Histórica de Preços de Combustíveis (dados abertos)](https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/serie-historica-de-precos-de-combustiveis)

Arquivo utilizado: combustíveis automotivos, 2º semestre de 2025.

| Item       -   Valor |
| Registros  -   384.208 |
| Colunas    -   16 |
| Período    -   01/07/2025 a 31/12/2025 |
| Produtos   -   Gasolina, Gasolina Aditivada, Etanol, Diesel, Diesel S10, GNV |

## Stack

Python • pandas • PostgreSQL • SQL • Git/GitHub

## Estrutura do projeto

```
anp-combustiveis-etl/
├── data/
│   ├── raw/          
│   └── processed/    
├── docs/             
├── notebooks/        
├── sql/             
├── src/              
├── requirements.txt
└── README.md
```

## Principais achados da exploração

- O CSV usa `;` como separador e vírgula como decimal
- O CNPJ precisa ser lido como texto para não perder o zero à esquerda
- A coluna `Valor de Compra` está 100% vazia e será descartada
- O GNV é cobrado em R$/m³ e os demais em R$/litro, então não podem ser comparados diretamente
- Não há linhas duplicadas e não há preços inválidos
- Manaus tem 3.903 registros, o que garante cobertura suficiente para a análise local

Detalhes completos em [`docs/exploracao.md`](docs/exploracao.md).

## Roadmap

- [x] Ambiente virtual e estrutura do projeto
- [x] Exploração e diagnóstico dos dados
- [ ] Extração (`extract.py`)
- [ ] Transformação e limpeza (`transform.py`)
- [ ] Modelagem do banco e criação das tabelas (`schema.sql`)
- [ ] Carga no PostgreSQL (`load.py`)
- [ ] Verificações de qualidade de dados e log de execução
- [ ] Consultas analíticas em SQL
- [ ] Diagrama do fluxo e resultados neste README

## Como rodar (ambiente)

```bash
python -m venv venv
venv\Scripts\activate.bat      # Windows (CMD)
pip install -r requirements.txt
```

O arquivo de dados deve ser baixado da página da ANP e colocado em `data/raw/`. A etapa de download automático será implementada no `extract.py`.

## Autor

Cauet Carlos • [GitHub](https://github.com/Cauet-Carlos)
