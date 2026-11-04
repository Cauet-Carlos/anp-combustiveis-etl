import logging
from pathlib import Path
import pandas as pd
import re

PASTA_RAW = Path(__file__).resolve().parent.parent / "data" / "raw"
ARQUIVO = PASTA_RAW / "Preços semestrais - AUTOMOTIVOS_2025.02.csv"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def leitura_dados(caminho: Path) -> pd.DataFrame:
    df = pd.read_csv(caminho, sep=';', decimal=',', dtype={"CNPJ da Revenda": str})
    linhas, colunas  = df.shape

    logging.info(f"O DataFrame foi carregado com sucesso. Total de linhas: {linhas} | Total de colunas: {colunas}")

    return df

def padronizar_colunas(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(' ', '_')
        .str.replace('-', '_')
        .str.replace(r'[^\w\s]', '', regex=True)
        .str.replace(r'_+', '_', regex=True)
    )

    assert all(re.fullmatch(r"[a-z0-9]+(_[a-z0-9]+)*", c) for c in df.columns), "Nome de coluna fora do padrão snake_case"
    
    return df


if __name__ == "__main__":
    df = leitura_dados(ARQUIVO)
    print(df.dtypes)
    print(df["CNPJ da Revenda"].str.len().value_counts())

    print("=="*30)

    print("Iniciando o processo de transformação...")
    df = padronizar_colunas(df)
    print("\nColunas padronizadas com sucesso:")
    print(list(df.columns))



