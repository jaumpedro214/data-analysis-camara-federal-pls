import requests
import pandas as pd
import json
import time
import logging

BASE_URL = "https://dadosabertos.camara.leg.br/api/v2"

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(
    level=logging.INFO,
    format=LOG_FORMAT,
)

if __name__ == "__main__":
    logger = logging.getLogger(__name__)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(logging.Formatter(LOG_FORMAT))

    logger.addHandler(stream_handler)
    logger.info("Iniciando script - get_propostas_camara.py")

    proposicoes_path = "./data/proposicoes.json"

    data = pd.read_json(proposicoes_path)
    ids = data["id"]

    data_proposicoes_temas = []
    for id in ids:
        logger.info(f"Fazendo requisição para a proposição {id}")

        response = requests.get(f"{BASE_URL}/proposicoes/{id}/temas")
        if response.status_code == 200:
            response_json = response.json()
            data = response_json["dados"]
        else:
            logger.info(
                f"Erro na requisição para a proposição {id}. Status code: {response.status_code}"
            )
            continue

        data_proposicoes_temas.append(
            {"id": id, "temas": "|".join(map(lambda x: x["tema"], data))}
        )

        # time.sleep(0.1)

    with open("./data/proposicoes_temas.json", "w") as f:
        json.dump(data_proposicoes_temas, f)