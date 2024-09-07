import tkinter as tk
from tkinter import messagebox, ttk
import psycopg2
from datetime import datetime

# Função para conectar ao banco de dados Postgree
def conectar_banco():
    conn = psycopg2.connect(
        dbname="vendas_db",
        user="seu_usuario",
        password="sua_senha",
        host="localhost"
    )
    return conn

# Função para registrar uma venda
def registrar_venda():
    produto = entry_produto.get()
    quantidade = entry_quantidade.get()
    preco_unitario = entry_preco_unitario.get()
    data_venda = entry_data_venda.get()
    
    if not produto or not quantidade or not preco_unitario or not data_venda:
        messagebox.showerror("Erro", "Todos os campos devem ser preenchidos!")
        return

    try:
        quantidade = int(quantidade)
        preco_unitario = float(preco_unitario)
        data_venda = datetime.strptime(data_venda, "%Y-%m-%d").date()
    except ValueError:
        messagebox.showerror("Erro", "Quantidade deve ser um número inteiro, ")
        return

    conn = conectar_banco()
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO vendas (produto, quantidade, preco_unitario, data_venda)
    VALUES (%s, %s, %s, %s)
    ''', (produto, quantidade, preco_unitario, data_venda))
    
    conn.commit()
    conn.close()
    
    messagebox.showinfo("Sucesso", "Venda registrada!")
    limpar_campos()
    atualizar_tabela()

# Função para limpar os campos
def limpar_campos():
    entry_produto.delete(0, tk.END)
    entry_quantidade.delete(0, tk.END)
    entry_preco_unitario.delete(0, tk.END)
    entry_data_venda.delete(0, tk.END)

# Função para atualizar a tabela com vendas
def atualizar_tabela():
    for row in tabela.get_children():
        tabela.delete(row)
    
    conn = conectar_banco()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM vendas')
    vendas = cursor.fetchall()
    
    for venda in vendas:
        tabela.insert('', tk.END, values=venda)
    
    conn.close()

# Criar a janela principal
root = tk.Tk()
root.title("Sistema de Vendas")

# Labels e Entradas para registro de vendas
tk.Label(root, text="Produto").grid(row=0, column=0, padx=10, pady=5)
tk.Label(root, text="Quantidade").grid(row=1, column=0, padx=10, pady=5)
tk.Label(root, text="Preço Unitário").grid(row=2, column=0, padx=10, pady=5)
tk.Label(root, text="Data da Venda (YYYY-MM-DD)").grid(row=3, column=0, padx=10, pady=5)

entry_produto = tk.Entry(root)
entry_quantidade = tk.Entry(root)
entry_preco_unitario = tk.Entry(root)
entry_data_venda = tk.Entry(root)

entry_produto.grid(row=0, column=1, padx=10, pady=5)
entry_quantidade.grid(row=1, column=1, padx=10, pady=5)
entry_preco_unitario.grid(row=2, column=1, padx=10, pady=5)
entry_data_venda.grid(row=3, column=1, padx=10, pady=5)

tk.Button(root, text="Registrar Venda", command=registrar_venda).grid(row=4, column=0, columnspan=2, pady=10)

# Tabela para exibir vendas
tabela = ttk.Treeview(root, columns=("ID", "Produto", "Quantidade", "Preço Unitário", "Data Venda"), show='headings')
tabela.heading("ID", text="ID")
tabela.heading("Produto", text="Produto")
tabela.heading("Quantidade", text="Quantidade")
tabela.heading("Preço Unitário", text="Preço Unitário")
tabela.heading("Data Venda", text="Data Venda")

tabela.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

atualizar_tabela()

root.mainloop()