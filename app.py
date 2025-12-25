import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Configuração da página
st.set_page_config(page_title="Mochila de Emergência Familiar", layout="wide")

st.title("🎒 Mochila de Emergência Familiar")
st.write("Controle de itens e validades em tempo real.")

# Estrutura de dados com categorias e itens
itens = [
    {"Categoria": "Alimentação", "Item": "Água Mineral", "Validade": "2026-06-01"},
    {"Categoria": "Alimentação", "Item": "Barras de Proteína", "Validade": "2026-02-15"},
    {"Categoria": "Saúde", "Item": "Medicamentos Erisipela", "Validade": "2026-01-20"},
    {"Categoria": "Saúde", "Item": "Primeiros Socorros", "Validade": "2027-10-10"},
    {"Categoria": "Higiene", "Item": "Sabonete/Álcool em Gel", "Validade": "2026-12-31"},
    {"Categoria": "Ferramentas", "Item": "Lanterna e Pilhas", "Validade": "2028-05-01"},
]

df = pd.DataFrame(itens)
df['Validade'] = pd.to_datetime(df['Validade'])

# Lógica de Alerta de 90 dias
def calcular_status(data):
    hoje = datetime.now()
    if data < hoje:
        return "🔴 VENCIDO"
    elif data <= hoje + timedelta(days=90):
        return "🟡 VENCE EM 90 DIAS"
    else:
        return "🟢 OK"

df['Status'] = df['Validade'].apply(calcular_status)

# Exibição por Categorias
for categoria in df['Categoria'].unique():
    st.subheader(f"📁 {categoria}")
    sub_df = df[df['Categoria'] == categoria]
    st.table(sub_df[['Item', 'Validade', 'Status']])

st.info("Para editar os itens, basta me pedir para alterar o código aqui no chat!")
