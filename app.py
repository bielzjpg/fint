import streamlit as st
from dashboard import dashboard
from receitas import receitas
from despesas import despesas
from saldo import saldo
from planejamento import planejamento
from agenda import agenda
from import_export import importar_exportar
from ajuda import ajuda
from utils import carregar_dados
import os

# Aplica o CSS do arquivo estilo.css
with open("estilo.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# Inicialização do estado
if "pagina" not in st.session_state:
    st.session_state.pagina = "dashboard"

if "receitas" not in st.session_state:
    r, d, p, n = carregar_dados()
    st.session_state.receitas = r
    st.session_state.despesas = d
    st.session_state.planejamentos = p
    st.session_state.notas = n

def set_pagina(pagina):
    st.session_state.pagina = pagina

# Roteamento
paginas = {
    "dashboard": dashboard,
    "receitas": receitas,
    "despesas": despesas,
    "saldo": saldo,
    "planejamento": planejamento,
    "agenda": agenda,
    "import_export": importar_exportar,
    "ajuda": ajuda,
}

paginas[st.session_state.pagina]()

# Menu lateral
st.sidebar.title("Navegação")
for nome, chave in [
    ("Dashboard", "dashboard"),
    ("Receitas", "receitas"),
    ("Despesas", "despesas"),
    ("Saldo", "saldo"),
    ("Planejamento", "planejamento"),
    ("Agenda", "agenda"),
    ("Importar/Exportar", "import_export"),
    ("Ajuda", "ajuda")
]:
    if st.sidebar.button(nome):
        set_pagina(chave)
        st.rerun()