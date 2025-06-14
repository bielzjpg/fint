import streamlit as st
from datetime import datetime
from utils import salvar_dados

def despesas():
    st.title("Despesas")
    with st.form("form_despesa"):
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
            st.session_state.despesas.append(nova)
            salvar_dados(st.session_state.receitas, st.session_state.despesas,
                         st.session_state.planejamentos, st.session_state.notas)
            st.success("Despesa adicionada!")

    for i, d in enumerate(st.session_state.despesas):
        st.write(f"{d['data_hora']} | {d['descricao']} | R$ {d['valor']:.2f} | {d['categoria']}")
        if st.button("Excluir", key=f"del_desp_{i}"):
            st.session_state.despesas.pop(i)
            salvar_dados(st.session_state.receitas, st.session_state.despesas,
                         st.session_state.planejamentos, st.session_state.notas)
            st.experimental_rerun()