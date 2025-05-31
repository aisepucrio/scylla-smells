import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess

def selecionar_pasta():
    """Abre o seletor de diretórios para escolher a pasta com arquivos .py."""
    pasta = filedialog.askdirectory()
    if pasta:
        entry_pasta.delete(0, tk.END)
        entry_pasta.insert(0, pasta)

def executar_analise():
    """Executa o script principal para analisar os arquivos da pasta escolhida."""
    pasta = entry_pasta.get()
    if not pasta:
        messagebox.showwarning("Aviso", "Por favor, selecione uma pasta antes de iniciar a análise.")
        return
    
    try:
        subprocess.run(["python", "main.py", pasta], check=True)
        messagebox.showinfo("Sucesso", "Análise concluída! O arquivo CSV foi gerado com os resultados.")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Erro", f"Ocorreu um erro ao executar a análise: {e}")

# Configuração da interface gráfica
root = tk.Tk()
root.title("Analisador de Code Smells")
root.geometry("400x250")

tk.Label(root, text="Selecione a pasta para análise:").pack(pady=30)

frame = tk.Frame(root)
frame.pack(pady=5)

entry_pasta = tk.Entry(frame, width=40)
entry_pasta.pack(side=tk.LEFT, padx=5)

btn_selecionar = tk.Button(frame, text="Selecionar", command=selecionar_pasta)
btn_selecionar.pack(side=tk.LEFT)

btn_analisar = tk.Button(root, text="Iniciar Análise", command=executar_analise)
btn_analisar.pack(pady=50)

root.mainloop()
