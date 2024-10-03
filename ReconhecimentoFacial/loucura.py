import cv2

# Inicializa a captura de vídeo a partir da webcam (0 é o índice da câmera padrão)
cap = cv2.VideoCapture(0)

# Verifica se a webcam foi aberta corretamente
if not cap.isOpened():
    print("Erro ao acessar a webcam")
    exit()

nome = 'leozim'

# Lê um frame (quadro de vídeo) da webcam
ret, frame = cap.read()

# Verifica se o frame foi capturado corretamente
if ret:
    # Exibe o frame capturado em uma janela
    cv2.imshow("Imagem Capturada", frame)

    print(type(frame))
    # Salva a imagem capturada
    cv2.imwrite(f"Pessoas/{nome}.jpg", frame)
    print("Imagem capturada e salva como 'captura_webcam.jpg'")

    # Aguarda até que o usuário pressione qualquer tecla para fechar a janela
    cv2.waitKey(0)

# Libera o dispositivo de captura e fecha todas as janelas
cap.release()
cv2.destroyAllWindows()