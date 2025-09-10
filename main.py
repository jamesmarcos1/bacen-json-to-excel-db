import pandas as pd
import requests

# Listas de períodos e CNPJs
periodos = ["202212", "202312", "202412"]
cnpjs = [
    "84911098", "03828278", "45441789", "59999300", "73230674"
]

# URL base
base_url = "https://www3.bcb.gov.br/informes/rest/balanco/download/{}-9011-{}.json"

# Lista para armazenar os dados
dados = []

# Percorrer períodos e CNPJs
for periodo in periodos:
    for cnpj in cnpjs:
        url = base_url.format(periodo, cnpj)
        try:
            resposta = requests.get(url)
            if resposta.status_code == 200:
                json_data = resposta.json()
                
                # Criar um dicionário para mapear os dtBase com suas datas reais
                datas_ref = {item["@id"]: item["@data"] for item in json_data["datasBaseReferencia"]}

                # Percorrer contas e organizar os dados
                for conta in json_data["BalancoPatrimonial"]["contas"]:
                    conta_id = conta["@id"]
                    descricao = conta["@descricao"]
                    
                    # Se houver valores individualizados, processá-los
                    if "valoresIndividualizados" in conta:
                        for valor in conta["valoresIndividualizados"]:
                            dt_base = valor["@dtBase"]
                            valor_conta = valor["@valor"]
                            data_real = datas_ref.get(dt_base, dt_base)  # Substituir dtBase pela data real

                            dados.append({
                                "CNPJ": cnpj,
                                "Periodo": periodo,
                                "Conta_ID": conta_id,
                                "Descrição": descricao,
                                "Data_Referencia": data_real,
                                "Valor": valor_conta
                            })
            else:
                print(f"Não foi possível obter dados de {url}")
        except Exception as e:
            print(f"Erro ao acessar {url}: {e}")

# Criar DataFrame
df = pd.DataFrame(dados)

# Salvar em Excel
df.to_excel("dados_para_banco.xlsx", index=False)

print("Arquivo Excel gerado com sucesso!")
