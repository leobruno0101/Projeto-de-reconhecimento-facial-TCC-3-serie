import tkinter as tk
from tkinter import Frame, Label, Entry, Button
from PIL import Image, ImageTk
import os


class Login:
    def __init__(self, master=None):
        self.master = master
        self.master.title("Tela de Login")

        # Frame esquerdo (azul)
        self.frameEsquerdo = Frame(master, width=300, bg="#7DC4F5")
        self.frameEsquerdo.pack(side=tk.LEFT, fill=tk.Y)

        # Frame direito
        self.frameDireito = Frame(master, width=300, bg="#7DC4F5")
        self.frameDireito.pack(side=tk.RIGHT, fill=tk.Y)

        # Frame principal
        self.janela = Frame(master)
        self.janela.pack(padx=20, pady=20)

        self.fontePadrao = ("Arial", 15, "bold")

        # Imagem (opcional)
        try:
            image_path = "imagemLogin.png"
            if os.path.exists(image_path):
                image = Image.open(image_path)
                photo = ImageTk.PhotoImage(image)
                self.imagem = Label(self.janela, image=photo)
                self.imagem.image = photo
                self.imagem.pack(pady=10)
            else:
                raise FileNotFoundError("A imagem não foi encontrada.")
        except Exception as e:
            self.imagem = Label(self.janela, text="Erro ao carregar a imagem.")
            self.imagem.pack(pady=10)
            print(e)

        # Container para o nome
        self.janela2 = Frame(self.janela, padx=20, pady=5)
        self.janela2.pack()

        self.nome = Label(self.janela2, text="Nome:", font=self.fontePadrao)
        self.nome.pack()

        self.nomeR = Entry(self.janela2, width=30, font=("Arial", 15))
        self.nomeR.pack(side=tk.LEFT)

        # Container para a senha
        self.janela3 = Frame(self.janela, padx=20, pady=5)
        self.janela3.pack()

        self.senha = Label(self.janela3, text="Senha:", font=self.fontePadrao)
        self.senha.pack()

        self.senhaR = Entry(self.janela3, width=30, font=("Arial", 15), show="*")
        self.senhaR.pack(side=tk.LEFT)

        # Container para o botão
        self.janela4 = Frame(self.janela, padx=20, pady=10)
        self.janela4.pack()

        self.autenticar = Button(self.janela4, text="Entrar", font=self.fontePadrao, command=self.verificaSenha)
        self.autenticar.pack()

        # Mensagem de autenticação
        self.mensagem = Label(self.janela4, font=self.fontePadrao)
        self.mensagem.pack()

    # Verificação de senha
    def verificaSenha(self):
        usuario = self.nomeR.get()
        senha = self.senhaR.get()
        if usuario == "Reconhecimento" and senha == "12345678":
            self.mensagem["text"] = "Autenticado!"
            self.abrir_tela_tabela()  # Abre a tela da tabela após autenticação
        else:
            self.mensagem["text"] = "Erro na autenticação!"

    # Função para abrir a tela da tabela
    def abrir_tela_tabela(self):
        self.master.destroy()  # Fecha a janela de login
        root2 = tk.Tk()
        root2.title("Tabela de Informações")
        root2.state("zoomed")

        root2.mainloop()

# Inicializa a janela de login

root = tk.Tk()
root.state("zoomed")
Login(root)
root.mainloop()