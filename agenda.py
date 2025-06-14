import streamlit as st
from utils import salvar_dados

def agenda():
    st.title("Agenda")
    eventos = [
        {**r, "tipo": "Receita"} for r in st.session_state.receitas
    ] + [
        {**d, "tipo": "Despesa"} for d in st.session_state.despesas
    ]
    eventos.sort(key=lambda x: x["data_hora"], reverse=True)
    for ev in eventos:
        st.write(f"[{ev['tipo']}] {ev['data_hora']} - {ev['descricao']} - R$ {ev['valor']:.2f} - {ev['categoria']}")
    st.markdown("---")
    st.subheader("Notas")
    texto = st.text_area("Anotações:", value=st.session_state.notas, height=200)
    if st.button("Salvar Notas"):
        st.session_state.notas = texto
        salvar_dados(st.session_state.receitas, st.session_state.despesas,
                     st.session_state.planejamentos, st.session_state.notas)
        st.success("Notas salvas!")