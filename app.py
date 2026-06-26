import streamlit as st
import pandas as pd
import requests
from io import StringIO

st.set_page_config(layout="wide")
st.title("🛡️ DP Union - Gestão de Equipamentos")

# URL da sua planilha publicada (a que você pegou em "Publicar na Web")
URL_CSV = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRbRQxpDoO2MvjsBesafYy-w55RsgyXhK74KOZj_2rrtQ7Up3LZP7y4KwvTk2nlPlHS0CgWQhsedzZi/pub?output=csv"

def get_data():
    response = requests.get(URL_CSV)
    data = StringIO(response.text)
    return pd.read_csv(data)

# Abas para separar a visualização do cadastro
aba1, aba2 = st.tabs(["📋 Visualizar Parque Instalado", "➕ Novo Cadastro"])

with aba1:
    try:
        df = get_data()
        st.dataframe(df, use_container_width=True)
    except:
        st.error("Erro ao carregar os dados. Verifique o link da planilha publicada.")

with aba2:
    st.info("Para cadastrar um novo equipamento, preencha os dados abaixo.")
    with st.form("form_cadastro"):
        # Seus campos de cadastro...
        nome_cliente = st.text_input("Nome do Cliente")
        equipamento = st.text_input("Equipamento")
        # ... outros campos ...
        
        if st.form_submit_button("Enviar Cadastro"):
            st.warning("Para manter a integridade, o cadastro está sendo enviado para a gerência via E-mail/Log.")
            # Aqui você pode usar st.write ou enviar um e-mail automático
