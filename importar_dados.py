import pandas as pd
import sqlite3

# Nome do arquivo CSV ou XLSX que você tem
arquivo = 'Parque_instalado_Geral_Final.xlsx - Parque de Máquinas dpUNION.csv'
df = pd.read_csv(arquivo)

# Conectar ao banco de dados
conn = sqlite3.connect('banco_dados_dp.db')
# Enviar os dados da planilha para a tabela do sistema
df.to_sql('parque_instalado', conn, if_exists='replace', index=False)
print(Dados importados com sucesso!)