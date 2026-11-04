import requests
import zipfile
import logging
from pathlib import Path

URL = "https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/arquivos/shpc/dsas/ca/ca-2025-02.zip"
PASTA_RAW = Path(__file__).resolve().parent.parent / "data" / "raw"
NOME_ARQUIVO = "ca-2025-02.zip"

# CONFIGURAÇÃO DOS LOGGINGS (REGISTROS DOS PROCESSOS)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

# FUNÇÕES PARA EXECUÇÃO COMPLETA DA EXTRAÇÃO
def baixar_arquivo(url: str, destino: Path) -> Path:
    logging.info(f"Baixando: {url}")

    destino.parent.mkdir(parents=True, exist_ok=True)
    if destino.exists():
        logging.warning(f"Arquivo já existe: {destino}")
        return destino
    
    with requests.get(url, stream=True, timeout=15) as resposta:
        resposta.raise_for_status()

        if resposta.status_code != 200:
            raise requests.HTTPError(f"Status HTTP inesperado: {resposta.status_code}")

        with open(destino, "wb") as arquivo:
            for bloco in resposta.iter_content(chunk_size=8192):
                if bloco:
                    arquivo.write(bloco)

    tamanho = destino.stat().st_size

    tamanho_mb = tamanho / (1024 * 1024)

    logging.info(
        f"Download concluído: {destino.name} | Tamanho: {tamanho_mb:.2f} MB"
    )

    return destino


def extrair_csv(arquivo_zip: Path, pasta_destino: Path) -> Path:
    with zipfile.ZipFile(arquivo_zip) as zf:
        nome_csv = zf.namelist()[0]
        zf.extract(nome_csv, pasta_destino)
    
    logging.info(f"CSV extraído: {nome_csv}")
    
    return pasta_destino / nome_csv



if __name__ == "__main__":
    zip_baixado = baixar_arquivo(URL, PASTA_RAW / NOME_ARQUIVO)
    extrair_csv(zip_baixado, PASTA_RAW)