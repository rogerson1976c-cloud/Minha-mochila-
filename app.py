import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Configuração visual
st.set_page_config(page_title="Mochila de Emergência", page_icon="🎒", layout="centered")

st.title("🎒 Controle de Validade")
st.subheader("Itens da Minha Mochila")

DB_FILE = "estoque_mochila.csv"

def carregar_dados():
    if os.path.exists(DB_FILE):
        return pd.read_csv(DB_FILE)
    return pd.DataFrame(columns=["Item", "Categoria", "Data de Validade"])

if 'estoque' not in st.session_state:
    st.session_state.estoque = carregar_dados()

# --- FORMULÁRIO ---
with st.expander("➕ Adicionar Novo Item", expanded=False):
    with st.form("novo_item", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            nome = st.text_input("Nome do Item")
        with col2:
            # Novas categorias adicionadas aqui
            cat = st.selectbox("Categoria", [
                "Alimentação", "Higiene", "Saúde/Remédios", 
                "Ferramentas", "Iluminação", "Abrigo/Roupas", 
                "Comunicação", "Documentos", "Outros"
            ])
        
        col3, col4 = st.columns(2)
        with col3:
            indeterminada = st.checkbox("Validade Indeterminada")
        with col4:
            validade = st.date_input("Data de Validade", datetime.now())
        
        enviar = st.form_submit_button("Salvar na Mochila")
        
        if enviar and nome:
            data_str = "Indeterminada" if indeterminada else validade.strftime('%Y-%m-%d')
            novo_item = pd.DataFrame([[nome, cat, data_str]], 
                                     columns=["Item", "Categoria", "Data de Validade"])
            st.session_state.estoque = pd.concat([st.session_state.estoque, novo_item], ignore_index=True)
            st.session_state.estoque.to_csv(DB_FILE, index=False)
            st.success(f"✅ {nome} adicionado!")

# --- EXIBIÇÃO ---
if not st.session_state.estoque.empty:
    df = st.session_state.estoque.copy()
    hoje = datetime.now().date()
    
    def calcular_status(data_val):
        if data_val == "Indeterminada":
            return "♾️ PERMANENTE"
        try:
            dt = datetime.strptime(data_val, '%Y-%m-%d').date()
            dias = (dt - hoje).days
            if dias < 0: return "🔴 VENCIDO"
            elif dias <= 30: return "🟡 VENCE EM BREVE"
            else: return "🟢 OK"
        except:
            return "❓ ERRO NA DATA"

    df['Status'] = df['Data de Validade'].apply(calcular_status)
    st.write("### Itens Cadastrados")
    st.dataframe(df, use_container_width=True)

    if st.button("Limpar Tudo"):
        if os.path.exists(DB_FILE): os.remove(DB_FILE)
        st.session_state.estoque = pd.DataFrame(columns=["Item", "Categoria", "Data de Validade"])
        st.rerun()
else:
    st.info("Sua mochila está vazia.")
