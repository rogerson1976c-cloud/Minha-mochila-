import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Configuração da Página
st.set_page_config(page_title="Mochila Rogerson", page_icon="🎒")

# Nome do arquivo de dados
DB_FILE = "estoque_mochila.csv"

def carregar_dados():
    if os.path.exists(DB_FILE):
        df = pd.read_csv(DB_FILE)
        # Tenta pegar a data de modificação do arquivo
        mod_time = os.path.getmtime(DB_FILE)
        dt_mod = datetime.fromtimestamp(mod_time).strftime('%d/%m/%Y às %H:%M')
        return df, dt_mod
    return pd.DataFrame(columns=["Item", "Categoria", "Data de Validade"]), "Nenhuma"

# Carregamento inicial
estoque, ultima_atualizacao = carregar_dados()

st.title("🎒 Minha Mochila")
st.info(f"🕒 Última atualização na nuvem: {ultima_atualizacao}")

# --- INTERFACE DE ADIÇÃO ---
with st.expander("➕ Adicionar/Editar Itens"):
    with st.form("form_item", clear_on_submit=True):
        nome = st.text_input("Nome do Item")
        cat = st.selectbox("Categoria", ["Alimentação", "Saúde", "Ferramentas", "Outros"])
        indet = st.checkbox("Validade Indeterminada")
        val = st.date_input("Data de Validade")
        
        if st.form_submit_button("Sincronizar com a Nuvem"):
            data_txt = "Indeterminada" if indet else val.strftime('%d/%m/%Y')
            novo = pd.DataFrame([[nome, cat, data_txt]], columns=estoque.columns)
            estoque = pd.concat([estoque, novo], ignore_index=True)
            estoque.to_csv(DB_FILE, index=False)
            st.success("Atualizado na nuvem e disponível para todos os seus aparelhos!")
            st.rerun()

# --- TABELA DE ITENS ---
st.write("### Itens no Inventário")
st.dataframe(estoque, use_container_width=True)

# --- FUNÇÃO OFFLINE ---
st.write("---")
st.subheader("🌐 Modo Offline")
st.write("Para acessar sem sinal, clique no botão abaixo e salve o arquivo. Se a internet cair, você abre este arquivo no seu celular.")

csv = estoque.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Baixar Versão Offline Atualizada",
    data=csv,
    file_name=f'mochila_backup_{datetime.now().strftime("%d-%m")}.csv',
    mime='text/csv',
)
