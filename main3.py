import pandas as pd
import requests
from datetime import datetime
import unicodedata  # Biblioteca para normalizar strings

def normalize_text(text):
    """
    Remove acentos e caracteres especiais de uma string.
    """
    if text is not None:
        return unicodedata.normalize("NFKD", text).encode("ASCII", "ignore").decode("utf-8")
    return ""

def parse_data_referencia(data_raw):
    tipo = data_raw[0]  # A ou S
    mes = int(data_raw[1:3])
    ano = int(data_raw[3:])
    if tipo == "A":
        return datetime(ano, 12, 31).date(), "A"
    elif tipo == "S":
        return datetime(ano, 6 if mes == 6 else 12, 30).date(), "S"
    return None, None

periodos = ["202412"]

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

                # Verifique se os dados do JSON estão corretos
                if "DemonstracaoDoResultado" not in json_data or "BalancoPatrimonial" not in json_data:
                    print(f"Erro: Blocos 'DemonstracaoDoResultado' ou 'BalancoPatrimonial' não encontrados no JSON.")
                    continue

                datas_ref = {item["@id"]: item["@data"] for item in json_data["datasBaseReferencia"]}

                # Iteração sobre o bloco 'DemonstracaoDoResultado'
                for conta in json_data["DemonstracaoDoResultado"]["contas"]:
                    conta_id = conta.get("@id")
                    descricao = conta.get("@descricao")
                    descricao_normalizada = normalize_text(descricao)

                    if "valoresIndividualizados" in conta:
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
                                "descricao_normalizada": descricao_normalizada,
                                "data_referencia": data_formatada,
                                "tipo_periodo": tipo_periodo,
                                "valor": float(valor_conta) if valor_conta is not None else None,
                                "tipo_bloco": "DemonstracaoDoResultado"
                            })

                # Iteração sobre o bloco 'BalancoPatrimonial'
                for conta in json_data["BalancoPatrimonial"]["contas"]:
                    conta_id = conta.get("@id")
                    descricao = conta.get("@descricao")
                    descricao_normalizada = normalize_text(descricao)

                    if "valoresIndividualizados" in conta:
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
                                "descricao_normalizada": descricao_normalizada,
                                "data_referencia": data_formatada,
                                "tipo_periodo": tipo_periodo,
                                "valor": float(valor_conta) if valor_conta is not None else None,
                                "tipo_bloco": "BalancoPatrimonial"
                            })

            else:
                print(f"Erro {resposta.status_code}: {url}")
        except Exception as e:
            print(f"Erro ao acessar {url}: {e}")

# Criar o DataFrame com os dados
df = pd.DataFrame(dados)

# Verificar se há dados antes de continuar
if df.empty:
    print("Nenhum dado encontrado, o DataFrame está vazio.")
else:
    # Verificar se a coluna 'descricao_normalizada' existe antes de aplicar o filtro
    if "descricao_normalizada" in df.columns:
        # Filtro por "lucro liquido" no texto normalizado
        lucros_liquidos = df[df["descricao_normalizada"].str.contains("lucro liquido", case=False, na=False)]
        if lucros_liquidos.empty:
            print("Nenhum dado de 'LUCRO LÍQUIDO' encontrado no JSON processado.")
        else:
            print("Dados de 'LUCRO LÍQUIDO' encontrados!")
            print(lucros_liquidos)
    else:
        print("A coluna 'descricao_normalizada' não foi encontrada no DataFrame.")

# Verificar o conteúdo do DataFrame
print(df.head())  # Verifique as primeiras linhas do DataFrame para garantir que as colunas estejam sendo preenchidas corretamente.

# Salvar os resultados no Excel
df.to_excel("dados_para_postgresql_base_9.xlsx", index=False)

print("[OK] Excel salvo com sucesso: dados_para_postgresql_base_9.xlsx")
