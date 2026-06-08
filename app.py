import streamlit as st

# Login
if "logado" not in st.session_state:
    st.session_state.logado = False

if not st.session_state.logado:
    st.title("Acesso Restrito")
    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")
    
    if st.button("Entrar"):
        if usuario == "admin" and senha == "123456":
            st.session_state.logado = True
            st.rerun()
        else:
            st.error("Usuário ou senha incorretos")
    st.stop()import streamlit as st
import gspread
from datetime import datetime
from google.oauth2.service_account import Credentials

st.title("Lista de Presença")

# conecta no Google Sheets
def conectar_sheets():
    creds = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )
    client = gspread.authorize(creds)
    return client.open("Lista Presenca").sheet1

if 'alunos' not in st.session_state:
    st.session_state.alunos = []

qtde = st.number_input("Quantos alunos temos hoje?", min_value=1, step=1)

for i in range(int(qtde)):
    nome = st.text_input(f"Nome do Aluno {i+1}", key=f"aluno_{i}")
    if nome and nome not in st.session_state.alunos:
        st.session_state.alunos.append(nome)

if st.button("Salvar e Mostrar lista"):
    if st.session_state.alunos:
        # salva no Google Sheets
        sheet = conectar_sheets()
        data = datetime.now().strftime("%d/%m/%Y %H:%M")
        sheet.append_row([data] + st.session_state.alunos)

        st.success("Lista salva no Google Sheets!")
        st.subheader("--- Lista de presença ---")
        for nome in st.session_state.alunos:
            st.write(f"- {nome}")

        texto_copia = "\n".join(st.session_state.alunos)
        st.text_area("Copiar lista:", texto_copia, height=200)
    else:
        st.warning("Digite pelo menos um nome")

if st.button("Limpar lista"):
    st.session_state.alunos = []
    st.rerun()
