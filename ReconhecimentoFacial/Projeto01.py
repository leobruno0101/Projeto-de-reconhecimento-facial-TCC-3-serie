import cv2
import face_recognition as fr
import os
import cvzone
from pyfirmata import Arduino,SERVO
from datetime import datetime
import time
from Banco import TBL_acesso, conn, TBL_pessoa

# board = Arduino('COM3')
# board.digital[8].mode = SERVO
#
# def rotateServo(angle):
#     board.digital[8].write(angle)
#     time.sleep(0.015)
#
# ledVM = board.get_pin('d:7:o')
# ledVD = board.get_pin('d:5:o')
# ledAM = board.get_pin('d:6:o')

def Procurarpessoa(pes):
    c = TBL_pessoa()
    c.execute("select id_pessoa from tbl_pessoa where pes_CPF = ?",(pes,))
    id = c.fetchone()
    conn.commit()
    return id[0]

def registrar_entrada(id_pessoa):
    c = TBL_acesso()
    hora_atual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    c.execute("INSERT INTO tbl_acesso (ace_horaEntrada, id_pessoa_ace) VALUES (?, ?)", (hora_atual, id_pessoa))
    conn.commit()
    print(f"Registro feito com sucesso!! informações:\n data: {hora_atual}\n pessoa: {id_pessoa}")

nomes = []
encods = []

lista = os.listdir("Pessoas")

# Carregar base de dados de pessoas altorizadas
for arquivo in lista:
    img = cv2.imread(f"Pessoas/{arquivo}")
    img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    encods.append(fr.face_encodings(img)[0])
    nomes.append(os.path.splitext(arquivo)[0])

def compararENC(encImg):
    for id,enc in enumerate(encods):
        comp = fr.compare_faces([encImg],enc)
        if comp[0]:
            break

    return comp[0], nomes[id]

print('Base carregada!')

video = cv2.VideoCapture(0)

faceloc = []

def reconhecer():
    while True:
        check, img = video.read()
        imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        try:
            faceloc.append(fr.face_locations(imgRGB)[0])
        except:
            faceloc = []

        if faceloc:
            # ledAM.write(1)
            y1, x2, y2, x1 = faceloc[-1]
            w, h = x2 - x1, y2 - y1
            cvzone.cornerRect(img,(x1,y1,w,h), colorR=(255,0,0))
            cvzone.putTextRect(img,'Analisando ...',(50,50), colorR=(255,0,0))

        if len(faceloc)>20:
            encodeIMG = fr.face_encodings(imgRGB)[0]
            comp, ID_pessoa = compararENC(encodeIMG)
            print(ID_pessoa)

            if comp:
                registrar_entrada(ID_pessoa)
                cvzone.putTextRect(img,'Acesso Liberado',(50,50), colorR=(0,255,0))
                # ledAM.write(0)
                # ledVD.write(1)
                # rotateServo(130)
                # time.sleep(2)
                # rotateServo(0)
                # ledVD.write(0)
                time.sleep(4)
            else:
                cvzone.putTextRect(img, 'Acesso Negado', (50, 50), colorR=(0, 0, 255))
                # ledAM.write(0)
                # ledVM.write(1)
                # time.sleep(2)
                # ledVM.write(0)

        cv2.imshow('IMG',img)
        cv2.waitKey(1)


if __name__ == '__main__':
    reconhecer()










