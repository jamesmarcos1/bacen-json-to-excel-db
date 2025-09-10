import pandas as pd
import requests
from datetime import datetime
import json  # Para inspeção do JSON

def parse_data_referencia(data_raw):
    tipo = data_raw[0]  # A ou S
    mes = int(data_raw[1:3])
    ano = int(data_raw[3:])
    if tipo == "A":
        return datetime(ano, 12, 31).date(), "A"
    elif tipo == "S":
        return datetime(ano, 6 if mes == 6 else 12, 30).date(), "S"
    return None, None

periodos = ["202412"]  # Foco no período que contém o lucro

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
                
                # Salvar o JSON em um arquivo local para inspeção
                with open(f"json_inspecao_{cnpj}_{periodo}.json", "w", encoding="utf-8") as arquivo:
                    json.dump(json_data, arquivo, indent=4, ensure_ascii=False)
                print(f"JSON salvo: json_inspecao_{cnpj}_{periodo}.json")
                
                datas_ref = {item["@id"]: item["@data"] for item in json_data["datasBaseReferencia"]}
                for conta in json_data["BalancoPatrimonial"]["contas"]:
                    conta_id = conta.get("@id")
                    descricao = conta.get("@descricao")
                    if "valoresIndividualizados" in conta:  # Processar todas as contas, inclusive "LUCRO LÍQUIDO"
                        for valor in conta["valoresIndividualizados"]:
                            dt_base = valor["@dtBase"]
                            valor_conta = valor["@valor"]
                            data_real = datas_ref.get(dt_base, dt_base)
                            data_formatada, tipo_periodo = parse_data_referencia(data_real)
                            dados.append({
                                "cnpj": cnpj,
                                "periodo": periodo,
                                "conta_id": conta_id,
                                "descricao": descricao,
                                "data_referencia": data_formatada,
                                "tipo_periodo": tipo_periodo,
                                "valor": float(valor_conta) if valor_conta is not None else None
                            })
            else:
                print(f"Erro {resposta.status_code}: {url}")
        except Exception as e:
            print(f"Erro ao acessar {url}: {e}")

# Criar o DataFrame com todos os dados
df = pd.DataFrame(dados)

# Verificar dados de "LUCRO LÍQUIDO"
lucros_liquidos = df[df["descricao"].str.contains("LUCRO LÍQUIDO", case=False, na=False)]
if lucros_liquidos.empty:
    print("Nenhum dado de 'LUCRO LÍQUIDO' encontrado no JSON processado.")
else:
    print(lucros_liquidos)

# Salvar os resultados no Excel

df.to_excel("dados_para_postgresql_base_5.xlsx", index=False)

print("[OK] Excel salvo com sucesso: dados_para_postgresql_base_4.xlsx")
