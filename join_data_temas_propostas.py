import pandas as pd

data_proposicoes = pd.read_json("./data/proposicoes.json")
data_proposicoes_temas = pd.read_json("./data/proposicoes_temas.json")

data_proposicoes = data_proposicoes.merge(
    data_proposicoes_temas, left_on="id", right_on="id"
)


data_proposicoes.to_json("./data/proposicoes_join_temas.json", orient="records")
