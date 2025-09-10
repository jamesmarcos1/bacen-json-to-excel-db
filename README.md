# Consórcio JSON to Excel & DB

Este repositório contém um script Python que baixa dados financeiros de consórcios do Banco Central (BACEN) em formato JSON, os processa, junta em um arquivo Excel e os prepara para serem importados em um banco de dados PostgreSQL.

## Funcionalidades

- **Baixa os dados JSON do BACEN**: O script se conecta ao endpoint da API do BACEN e baixa dados financeiros relacionados ao consórcio, incluindo demonstrações de resultado e balanços patrimoniais.
- **Processa e limpa os dados**: Normaliza os dados (removendo acentos e caracteres especiais), organiza as informações por período, conta e CNPJ.
- **Exporta para Excel**: Gera um arquivo Excel contendo os dados processados para facilitar a análise.
- **Importação para Banco de Dados**: O script prepara os dados para serem importados diretamente para um banco de dados PostgreSQL.

## Como Rodar

### Pré-requisitos

- Python 3.x
- Bibliotecas Python: pandas, requests, unicodedata (instale as dependências com `pip install -r requirements.txt`)

### Passos para Execução

1. Clone este repositório:
   ```bash
   git clone https://github.com/seu-usuario/consorcio-json-to-excel-db.git

# Consortium JSON to Excel & DB

This repository contains a Python script that downloads financial data from consortia from the Central Bank (BACEN) in JSON format, processes it, combines it into an Excel file, and prepares it for import into a PostgreSQL database.

## Functionalities

- **Downloads JSON data from BACEN**: The script connects to the BACEN API endpoint and downloads financial data related to the consortium, including income statements and balance sheets.
- **Processes and cleans data**: Normalizes the data (removing accents and special characters), organizes the information by period, account, and CNPJ (Brazilian Taxpayer Registry).
- **Exports to Excel**: Generates an Excel file containing the processed data for easier analysis.
- **Imports to Database**: The script prepares the data for direct import into a PostgreSQL database.

## How to Run

### Prerequisites

- Python 3.x
- Python libraries: pandas, requests, unicodedata (install dependencies with `pip install -r requirements.txt`)

### Steps to Run

1. Clone this repository:
```bash
git clone https://github.com/seu-usuario/consorcio-json-to-excel-db.git
