# Exploração dos dados ANP

## Visão geral
- Arquivo: preços-semestrais-automotivos_2025.02.csv (ANP, série histórica de combustíveis automotivos)
- Linhas / colunas: 384.208 / 16
- Período coberto: 01/07/2025 a 31/12/2025
- Linhas de Manaus: 3.903
- Postos distintos em Manaus: (preencher)

## Como abrir o arquivo
- Separador: `;`
- Decimal: `,`
- Encoding: utf-8 (o padrão funcionou)
- Extra: `dtype={"CNPJ da Revenda": str}`

## Produtos
GASOLINA, GASOLINA ADITIVADA, ETANOL, DIESEL, DIESEL S10 (todos em R$/litro) e GNV (R$/m³).

## Preços
Sem zeros e nem negativos. Faixa por produto entre 3,09 (etanol) e 9,59 (gasolina aditivada). (Conclusão sobre os máximos: preencher)

## Problemas encontrados
| Coluna | Problema | O que fazer no transform |
|--------|----------|--------------------------|
| Nomes das colunas | Espaços, hífens e maiúsculas | Padronizar para snake_case |
| CNPJ da Revenda | Lido como número, perde o zero | Ler como texto; o arquivo já traz 14 dígitos |
| Valor de Venda | Lido como texto por causa da vírgula | Ler com decimal="," |
| Valor de Compra | 100% vazia | Descartar a coluna |
| Complemento | ~77% nulo | Manter como opcional ou descartar |
| Numero Rua | Mistura números com S/N e SN | Padronizar o "sem número" |
| Data da Coleta | Vem como texto | Converter com format="%d/%m/%Y" |
| Unidade de Medida | GNV em m³, resto em litro | Guardar a unidade no produto; não misturar na análise |
| Produto | DIESEL e DIESEL S10 separados | Decidir se mantém separados |

## Perguntas para a próxima etapa
- Os preços máximos são reais (regiões remotas) ou erro?
- Manter DIESEL e DIESEL S10 separados na dim_produto?
- Manter ou descartar Complemento?