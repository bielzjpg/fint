import json

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