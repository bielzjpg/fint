import streamlit as st
import json
from utils import salvar_dados

def importar_exportar():
    st.title("Importar / Exportar")
    st.download_button("Exportar dados", json.dumps({
        "receitas": st.session_state.receitas,
        "despesas": st.session_state.despesas,
        "planejamentos": st.session_state.planejamentos,
        "notas": st.session_state.notas
    }, indent=4), file_name="backup_financeiro.json", mime="application/json")

    arquivo = st.file_uploader("Importar JSON", type=["json"])
    if arquivo:
        dados = json.load(arquivo)
        st.session_state.receitas = dados.get("receitas", [])
        st.session_state.despesas = dados.get("despesas", [])
        st.session_state.planejamentos = dados.get("planejamentos", [])
        st.session_state.notas = dados.get("notas", "")
        salvar_dados(st.session_state.receitas, st.session_state.despesas,
                     st.session_state.planejamentos, st.session_state.notas)
        st.success("Dados importados com sucesso!")
        st.experimental_rerun()