import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Configuração visual da página
st.set_page_config(page_title="Mochila de Emergência", page_icon="🎒", layout="centered")

st.title("🎒 Controle de Validade")
st.subheader("Itens da Mochila de Emergência")

# Nome do arquivo onde os dados serão salvos
DB_FILE = "estoque_mochila.csv"

# Função para carregar dados
def carregar_dados():
    if os.path.exists(DB_FILE):
        return pd.read_csv(DB_FILE, parse_dates=["Data de Validade"])
    return pd.DataFrame(columns=["Item", "Categoria", "Data de Validade"])

# Inicializa o estado da sessão
if 'estoque' not in st.session_state:
    st.session_state.estoque = carregar_dados()

# --- FORMULÁRIO PARA ADICIONAR ITENS ---
with st.expander("➕ Adicionar Novo Item", expanded=False):
    with st.form("novo_item", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            nome = st.text_input("Nome do Item (Ex: Atum, Lanterna)")
        with col2:
            cat = st.selectbox("Categoria", ["Alimentação", "Higiene/Saúde", "Ferramentas", "Iluminação", "Comunicação"])
        
        validade = st.date_input("Data de Validade", datetime.now())
        enviar = st.form_submit_button("Salvar na Mochila")
        
        if enviar and nome:
            novo_item = pd.DataFrame([[nome, cat, pd.to_datetime(validade)]], 
                                     columns=["Item", "Categoria", "Data de Validade"])
            st.session_state.estoque = pd.concat([st.session_state.estoque, novo_item], ignore_index=True)
            # Salva no arquivo CSV
            st.session_state.estoque.to_csv(DB_FILE, index=False)
            st.success(f"✅ {nome} adicionado!")

# --- EXIBIÇÃO DOS ITENS ---
if not st.session_state.estoque.empty:
    df = st.session_state.estoque.copy()
    hoje = pd.Timestamp(datetime.now().date())
    
    # Lógica de Status com cores
    def calcular_status(data):
        dias_para_vencer = (data - hoje).days
        if dias_para_vencer < 0:
            return "🔴 VENCIDO"
        elif dias_para_vencer <= 30:
            return "🟡 VENCE EM BREVE"
        else:
            return "🟢 OK"

    df['Status'] = df['Data de Validade'].apply(calcular_status)
    
    # Ordenar por data (os mais próximos de vencer primeiro)
    df = df.sort_values(by="Data de Validade")

    st.write("### Itens Cadastrados")
    # Exibe a tabela formatada
    st.dataframe(df.style.applymap(lambda x: 'color: red' if x == "🔴 VENCIDO" else ('color: orange' if x == "🟡 VENCE EM BREVE" else 'color: green'), subset=['Status']), use_container_width=True)

    if st.button("Limpar lista (Cuidado!)"):
        if os.path.exists(DB_FILE):
            os.remove(DB_FILE)
        st.session_state.estoque = pd.DataFrame(columns=["Item", "Categoria", "Data de Validade"])
        st.rerun()
else:
    st.info("Sua mochila está vazia. Adicione itens acima para começar!")
