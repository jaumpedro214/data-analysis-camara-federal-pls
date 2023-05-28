import requests
import pprint
import time
import json
import logging

BASE_URL = "https://dadosabertos.camara.leg.br/api/v2"
N_ITENS_PER_PAGE = 50
START_YEAR = 2003

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(
    level=logging.INFO,
    format=LOG_FORMAT,
)

if __name__ == "__main__":
    params = {
        "itens": N_ITENS_PER_PAGE,
        "pagina": 1,
        "ordem": "DESC",
        "ordenarPor": "ano",
        "siglaTipo": "PL",
    }
    proposicoes = []
    in_keep_querying_prepositions = True

    logger = logging.getLogger(__name__)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(logging.Formatter(LOG_FORMAT))

    logger.addHandler(stream_handler)
    logger.info("Iniciando script - get_propostas_camara.py")
    logger.info("BASIC PARAMS: " + json.dumps(params))

    while in_keep_querying_prepositions:
        response = requests.get(f"{BASE_URL}/proposicoes", params=params)

        logger.info(f'Fazendo requisição para a página {params["pagina"]}')

        if response.status_code == 200:
            response_json = response.json()
            data = response_json["dados"]

            if not data:
                logger.info("Não há mais proposições")
                break

            for proposicao in data:
                if proposicao["ano"] < START_YEAR:
                    logger.info(
                        f'Proposição {proposicao["id"]} é de {proposicao["ano"]}. Parando de fazer requisições'
                    )
                    in_keep_querying_prepositions = False
                    break

                proposicoes.append(proposicao)

        else:
            logger.error(f"Erro na requisição. Status code: {response.status_code}")
            break

        params["pagina"] += 1
        time.sleep(0.5)

    with open(f"./data/proposicoes.json", 'w') as file:
        json.dump(proposicoes, file, indent=4, ensure_ascii=False)
