import streamlit as st
import sqlite3
import pandas as pd

# Configuração da página da aplicação
st.set_page_config(page_title="DP Union - Parque de Equipamentos", layout="wide")
st.title("Gestão de Parque Instalado e Clientes")

# Função para inicializar e conectar ao banco de dados SQLite
def get_connection():
    conn = sqlite3.connect('banco_dados_dp.db', check_same_thread=False)
    # Criar a tabela se ela não existir
    conn.execute('''
        CREATE TABLE IF NOT EXISTS parque_instalado (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Representada TEXT,
            Equipamento TEXT,
            Modelo TEXT,
            Numero_Serie TEXT,
            Acessorios_Info TEXT,
            Data_Instalacao TEXT,
            Cliente TEXT,
            Cidade TEXT,
            Estado TEXT,
            Departamento TEXT,
            Nome TEXT,
            Email TEXT,
            Telefone TEXT,
            Celular TEXT
        )
    ''')
    return conn

conn = get_connection()

# Criação das abas para organização visual
aba1, aba2 = st.tabs(["📋 Visualizar e Editar Banco de Dados", "➕ Cadastrar Novo Equipamento"])

# --- ABA 1: VISUALIZAÇÃO E EDIÇÃO ---
with aba1:
    st.subheader("Portfólio de Clientes e Equipamentos")
    st.write("Edite as informações diretamente na tabela abaixo e as alterações serão salvas no banco de dados.")
    
    # Carregar dados do banco
    df = pd.read_sql_query("SELECT * FROM parque_instalado", conn)
    
    if not df.empty:
        # st.data_editor permite edição estilo Excel direto na tela
        df_editado = st.data_editor(
            df, 
            num_rows="dynamic", 
            use_container_width=True,
            hide_index=True,
            column_config={
                "id": st.column_config.NumberColumn("ID", disabled=True)
            }
        )
        
        if st.button("💾 Salvar Alterações no Banco de Dados"):
            # Substitui a tabela antiga pelos dados editados
            df_editado.to_sql('parque_instalado', conn, if_exists='replace', index=False)
            st.success("Banco de dados atualizado com sucesso!")
            st.rerun()
    else:
        st.info("O banco de dados está vazio. Cadastre o primeiro equipamento na aba ao lado.")

# --- ABA 2: CADASTRO DE NOVOS ITENS ---
with aba2:
    st.subheader("Formulário de Entrada de Dados")
    
    with st.form(key="form_cadastro", clear_on_submit=True):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            representada = st.text_input("Representada (Fornecedor)")
            equipamento = st.text_input("Equipamento")
            modelo = st.text_input("Modelo")
            numero_serie = st.text_input("Número de Série")
            acessorios = st.text_input("Acessórios/SN - Info")
            
        with col2:
            data_inst = st.date_input("Data da Instalação")
            cliente = st.text_input("Cliente")
            cidade = st.text_input("Cidade")
            estado = st.text_input("Estado")
            departamento = st.text_input("Departamento")
            
        with col3:
            nome = st.text_input("Nome (Responsável)")
            email = st.text_input("E-mail")
            telefone = st.text_input("Telefone")
            celular = st.text_input("Celular")
            
        submit_button = st.form_submit_button(label="Cadastrar no Sistema")
        
        if submit_button:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO parque_instalado (
                    Representada, Equipamento, Modelo, Numero_Serie, Acessorios_Info, 
                    Data_Instalacao, Cliente, Cidade, Estado, Departamento, Nome, Email, Telefone, Celular
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (representada, equipamento, modelo, numero_serie, acessorios, 
                  str(data_inst), cliente, cidade, estado, departamento, nome, email, telefone, celular))
            conn.commit()
            st.success(f"Equipamento {modelo} cadastrado para o cliente {cliente} com sucesso!")