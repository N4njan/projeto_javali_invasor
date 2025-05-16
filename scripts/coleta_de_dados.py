import requests
import pandas as pd
import os
import time

# Constantes do projeto
TAXON_KEY = 7705930  # Sus scrofa
PAIS = "BR"
ANOS = list(range(2013, 2025))
LIMITE = 300
MAX_REGISTROS_POR_ANO = 3000
PASTA_SAIDA = "dados"
API_URL = "https://api.gbif.org/v1/occurrence/search"

os.makedirs(PASTA_SAIDA, exist_ok=True)

def coletar_dados_por_ano(ano):
    todos_resultados = []
    offset = 0

    while offset < MAX_REGISTROS_POR_ANO:
        print(f"🔎 Ano {ano} — buscando de {offset} a {offset + LIMITE}")
        params = {
            "taxonKey": TAXON_KEY,
            "country": PAIS,
            "limit": LIMITE,
            "offset": offset,
            "year": ano
        }

        resposta = requests.get(API_URL, params=params)
        if resposta.status_code != 200:
            print(f"⚠️ Erro ao buscar ano {ano}: {resposta.status_code}")
            break

        dados = resposta.json().get("results", [])
        if not dados:
            break

        todos_resultados.extend(dados)
        offset += LIMITE
        time.sleep(1)

    return pd.DataFrame(todos_resultados)

def salvar_csv(df, ano):
    if df.empty:
        print(f"⚠️ Nenhum dado para {ano}.")
        return

    colunas_interesse = [
        "scientificName", "eventDate", "decimalLatitude", "decimalLongitude",
        "stateProvince", "country", "basisOfRecord", "institutionCode"
    ]
    colunas_existentes = [col for col in colunas_interesse if col in df.columns]
    df_filtrado = df[colunas_existentes]

    caminho = os.path.join(PASTA_SAIDA, f"ocorrencias_javali_{ano}.csv")
    df_filtrado.to_csv(caminho, index=False)
    print(f"✅ Dados de {ano} salvos em: {caminho}")

def main():
    for ano in ANOS:
        df_ano = coletar_dados_por_ano(ano)
        salvar_csv(df_ano, ano)

if __name__ == "__main__":
    main()
