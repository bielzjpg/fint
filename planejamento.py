import streamlit as st
from datetime import date
from utils import salvar_dados

def planejamento():
    st.title("Planejamento")
    with st.form("form_planejamento"):
        data_pag = st.date_input("Data do pagamento", value=date.today())
        descricao = st.text_input("Descrição")
        submit = st.form_submit_button("Adicionar")
        if submit:
            novo = {"data": data_pag.strftime("%d/%m/%Y"), "descricao": descricao}
            st.session_state.planejamentos.append(novo)
            salvar_dados(st.session_state.receitas, st.session_state.despesas,
                         st.session_state.planejamentos, st.session_state.notas)
            st.success("Planejamento salvo.")

    for i, p in enumerate(st.session_state.planejamentos):
        st.write(f"{p['data']} — {p['descricao']}")
        if st.button("Excluir", key=f"del_plan_{i}"):
            st.session_state.planejamentos.pop(i)
            salvar_dados(st.session_state.receitas, st.session_state.despesas,
                         st.session_state.planejamentos, st.session_state.notas)
            st.experimental_rerun()