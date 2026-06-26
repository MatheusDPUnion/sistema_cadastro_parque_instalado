import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

st.set_page_config(layout="wide")
st.title("🛡️ DP Union - Controle de Parque")

# URL da sua planilha (garanta que o link esteja compartilhado como Editor)
URL_PLANILHA = "https://docs.google.com/spreadsheets/d/1HLnOkdOImSdLC0-K1_cWDw0hkbPSFxdu2QPQMmcn3zs/edit?usp=sharing" 

conn = st.connection("gsheets", type=GSheetsConnection)

try:
    # 1. Leitura forçando tudo como texto para evitar erro de tipo
    df = conn.read(spreadsheet=URL_PLANILHA, dtype=str)
    
    # 2. Limpeza básica: remove colunas totalmente vazias (se houver)
    df = df.dropna(how='all', axis=1)

    st.subheader("Base de Equipamentos")
    
    # 3. Editor de dados com controle de sessão
    df_editado = st.data_editor(
        df, 
        use_container_width=True, 
        num_rows="dynamic"
    )

    if st.button("💾 Salvar Alterações na Nuvem"):
        # 4. Gravação na planilha
        conn.update(spreadsheet=URL_PLANILHA, data=df_editado)
        st.success("Dados salvos com sucesso!")
        st.rerun()

except Exception as e:
    st.error(f"Erro de conexão: {e}")
    st.write("Dica: Verifique se o link da planilha está correto e se o compartilhamento está como 'Editor'.")
