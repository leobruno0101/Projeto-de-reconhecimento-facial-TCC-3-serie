import sqlite3
from datetime import datetime

from Tools.scripts.find_recursionlimit import RecursiveBlowup1

conn = sqlite3.connect('DB_ReconhecimentoFacial.db')
c = conn.cursor()

c.execute("PRAGMA foreign_keys = ON")

def TBL_imagem():
    c.execute("""CREATE TABLE IF NOT EXISTS tbl_imagens(
                id_img INTEGER PRIMARY KEY AUTOINCREMENT,
                img_caminho text NOT NULL,
                id_pessoa_img INTEGER
                )""")
    return c

def TBL_cidade():
    c.execute("""CREATE TABLE IF NOT EXISTS tbl_cidade(
                    id_cidade INTEGER PRIMARY KEY AUTOINCREMENT,
                    cid_nome text NOT NULL,
                    cid_UF TEXT NOT NULL
                )""")
    return c

def TBL_pessoa():
    c.execute("""CREATE TABLE IF NOT EXISTS tbl_pessoa(
                id_pessoa INTEGER PRIMARY KEY AUTOINCREMENT,
                pes_nome TEXT NOT NULL,
                pes_CPF TEXT NOT NULL,
                pes_tell TEXT NOT NULL,
                pes_rg TEXT NOT NULL,
                pes_nasc TEXT NOT NULL,
                pes_email TEXT NOT NULL,
                id_cidade INTEGER
                )""")
    return c

def TBL_acesso():
    c.execute('''CREATE TABLE IF NOT EXISTS tbl_acesso(
                id_acesso INTEGER PRIMARY KEY AUTOINCREMENT,
                ace_horaEntrada TEXT NOT NULL,
                id_pessoa_ace INTEGER
            )''')
    return c

def TBL_usuarios():
    c.execute('''Create TABLE IF NOT EXISTE usuarios(
                id_usu INTEGER PRIMARY KEY AUTOINCREMENT,
                usu_usuario text NOT NULL,
                usu_senha text NOT NULL
                )''')
    return c



def registrar_pessoa():
    c = TBL_pessoa()
    c.execute("""INSERT INTO tbl_pessoa (pes_nome, pes_CPF, pes_tell, pes_rg, pes_nasc, pes_email) VALUES ('Leonardo Bruno', '123.123.123-45', '(34)99999-1234', 'MG-123132123', '2006-11-18', 'leozim@hotmail.com')""")
    conn.commit()


def exibir_acessos():
    c = TBL_acesso()
    c.execute("SELECT * FROM tbl_acesso")
    entradas = c.fetchall()
    for entrada in entradas:
        print(f"ID: {entrada[0]}, Nome: {entrada[2]}, Hora de Entrada: {entrada[1]}")


def registrar_entrada(nome):
    c = TBL_acesso()
    hora_atual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    c.execute("INSERT INTO tbl_acesso (nome, hora_entrada) VALUES (?, ?)", (nome, hora_atual))
    conn.commit()
    print(f"Entrada registrada: {nome} às {hora_atual}")

def selecionarPessoas():
    c = TBL_pessoa()
    c.execute("SELECT * FROM tbl_pessoa")
    entradas = c.fetchall()
    for entrada in entradas:
        print(f"ID: {entrada[0]}, Nome: {entrada[1]}, CPF: {entrada[2]}, telefone: {entrada[3]}, RG: {entrada[4]}, Data de nascimento: {entrada[5]}, Email: {entrada[6]}")




if __name__ == '__main__':
    exibir_acessos()







