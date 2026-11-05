import logging
from pathlib import Path
import pandas as pd
import re
import os

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


def conversao_tipos(df: pd.DataFrame) -> pd.DataFrame:
    df["data_da_coleta"] = pd.to_datetime(df["data_da_coleta"], format="%d/%m/%Y")

    data_min = df["data_da_coleta"].min()
    data_max = df["data_da_coleta"].max()

    logging.info(f"Período de datas analisadas: {data_min} / {data_max}")

    return df


def remocao_colunas_vazias(df: pd.DataFrame) -> pd.DataFrame:
    colunas_vazias = df.columns[df.isna().all()].to_list()
    logging.info(f"Colunas vazias identificadas para remoção: {colunas_vazias}")

    df = df.drop(columns=colunas_vazias)

    return df


def padronizar_numero_rua(df: pd.DataFrame, coluna: str = "numero_rua") -> pd.DataFrame:
    df[coluna] = df[coluna].str.strip().str.upper()

    mascara_sem_num = df[coluna].str.fullmatch(r"S\s*/?\s*NO?", na=False)

    df.loc[mascara_sem_num, coluna] = "S/N"

    total_sn = mascara_sem_num.sum()

    logging.info(
      f"Total de linhas padronizadas como 'S/N' na coluna '{coluna}':"
      f" {total_sn}"
    )

    return df






if __name__ == "__main__":
    largura_terminal = os.get_terminal_size().columns
    df = leitura_dados(ARQUIVO)
    print(df.dtypes)
    print(df["CNPJ da Revenda"].str.len().value_counts())

    print("=" * largura_terminal)

    print("Iniciando o processo de transformação...")
    df = padronizar_colunas(df)
    print("\nColunas padronizadas com sucesso:")
    print(list(df.columns))

    print("=" * largura_terminal)

    print("Iniciando o processo de conversão de tipos...")
    df = conversao_tipos(df)
    print("\nTipos de dados atualizados:")
    print(df.dtypes)

    print("=" * largura_terminal)

    print("Verificando e removendo colunas completamente vazias...")
    df = remocao_colunas_vazias(df)
    print("\nColunas restantes no DataFrame:")
    print(list(df.columns))

    print("=" * largura_terminal)

    print("Iniciando a padronização do número da rua...")
    df = padronizar_numero_rua(df, coluna="numero_rua")
    print("\nNúmero da rua padronizado com sucesso:")
    print(df["numero_rua"].value_counts().head())

   


