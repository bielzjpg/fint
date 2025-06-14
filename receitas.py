import streamlit as st
from datetime import datetime
from utils import salvar_dados

def receitas():
    st.title("Receitas")
    with st.form("form_receita"):
        descricao = st.text_input("Descrição")
        valor = st.number_input("Valor", min_value=0.01, format="%.2f")
        categoria = st.text_input("Categoria")
        submit = st.form_submit_button("Adicionar")
        if submit:
            nova = {
                "descricao": descricao,
                "valor": valor,
                "categoria": categoria,
                "data_hora": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            }
            st.session_state.receitas.append(nova)
            salvar_dados(st.session_state.receitas, st.session_state.despesas,
                         st.session_state.planejamentos, st.session_state.notas)
            st.success("Receita adicionada!")

    for i, r in enumerate(st.session_state.receitas):
        st.write(f"{r['data_hora']} | {r['descricao']} | R$ {r['valor']:.2f} | {r['categoria']}")
        if st.button("Excluir", key=f"del_rec_{i}"):
            st.session_state.receitas.pop(i)
            salvar_dados(st.session_state.receitas, st.session_state.despesas,
                         st.session_state.planejamentos, st.session_state.notas)
            st.experimental_rerun()