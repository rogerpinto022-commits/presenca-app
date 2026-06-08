import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from datetime import datetime, date, timedelta
import qrcode
import os

# ========== LOGIN ==========
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("Sistema de Presença - Login")

    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        if usuario == "almir" and senha == "28051982Isa#":
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Usuário ou senha incorretos")
    st.stop()

# ========== SEU APP AQUI ==========
st.title("Sistema de Presença")
st.write(f"Bem-vindo, almir!")

CREDS_FILE = "credentials.json"
SHEET_URL = "https://docs.google.com/spreadsheets/d/1If2otqQbyuWRipw9xMCBdDKOj-jKSJuNM2O8-QcgjhI/edit?gid=0#gid=0"
SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

def conectar():
    creds = Credentials.from_service_account_file(CREDS_FILE, scopes=SCOPE)
    client = gspread.authorize(creds)
    sheet = client.open_by_url(SHEET_URL)
    return sheet

def get_aba(nome_aba, colunas):
    sheet = conectar()
    try:
        aba = sheet.worksheet(nome_aba)
    except:
        aba = sheet.add_worksheet(title=nome_aba, rows=1000, cols=len(colunas))
        aba.append_row(colunas)
    return aba

def cadastrar_aluno(nome, escola, turma):
    aba_alunos = get_aba("Alunos", ["codigo_qr", "nome", "escola", "turma", "data_cadastro"])
    registros = aba_alunos.get_all_records()
    df = pd.DataFrame(registros) if registros else pd.DataFrame()
    novo_id = len(df) + 1
    codigo_qr = f"QR{novo_id:04d}"
    data_cadastro = date.today().strftime("%Y-%m-%d")
    aba_alunos.append_row([codigo_qr, nome, escola, turma, data_cadastro])
    os.makedirs("qrcodes", exist_ok=True)
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(codigo_qr)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    caminho = f"qrcodes/{codigo_qr}_{nome.replace(' ', '_')}.png"
    img.save(caminho)
    return {"status": "ok", "codigo_qr": codigo_qr, "nome": nome, "caminho_qr": caminho}

def registrar_presenca(codigo_qr):
    aba_alunos = get_aba("Alunos", ["codigo_qr", "nome", "escola", "turma", "data_cadastro"])
    aba_presenca = get_aba("Presencas", ["codigo_qr", "nome", "escola", "turma", "data", "hora", "status"])
    registros_alunos = aba_alunos.get_all_records()
    df_alunos = pd.DataFrame(registros_alunos) if registros_alunos else pd.DataFrame()
    aluno = df_alunos[df_alunos['codigo_qr'] == codigo_qr]
    if aluno.empty:
        return {"status": "erro", "msg": "QR não cadastrado"}
    aluno = aluno.iloc[0]
    hoje = date.today().strftime("%Y-%m-%d")
    hora = datetime.now().strftime("%H:%M:%S")
    registros_presenca = aba_presenca.get_all_records()
    df_presenca = pd.DataFrame(registros_presenca) if registros_presenca else pd.DataFrame()
    if not df_presenca.empty:
        if ((df_presenca['codigo_qr'] == codigo_qr) & (df_presenca['data'] == hoje)).any():
            return {"status": "erro", "msg": "Presença já registrada hoje"}
    aba_presenca.append_row([codigo_qr, aluno['nome'], aluno['escola'], aluno['turma'], hoje, hora, "Presente"])
    return {"status": "ok", "msg": f"{aluno['nome']} - Presença registrada às {hora}"}

def get_resumo_diario(escola=None):
    aba_presenca = get_aba("Presencas", ["codigo_qr", "nome", "escola", "turma", "data", "hora", "status"])
    registros = aba_presenca.get_all_records()
    df = pd.DataFrame(registros) if registros else pd.DataFrame()
    if df.empty:
        return {"total_presentes": 0, "atrasados": 0, "pontuais": 0, "taxa_pontualidade": 0}
    hoje = date.today().strftime("%Y-%m-%d")
    df_hoje = df[df['data'] == hoje]
    if escola:
        df_hoje = df_hoje[df_hoje['escola'] == escola]
    total = len(df_hoje)
    if total == 0:
        return {"total_presentes": 0, "atrasados": 0, "pontuais": 0, "taxa_pontualidade": 0}
    df_hoje['hora_dt'] = pd.to_datetime(df_hoje['hora'], format='%H:%M:%S')
    atrasados = len(df_hoje[df_hoje['hora_dt'].dt.time > datetime.strptime("08:00:00", "%H:%M:%S").time()])
    return {
        "total_presentes": total,
        "atrasados": atrasados,
        "pontuais": total - atrasados,
        "taxa_pontualidade": round(((total - atrasados) / total) * 100, 1)
    }

# Aqui tu coloca a interface Streamlit do teu app
# Ex: st.text_input, st.button, etc usando as funções acima
