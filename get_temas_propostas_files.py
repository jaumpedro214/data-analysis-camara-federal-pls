import requests
import pandas as pd
import json
import time
import logging

MAX_YEAR = 2023
MIN_YEAR = 1990
BASE_URL = f"https://dadosabertos.camara.leg.br/arquivos/proposicoesTemas/json/"#proposicoesTemas-{}.json"

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(
    level=logging.INFO,
    format=LOG_FORMAT,
)


if __name__ == "__main__":

    logger = logging.getLogger(__name__)
    logger.info("Iniciando script - get_propostas_camara.py")

    proposicoes_temas = []

    for year in range(MIN_YEAR, MAX_YEAR + 1):
        logger.info(f"Fazendo requisição para o ano de {year}")
        response = requests.get(f"{BASE_URL}proposicoesTemas-{year}.json")
        if response.status_code == 200:
            response_json = response.json()
            data = response_json["dados"]
            
            if not data:
                logger.info(f"Não há proposições para o ano de {year}")
                break
            
            logger.info(f"Total de proposições para o ano de {year}: {len(data)}")
            proposicoes_temas = proposicoes_temas + data
        else:
            logger.error(f"Erro na requisição. Status code: {response.status_code}")

    logger.info(f"Total de proposições: {len(proposicoes_temas)}")

    with open("./data/proposicoes_temas.json", "w") as f:
        json.dump(proposicoes_temas, f)
