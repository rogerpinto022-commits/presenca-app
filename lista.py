
import streamlit as st

# === LOGIN ===
if "logado" not in st.session_state:
    st.session_state.logado = False

if not st.session_state.logado:
    st.title("Acesso Restrito")
    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")
    
    if st.button("Entrar"):
        if usuario == "almir" and senha == "28051982Isa#":
            st.session_state.logado = True
            st.rerun()
        else:
            st.error("Usuário ou senha incorretos")
    st.stop()

# === A PARTIR DAQUI É O TEU APP NORMAL ===
st.title("Sistema de Presença")
st.write("Bem-vindo, almir!")

# Cola aqui o resto do teu código que já existia no app.py
# Exemplo:
# st.dataframe(dados)
# st.button("Marcar Presença")
