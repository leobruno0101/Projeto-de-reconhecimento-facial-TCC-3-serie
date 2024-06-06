import cv2 as cv

img = cv.imread('imagens/gato-grande.jpg')
cv.imshow('gato',img)

def rescaleframe(frame, scale=0.75):
    largura = int(frame.shape[1] * scale)
    altura = int(frame.shape[0] * scale)

    dimensoes = (largura,altura)

    return  cv.resize(frame, dimensoes, interpolation=cv.INTER_AREA)

cv.inshow


Captura = cv.VideoCapture('videos/CatFamily1.mov')

while True:
    istrue, frame = Captura.read()

    frame_resize = rescaleframe(frame.5)

    cv.imshow('video', frame)
    cv.imshow('video redimencionado', frame_resize)

    if cv.waitKey(20) & 0xFF==ord('d'):
        break

Captura.release()
cv.destroyAllWindows()