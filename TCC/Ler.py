import cv2 as cv
#ler imagens

#img = cv.imread('./Imagens/gato.jpg')

#cv.imshow('gato', img)

#cv.waitKey(0)
#-------------------------------------------------------

#ler videos
Captura = cv.VideoCapture('videos/CatFamily1.mov')

while True:
    istrue, frame = Captura.read()
    cv.imshow('video', frame)

    if cv.waitKey(20) & 0xFF==ord('d'):
        break

Captura.release()
cv.destroyAllWindows()



#-------------------------------------------------------------


