import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="DP Union - Portfolio", layout="wide", initial_sidebar_state="expanded")

# TEMA CUSTOMIZADO VIA CSS
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #deff9a; color: black; font-weight: bold; }
    .stSidebar { background-color: #000; color: white; }
    </style>
    """, unsafe_allow_stdio=True)

st.title("🛡️ Gestão de Parque Instalado - DP Union")
st.markdown("---")

# CONEXÃO COM GOOGLE SHEETS
# Substitua o link abaixo pelo link da sua planilha do Google
URL_PLANILHA = "https://docs.google.com/spreadsheets/d/1HLnOkdOImSdLC0-K1_cWDw0hkbPSFxdu2QPQMmcn3zs/edit?usp=sharing"

conn = st.connection("gsheets", type=GSheetsConnection)

try:
    # Lendo os dados atuais
    df = conn.read(spreadsheet=URL_PLANILHA)
    
    # SIDEBAR - FILTROS
    st.sidebar.header("🔍 Filtros de Busca")
    cliente_filtro = st.sidebar.multiselect("Filtrar por Cliente", options=df["Cliente"].unique())
    rep_filtro = st.sidebar.multiselect("Filtrar por Representada", options=df["REPRESENTADA"].unique())

    # Aplicando filtros
    df_filtrado = df
    if cliente_filtro:
        df_filtrado = df_filtrado[df_filtrado["Cliente"].isin(cliente_filtro)]
    if rep_filtro:
        df_filtrado = df_filtrado[df_filtrado["REPRESENTADA"].isin(rep_filtro)]

    # ABAS
    aba_view, aba_add = st.tabs(["📋 Base de Dados & Edição", "➕ Novo Cadastro"])

    with aba_view:
        st.subheader("Visualização e Edição Rápida")
        st.info("Clique em qualquer célula para editar. Após terminar, clique no botão 'Salvar' abaixo.")
        
        df_editado = st.data_editor(df_filtrado, num_rows="dynamic", use_container_width=True, hide_index=True)
        
        if st.button("💾 Salvar Alterações na Nuvem"):
            # Atualiza a base original com os dados filtrados/editados
            df.update(df_editado)
            conn.update(spreadsheet=URL_PLANILHA, data=df)
            st.success("Dados sincronizados com o Google Sheets!")

    with aba_add:
        with st.form("form_novo", clear_on_submit=True):
            st.subheader("Cadastro de Novo Equipamento")
            col1, col2 = st.columns(2)
            
            with col1:
                rep = st.text_input("Representada")
                equip = st.text_input("Equipamento")
                mod = st.text_input("Modelo")
                sn = st.text_input("Número de Série")
                data = st.date_input("Data Instalação")
                
            with col2:
                cli = st.text_input("Cliente")
                cid = st.text_input("Cidade")
                est = st.text_input("Estado")
                email = st.text_input("E-mail")
                tel = st.text_input("Telefone")

            if st.form_submit_button("Cadastrar"):
                nova_linha = pd.DataFrame([{
                    "REPRESENTADA": rep, "Equipamento": equip, "Modelo": mod, 
                    "Número Série": sn, "Data Instalação": str(data), 
                    "Cliente": cli, "Cidade": cid, "Estado": est, "EMAIL": email, "TELEFONE": tel
                }])
                df_final = pd.concat([df, nova_linha], ignore_index=True)
                conn.update(spreadsheet=URL_PLANILHA, data=df_final)
                st.success("Novo item cadastrado com sucesso!")
                st.rerun()

except Exception as e:
    st.error("Erro ao conectar com o banco de dados. Verifique o link da planilha.")
    st.write(e)
