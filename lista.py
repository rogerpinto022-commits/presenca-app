import streamlit as st

st.title("Lista de Presença")

qtde = st.number_input("Quantos alunos temos hoje?", min_value=1, step=1)

alunos = []
for i in range(int(qtde)):
    nome = st.text_input(f"Digite o nome do Aluno {i+1}", key=i)
    if nome:
        alunos.append(nome)

if st.button("Mostrar lista"):
    st.subheader("--- Lista de presença ---")
    for nome in alunos:
        st.write(f"- {nome}")
