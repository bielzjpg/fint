import streamlit as st

def saldo():
    st.title("Saldo")
    total_receitas = sum(r['valor'] for r in st.session_state.receitas)
    total_despesas = sum(d['valor'] for d in st.session_state.despesas)
    saldo = total_receitas - total_despesas
    st.subheader(f"💰 Saldo Atual: R$ {saldo:.2f}")