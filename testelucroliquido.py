import pandas as pd
import requests
from datetime import datetime
import json  # Para inspecionar o JSON

def parse_data_referencia(data_raw):
    tipo = data_raw[0]  # A ou S
    mes = int(data_raw[1:3])
    ano = int(data_raw[3:])
    if tipo == "A":
        return datetime(ano, 12, 31).date(), "A"
    elif tipo == "S":
        return datetime(ano, 6 if mes == 6 else 12, 30).date(), "S"
    return None, None

periodos = ["202412"]  # Apenas o período em questão

cnpjs = [
    "06043050"
]

base_url = "https://www3.bcb.gov.br/informes/rest/balanco/download/{}-9011-{}.json"
dados = []

for periodo in periodos:
    for cnpj in cnpjs:
        url = base_url.format(periodo, cnpj)
        try:
            resposta = requests.get(url)
            if resposta.status_code == 200:
                json_data = resposta.json()

                # Salvar o JSON completo para análise
                with open(f"json_inspecao_{cnpj}_{periodo}.json", "w", encoding="utf-8") as arquivo:
                    json.dump(json_data, arquivo, indent=4, ensure_ascii=False)
                print(f"JSON completo salvo: json_inspecao_{cnpj}_{periodo}.json")

                # Exibir as descrições das contas no terminal
                print("Descrições encontradas no JSON:")
                for conta in json_data["BalancoPatrimonial"]["contas"]:
                    descricao = conta.get("@descricao", "Sem descrição")
                    print(f"Descrição: {descricao}")
            else:
                print(f"Erro {resposta.status_code}: {url}")
        except Exception as e:
            print(f"Erro ao acessar {url}: {e}")
