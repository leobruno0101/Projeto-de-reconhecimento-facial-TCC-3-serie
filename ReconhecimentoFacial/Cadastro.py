import tkinter as tk
from tkinter import ttk
import cv2
from PIL import Image, ImageTk
import numpy as np
from tkinter import messagebox, filedialog
import subprocess
from Banco import TBL_pessoa, TBL_cidade, conn, TBL_imagem

ufs_brasil = [
    "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO",
    "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI",
    "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"
]

image=''

def capturarFoto():
    global image
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    if ret:
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(frame_rgb)
        img_pil = img_pil.resize((450, 350))
        img_tk = ImageTk.PhotoImage(image=img_pil)
        Mostrarimg.config(image=img_tk,bg="#012A4A", borderwidth=0)
        Mostrarimg.image = img_tk
        image = np.array(frame)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

def abrirarquivo():
    global image
    caminho_arquivo = filedialog.askopenfilename(
        title="Selecionar Arquivo",
        filetypes=(("Todos os arquivos", "*.*"), ("Arquivos de Texto", "*.txt"))
    )
    frame = Image.open(caminho_arquivo)
    frame = frame.resize((450,350))
    img_tk = ImageTk.PhotoImage(image=frame)
    Mostrarimg.config(image=img_tk,bg="#012A4A", borderwidth=0)
    Mostrarimg.image = img_tk
    image = np.array(frame)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

def cadCidade(cid,UF):
    c = TBL_cidade()
    c.execute("select cid_nome from tbl_cidade")
    id = c.fetchall()
    for i in id:
        if i == cid:
            return
    c.execute("Insert into tbl_cidade(cid_nome, cid_UF) values (?,?)",(cid,UF))
    conn.commit()

def Procurarcidade(cid):
    c = TBL_cidade()
    c.execute("select id_cidade from tbl_cidade where cid_nome = ?",(cid,))
    id = c.fetchone()
    conn.commit()
    return id[0]


def cadpessoa():
    nome = entry_nome.get()
    cpf = entry_cpf.get()
    RG = entry_rg.get()
    nasc = entry_datanasci.get()
    tell = entry_telefone.get()
    email = entry_email.get()
    cidade = entry_cidade.get()
    UF = comb_UF.get()
    if not nome or not cpf or not RG or not nasc or not tell or not email or not cidade or not UF:
        messagebox.showinfo("OPÁ!!","Por favor complete todos os campos!")
        return

    cadCidade(cidade,UF)
    cidade = Procurarcidade(cidade)
    c = TBL_pessoa()
    c.execute("select pes_CPF from tbl_pessoa")
    CP = c.fetchall()
    for i in CP:
        if i == cpf:
            messagebox.showinfo("OPÁ!!","Este CPF já está cadastrado")
            return

    c.execute("INSERT INTO tbl_pessoa (pes_nome, pes_CPF, pes_tell, pes_rg, pes_nasc, pes_email,id_cidade) VALUES (?,?,?,?,?,?,?)",(nome,cpf,tell,RG,nasc,email,cidade))
    conn.commit()

def Procurarpessoa(pes):
    c = TBL_pessoa()
    c.execute("select id_pessoa from tbl_pessoa where pes_CPF = ?",(pes,))
    id = c.fetchone()
    conn.commit()
    return id[0]

def cadastrar():
    global image
    cadpessoa()
    cpf = entry_cpf.get()
    id_pessoa = Procurarpessoa(cpf)
    cv2.imwrite(f"Pessoas/{id_pessoa}.jpg", image)
    caminho = (f"Pessoas/{id_pessoa}.jpg")
    c = TBL_imagem()
    c.execute("insert into tbl_imagens(img_caminho, id_pessoa_img) Values (?,?)",(caminho,id_pessoa))
    conn.commit()
    messagebox.showinfo("Cadastrado", "Seu cadastro foi feito com sucesso!!")


# Janela principal
root = tk.Tk()
root.title("Cadastro")
root.geometry("600x600")

UF = tk.StringVar(root)

# Alterar a cor de fundo da janela principal para preto
root.configure(bg="#252525")

# Frame 1 para os componentes de login, com o fundo azul escuro
frame1 = tk.Frame(root, bg="#012A4A", bd=0)
frame1.pack(pady=(0, 1))  # Definindo espaçamento vertical
frame1.place(relx=0.5, rely=0.5, anchor=tk.CENTER, relwidth=0.7, relheight=0.9)  # Alongado horizontalmente

# CPF
label_nome = tk.Label(frame1, text="Nome Completo", font=("Arial", 17), bg="#012A4A", fg="lightgray")
label_nome.place(relx=0.1, rely=0.05)
entry_nome = tk.Entry(frame1, font=("Arial", 12), bg="lightgray", bd=2)
entry_nome.place(relx=0.1, rely=0.1, relwidth=0.8)

label_cpf = tk.Label(frame1, text="CPF", font=("Arial", 17), bg="#012A4A", fg="lightgray")
label_cpf.place(relx=0.1, rely=0.15)
entry_cpf = tk.Entry(frame1, font=("Arial", 12), bg="lightgray", bd=2)
entry_cpf.place(relx=0.1, rely=0.2, relwidth=0.35)

label_rg = tk.Label(frame1, text="RG", font=("Arial", 17), bg="#012A4A", fg="lightgray")
label_rg.place(relx=0.55, rely=0.15)
entry_rg = tk.Entry(frame1, font=("Arial", 12), bg="lightgray", bd=2)
entry_rg.place(relx=0.55, rely=0.2, relwidth=0.35)

# data
label_datanasci = tk.Label(frame1, text="Data de Nascimento", font=("Arial", 17), bg="#012A4A", fg="lightgray")
label_datanasci.place(relx=0.1, rely=0.25)
entry_datanasci = tk.Entry(frame1, font=("Arial", 12), bg="lightgray", bd=2)
entry_datanasci.place(relx=0.1, rely=0.3, relwidth=0.35)

label_telefone = tk.Label(frame1, text="Telefone", font=("Arial", 17), bg="#012A4A", fg="lightgray")
label_telefone.place(relx=0.55, rely=0.25)
entry_telefone = tk.Entry(frame1, font=("Arial", 12), bg="lightgray", bd=2)
entry_telefone.place(relx=0.55, rely=0.3, relwidth=0.35)

label_email = tk.Label(frame1, text="Email", font=("Arial", 17), bg="#012A4A", fg="lightgray")
label_email.place(relx=0.1, rely=0.35)
entry_email = tk.Entry(frame1, font=("Arial", 12), bg="lightgray", bd=2)
entry_email.place(relx=0.1, rely=0.4, relwidth=0.8)

label_cidade = tk.Label(frame1, text="Nome da cidade", font=("Arial", 17), bg="#012A4A", fg="lightgray")
label_cidade.place(relx=0.1, rely=0.45)
entry_cidade = tk.Entry(frame1, font=("Arial", 12), bg="lightgray", bd=2)
entry_cidade.place(relx=0.1, rely=0.5, relwidth=0.35)

style = ttk.Style()
style.theme_use('clam')
style.configure("TCombobox", fieldbackground="lightgray")  # Define a cor de fundo

label_UF = tk.Label(frame1, text="Unidade Federativa", font=("Arial", 17), bg="#012A4A", fg="lightgray")
label_UF.place(relx=0.55, rely=0.45)
comb_UF = ttk.Combobox(root, font=("Arial", 13), values=ufs_brasil)
comb_UF.configure(background="lightgray", foreground="black")
comb_UF.place(relx=0.534, rely=0.5, relwidth=0.247)

Bcapturar = tk.Button(frame1, text="Fazer captura" , font=("Arial", 12), bg="lightgray", command=capturarFoto)
Bcapturar.place(relx=0.11, rely=0.75, relwidth=0.15, relheight=0.06)

Bbuscar = tk.Button(frame1, text="Buscar imagem" , font=("Arial", 12), bg="lightgray", command=abrirarquivo)
Bbuscar.place(relx=0.11, rely=0.63  , relwidth=0.15, relheight=0.06)

Mostrarimg = tk.Label(frame1, text="Esperando uma Imagem", font=("Arial", 12, "bold"), bg="lightgray", borderwidth=2, relief="solid")
Mostrarimg.place(relx=0.295, rely=0.57, relwidth=0.4, relheight=0.37)

Binserir = tk.Button(frame1, text="Cadastrar" , font=("Arial", 12), bg="lightgray", command=cadastrar)
Binserir.place(relx=0.737, rely=0.6  , relwidth=0.15, relheight=0.06)

Balterar = tk.Button(frame1, text="Alterar" , font=("Arial", 12), bg="lightgray")
Balterar.place(relx=0.737, rely=0.7  , relwidth=0.15, relheight=0.06)

Bdeletar = tk.Button(frame1, text="Deletar" , font=("Arial", 12), bg="lightgray")
Bdeletar.place(relx=0.737, rely=0.8  , relwidth=0.15, relheight=0.06)








# Estado da janela maximizado
root.state("zoomed")
root.mainloop()