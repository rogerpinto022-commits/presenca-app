import streamlit as st
import pandas as pd

st.title("Lista de Presença")

# guarda os nomes mesmo se recarregar a página
if 'alunos' not in st.session_state:
    st.session_state.alunos = []

qtde = st.number_input("Quantos alunos temos hoje?", min_value=1, step=1)

for i in range(int(qtde)):
    nome = st.text_input(f"Nome do Aluno {i+1}", key=f"aluno_{i}")
    if nome and nome not in st.session_state.alunos:
        st.session_state.alunos.append(nome)

if st.button("Mostrar lista"):
    if st.session_state.alunos:
        st.subheader("--- Lista de presença ---")
        for nome in st.session_state.alunos:
            st.write(f"- {nome}")
        
        # cria arquivo Excel pra baixar
        df = pd.DataFrame({"Alunos": st.session_state.alunos})
        csv = df.to_csv(index=False).encode('utf-8')
        
        st.download_button(
            label="Baixar lista em Excel",
            data=csv,
            file_name="lista_presenca.csv",
            mime="text/csv"
        )
    else:
        st.warning("Digite pelo menos um nome")

if st.button("Limpar lista"):
    st.session_state.alunos = []
    st.rerun()
