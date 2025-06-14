import streamlit as st
from datetime import datetime, date
import json
import pandas as pd
import altair as alt

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Montserrat', sans-serif;
    background-color: #121214; /* fundo preto */
    color: #E1BEE7; /* roxo claro para textos */
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #6a0dad 0%, #4b0082 100%);
    color: white;
    border-right: 4px solid #7b1fa2;
}

/* Títulos da sidebar */
[data-testid="stSidebar"] h1, 
[data-testid="stSidebar"] h2, 
[data-testid="stSidebar"] h3 {
    color: #d1c4e9;
}

/* Botões do menu na sidebar */
.stButton button {
    background-color: #7b1fa2 !important;
    color: white !important;
    font-weight: 700;
    border-radius: 10px;
    border: none;
    padding: 10px 15px;
    margin-bottom: 8px;
    transition: background-color 0.3s ease;
    width: 100%;
    box-shadow: 0 3px 6px rgba(123, 31, 162, 0.6);
    cursor: pointer;
}
.stButton button:hover {
    background-color: #4a0072 !important;
}

/* Botão ativo do menu */
.stButton button:focus, .stButton button[aria-pressed="true"] {
    background-color: #37005c !important;
    box-shadow: 0 0 12px #37005c;
}

/* Títulos das páginas */
h1 {
    color: #d1c4e9;
    font-weight: 700;
    margin-bottom: 20px;
}

/* Métricas */
[data-testid="metric-container"] {
    background-color: #4a0072;
    border-radius: 12px;
    padding: 15px;
    color: white;
    font-weight: 700;
    box-shadow: 0 5px 10px rgba(74, 0, 114, 0.7);
}

/* Inputs e forms */
.stTextInput>div>div>input, 
.stNumberInput>div>input, 
.stDateInput>div>input, 
.stTextArea>div>textarea {
    border: 2px solid #7b1fa2 !important;
    border-radius: 10px !important;
    padding: 8px !important;
    background-color: #1e1b27 !important;
    color: #d1c4e9 !important;
    font-weight: 600;
}

/* Forms submit buttons */
.stButton>button {
    background-color: #7b1fa2 !important;
    color: white !important;
    font-weight: 700 !important;
    border-radius: 10px !important;
    padding: 10px 20px !important;
    margin-top: 10px !important;
    box-shadow: 0 5px 10px rgba(123, 31, 162, 0.7);
    transition: background-color 0.3s ease;
}
.stButton>button:hover {
    background-color: #4a0072 !important;
}

/* Linhas e divisores */
hr {
    border: 1px solid #7b1fa2;
    margin: 20px 0;
}

/* Rodapé */
footer {
    text-align: center;
    color: #7b1fa2;
    font-size: 12px;
    margin-top: 40px;
}

/* Altair charts custom color */
.vega-embed .mark-rect {
    fill: #7b1fa2 !important;
}

/* Scrollbar roxo */
::-webkit-scrollbar {
    width: 8px;
}
::-webkit-scrollbar-thumb {
    background-color: #7b1fa2;
    border-radius: 10px;
}
::-webkit-scrollbar-track {
    background-color: #121214;
}

</style>
""", unsafe_allow_html=True)


# Funções de dados
def salvar_dados(receitas, despesas, planejamentos, notas):
    with open("dados_financeiros.json", "w", encoding="utf-8") as f:
        json.dump({
            "receitas": receitas,
            "despesas": despesas,
            "planejamentos": planejamentos,
            "notas": notas
        }, f, ensure_ascii=False, indent=4)

def carregar_dados():
    try:
        with open("dados_financeiros.json", "r", encoding="utf-8") as f:
            dados = json.load(f)
        return (dados.get("receitas", []), dados.get("despesas", []), 
                dados.get("planejamentos", []), dados.get("notas", ""))
    except FileNotFoundError:
        return [], [], [], ""

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
    # Streamlit rerun já acontece automaticamente, sem necessidade de st.experimental_rerun()

# Sidebar menu com botões, usando keys que não conflitam com variáveis
with st.sidebar:
    st.title("📊 Menu")
    paginas = [
        ("Dashboard", "dashboard"),
        ("Receitas", "receitas"),
        ("Despesas", "despesas"),
        ("Saldo", "saldo"),
        ("Planejamento", "planejamento"),
        ("Agenda", "agenda"),
        ("Importar/Exportar", "import_export"),
        ("Ajuda", "ajuda")
    ]
    for nome, chave in paginas:
        estilo = (
            "width: 100%; margin: 4px 0; font-weight: bold; "
            + ("background-color: #4CAF50; color: white;" if st.session_state.pagina == chave else "")
        )
        if st.button(nome, key=f"menu_{chave}", help=f"Abrir {nome}"):
            set_pagina(chave)

# Funções das páginas

def dashboard():
    st.title("Dashboard")
    receitas = st.session_state.receitas
    despesas = st.session_state.despesas
    total_receitas = sum(r['valor'] for r in receitas)
    total_despesas = sum(d['valor'] for d in despesas)
    saldo = total_receitas - total_despesas
    st.metric("Total Receitas", f"R$ {total_receitas:.2f}")
    st.metric("Total Despesas", f"R$ {total_despesas:.2f}")
    st.metric("Saldo Atual", f"R$ {saldo:.2f}")

    if receitas or despesas:
        df = pd.DataFrame([
            {"tipo": "Receitas", "valor": total_receitas},
            {"tipo": "Despesas", "valor": total_despesas}
        ])
        chart = alt.Chart(df).mark_bar().encode(
            x="tipo",
            y="valor",
            color="tipo"
        )
        st.altair_chart(chart, use_container_width=True)

def receitas():
    st.title("Receitas")
    with st.form("form_receita"):
        descricao = st.text_input("Descrição", key="descricao_receita")
        valor = st.number_input("Valor", min_value=0.01, format="%.2f", key="valor_receita")
        categoria = st.text_input("Categoria", key="categoria_receita")
        submit = st.form_submit_button("Adicionar")
        if submit:
            nova = {
                "descricao": descricao,
                "valor": valor,
                "categoria": categoria,
                "data_hora": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            }
            st.session_state.receitas.append(nova)
            salvar_dados(st.session_state.receitas, st.session_state.despesas, st.session_state.planejamentos, st.session_state.notas)
            st.success("Receita adicionada!")

    # Mostrar lista e permitir exclusão
    for i, r in enumerate(st.session_state.receitas):
        st.write(f"{r['data_hora']} | {r['descricao']} | R$ {r['valor']:.2f} | {r['categoria']}")
        if st.button("Excluir", key=f"del_rec_{i}"):
            st.session_state.receitas.pop(i)
            salvar_dados(st.session_state.receitas, st.session_state.despesas, st.session_state.planejamentos, st.session_state.notas)
            st.experimental_rerun()  # Aqui é permitido usar normalmente para atualizar a tela após excluir

def despesas():
    st.title("Despesas")
    with st.form("form_despesa"):
        descricao = st.text_input("Descrição", key="descricao_despesa")
        valor = st.number_input("Valor", min_value=0.01, format="%.2f", key="valor_despesa")
        categoria = st.text_input("Categoria", key="categoria_despesa")
        submit = st.form_submit_button("Adicionar")
        if submit:
            nova = {
                "descricao": descricao,
                "valor": valor,
                "categoria": categoria,
                "data_hora": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            }
            st.session_state.despesas.append(nova)
            salvar_dados(st.session_state.receitas, st.session_state.despesas, st.session_state.planejamentos, st.session_state.notas)
            st.success("Despesa adicionada!")

    for i, d in enumerate(st.session_state.despesas):
        st.write(f"{d['data_hora']} | {d['descricao']} | R$ {d['valor']:.2f} | {d['categoria']}")
        if st.button("Excluir", key=f"del_desp_{i}"):
            st.session_state.despesas.pop(i)
            salvar_dados(st.session_state.receitas, st.session_state.despesas, st.session_state.planejamentos, st.session_state.notas)
            st.experimental_rerun()

def saldo():
    st.title("Saldo")
    total_receitas = sum(r['valor'] for r in st.session_state.receitas)
    total_despesas = sum(d['valor'] for d in st.session_state.despesas)
    saldo = total_receitas - total_despesas
    st.subheader(f"💰 Saldo Atual: R$ {saldo:.2f}")

def planejamento():
    st.title("Planejamento")
    with st.form("form_planejamento"):
        data_pag = st.date_input("Data do pagamento", value=date.today(), key="data_planejamento")
        descricao = st.text_input("Descrição", key="descricao_planejamento")
        submit = st.form_submit_button("Adicionar")
        if submit:
            novo = {"data": data_pag.strftime("%d/%m/%Y"), "descricao": descricao}
            st.session_state.planejamentos.append(novo)
            salvar_dados(st.session_state.receitas, st.session_state.despesas, st.session_state.planejamentos, st.session_state.notas)
            st.success("Planejamento salvo.")

    for i, p in enumerate(st.session_state.planejamentos):
        st.write(f"{p['data']} — {p['descricao']}")
        if st.button("Excluir", key=f"del_plan_{i}"):
            st.session_state.planejamentos.pop(i)
            salvar_dados(st.session_state.receitas, st.session_state.despesas, st.session_state.planejamentos, st.session_state.notas)
            st.experimental_rerun()

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
    texto = st.text_area("Anotações:", value=st.session_state.notas, height=200, key="notas_text_area")
    if st.button("Salvar Notas", key="btn_salvar_notas"):
        st.session_state.notas = texto
        salvar_dados(st.session_state.receitas, st.session_state.despesas, st.session_state.planejamentos, st.session_state.notas)
        st.success("Notas salvas!")

def importar_exportar():
    st.title("Importar / Exportar")
    st.download_button("Exportar dados", json.dumps({
        "receitas": st.session_state.receitas,
        "despesas": st.session_state.despesas,
        "planejamentos": st.session_state.planejamentos,
        "notas": st.session_state.notas
    }, indent=4), file_name="backup_financeiro.json", mime="application/json")

    arquivo = st.file_uploader("Importar JSON", type=["json"], key="uploader_json")
    if arquivo:
        dados = json.load(arquivo)
        st.session_state.receitas = dados.get("receitas", [])
        st.session_state.despesas = dados.get("despesas", [])
        st.session_state.planejamentos = dados.get("planejamentos", [])
        st.session_state.notas = dados.get("notas", "")
        salvar_dados(st.session_state.receitas, st.session_state.despesas, st.session_state.planejamentos, st.session_state.notas)
        st.success("Dados importados com sucesso!")
        st.experimental_rerun()

def ajuda():
    st.title("Ajuda")
    st.markdown("""
    Sistema de controle financeiro com registro de receitas, despesas, planejamento, exportação/importação de dados e anotações.
    """)

# Roteamento
if st.session_state.pagina == "dashboard":
    dashboard()
elif st.session_state.pagina == "receitas":
    receitas()
elif st.session_state.pagina == "despesas":
    despesas()
elif st.session_state.pagina == "saldo":
    saldo()
elif st.session_state.pagina == "planejamento":
    planejamento()
elif st.session_state.pagina == "agenda":
    agenda()
elif st.session_state.pagina == "import_export":
    importar_exportar()
elif st.session_state.pagina == "ajuda":
    ajuda()

# Rodapé
st.markdown("<div style='text-align:center; color:#999; font-size:10px;'>Criado por Canal do Gabriel 💼</div>", unsafe_allow_html=True)
