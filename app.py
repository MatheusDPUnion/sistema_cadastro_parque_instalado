import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="DP Union - Gestão", layout="wide")

st.title("🛡️ DP Union - Controle de Parque Instalado")

# Conexão com o Google Sheets
# IMPORTANTE: Coloque o URL da sua planilha abaixo
URL_PLANILHA = "https://docs.google.com/spreadsheets/d/1HLnOkdOImSdLC0-K1_cWDw0hkbPSFxdu2QPQMmcn3zs/edit?usp=sharing" 

conn = st.connection("gsheets", type=GSheetsConnection)

# Carrega dados com tratamento de cache para não dar erro
@st.cache_data(ttl=60)
def load_data():
    return conn.read(spreadsheet=URL_PLANILHA, usecols=[0,1,2,3,4,5,6,7,8,9,10,11,12,13])

try:
    df = load_data()
    
    # Garantir que todas as colunas tenham nomes de string
    df.columns = df.columns.astype(str)

    st.subheader("Base de Equipamentos")
    
    # Editor de dados robusto
    df_editado = st.data_editor(
        df, 
        use_container_width=True, 
        num_rows="dynamic",
        key="data_editor"
    )

    if st.button("💾 Sincronizar com o Google Sheets"):
        conn.update(spreadsheet=URL_PLANILHA, data=df_editado)
        st.success("Dados salvos na nuvem com sucesso!")
        st.rerun()

except Exception as e:
    st.error(f"Erro ao carregar a planilha. Verifique o link e as permissões. Detalhe: {e}")
