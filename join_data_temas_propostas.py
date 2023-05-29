import pandas as pd

data_proposicoes = pd.read_json("./data/proposicoes.json")
data_proposicoes_temas = pd.read_json("./data/proposicoes_temas.json")

# Extract id from uriProposicao
data_proposicoes_temas["id"] = (
    data_proposicoes_temas["uriProposicao"]
    .apply(lambda x: x.split("/")[-1])
    .astype(int)
)

# Filter only the siglaTipo = PL
data_proposicoes_temas = data_proposicoes_temas[
    data_proposicoes_temas["siglaTipo"] == "PL"
]

# Remove columns
data_proposicoes_temas = data_proposicoes_temas.drop(
    columns=["uriProposicao", "numero", "ano", "codTema", "relevancia", "siglaTipo"]
)


print("data_proposicoes_temas len: ", len(data_proposicoes_temas))
print("data_proposicoes len: ", len(data_proposicoes))

data_proposicoes = data_proposicoes.merge(
    data_proposicoes_temas, left_on="id", right_on="id", how="left"
)

print("data_proposicoes_join len: ", len(data_proposicoes))

data_proposicoes.to_json("./data/proposicoes_join_temas.json", orient="records")
