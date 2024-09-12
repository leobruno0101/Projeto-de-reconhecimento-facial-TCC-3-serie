import sqlite3
from datetime import datetime


conn = sqlite3.connect('registro_entrada.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS entradas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                hora_entrada TEXT NOT NULL
            )''')

def registrar_entrada(nome):
    hora_atual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    c.execute("INSERT INTO entradas (nome, hora_entrada) VALUES (?, ?)", (nome, hora_atual))
    conn.commit()
    print(f"Entrada registrada: {nome} às {hora_atual}")


def exibir_entradas():
    c.execute("SELECT * FROM entradas")
    entradas = c.fetchall()
    for entrada in entradas:
        print(f"ID: {entrada[0]}, Nome: {entrada[1]}, Hora de Entrada: {entrada[2]}")

if __name__ == '__main__':
    exibir_entradas()







