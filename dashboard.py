import streamlit as st
import pandas as pd
import altair as alt

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