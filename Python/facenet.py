from PIL import Image
from os import listdir
from os.path import isdir
from numpy import asarray, expand_dims
import numpy as np


# (3°)
def load_face(filename):
    #Carregando imagem do arquivo
    image = Image.open(filename)

    #converter para RGB
    image = image.convert("RGB")

    return asarray(image)


#Carregando imagens de face de um diretório (2)°

def load_faces(directory_src):

    faces = list()

    #iterando arquivos
    for filename in listdir(directory_src):
        
        path = directory_src + filename

        try:
            faces.append(load_face(path))
        except:
            print("Error na imagem".format(path))
    
    return faces

#Carregando todo o dataset de imagens de faces (1°)

def load_fotos(directory_src):

    X, y = list(), list()

    #iterar pastas por classes
    for subdir in listdir(directory_src):
        #path
        path = directory_src + subdir + "\\"

        if not isdir(path):
            continue

        faces = load_faces(path)

        labels = [subdir for _ in range(len(faces ))]

        #sumarizar progresso
        print('>Carregadas %d faces da classe: %s' % (len(faces), subdir))

        X.extend(faces)
        y.extend(labels)
    
    return asarray(X), asarray(y)

#Após isso tudo ele abre em cadeira lá pra cima 



#Carregando todas as imagens

trainX, trainy = load_fotos(directory_src = "C:\\TCC\\faces\\")



from tensorflow.keras.models import load_model

model = load_model('facenet_keras.h5')

model.summary()

def get_embedding(model, face_pixels):
    
    #Realizar uma padronização
    mean, std = face_pixels.mean(), face_pixels.std()

    face_pixels = (face_pixels - mean)/std   #Melhorar na hora de identificar caracteristicas

    #transformar a face em 1 único exemplo

    ##(160,160) -> (1,160,160)

    samples = expand_dims(face_pixels, axis=0)

    #Realizar a predição gerando o embedding
    yhat = model.predict(samples)

    #Pegar apenas a primeira posição que a matriz retorna 
    
    return yhat[0]
 
newTrainX = list()

for face in trainX:
    embedding = get_embedding(model, face)
    newTrainX.append(embedding)

newTrainX = asarray(newTrainX)

newTrainX.shape

import pandas as pd

df = pd.DataFrame(data=newTrainX)

df

df['target'] = trainy

df

df.to_csv('faces.csv')
