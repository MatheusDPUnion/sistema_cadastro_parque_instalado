import streamlit as st
import sqlite3
import pandas as pd
import os

DB_NAME = "banco_dados_dp.db"
CSV_FILE = "parque.csv" # Renomeie sua planilha para este nome no GitHub

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # Verifica se a tabela já existe
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='parque_instalado'")
    if not cursor.fetchone():
        # Se não existe, cria a partir do CSV
        df = pd.read_csv(CSV_FILE)
        df.to_sql('parque_instalado', conn, if_exists='replace', index=False)
    conn.close()

# Inicializa o banco na primeira execução
if not os.path.exists(DB_NAME):
    init_db()

# Interface
st.title("DP Union - Gestão de Equipamentos")
conn = sqlite3.connect(DB_NAME, check_same_thread=False)
df = pd.read_sql_query("SELECT * FROM parque_instalado", conn)

st.subheader("Portfólio de Clientes")
df_editado = st.data_editor(df, num_rows="dynamic", use_container_width=True)

if st.button("💾 Salvar Alterações"):
    df_editado.to_sql('parque_instalado', conn, if_exists='replace', index=False)
    st.success("Alterações salvas!")
