import streamlit as st
import os
from analisador.main import check_code_smells_in_directory
from tkinter import Tk, filedialog

# Configuração da página
st.set_page_config(page_title="Detector de Code Smells", layout="centered")

st.title("👨‍💻 Detector de Code Smells em Python")
st.markdown("Selecione uma pasta com arquivos `.py` para análise. O sistema analisará subpastas também.")

# Campo de entrada manual
folder_path = st.text_input("📁 Caminho da pasta (manual):", "")

# Botão para abrir seletor de pasta
def select_folder():
    root = Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    folder_selected = filedialog.askdirectory()
    root.destroy()
    return folder_selected

if st.button("📂 Selecionar pasta com botão"):
    selected = select_folder()
    if selected:
        folder_path = selected
        st.experimental_rerun()

# Botão de análise
if st.button("🔍 Analisar"):
    if folder_path and os.path.exists(folder_path):
        check_code_smells_in_directory(folder_path)
        st.success("✅ Análise concluída! Arquivo `code_smells.csv` gerado.")
        with open("code_smells.csv", "rb") as f:
            st.download_button("📥 Baixar code_smells.csv", f, file_name="code_smells.csv")
    else:
        st.error("❌ Caminho inválido. Verifique e tente novamente.")
