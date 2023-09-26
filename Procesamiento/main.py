import cv2
import pickle
import numpy as np
import time

estacionamientos = []
with open('Procesamiento/espacios.pkl', 'rb') as file: #abriendo el archivo pkl
    estacionamientos = pickle.load(file)

video = cv2.VideoCapture('Procesamiento/starbuck.mp4') #abriendo video

#listas para llevar el tiempo que llevan vacios u ocupados los sitios
times = []
times_1 = []
total = [0]*len(estacionamientos)
total_1 = [0]*len(estacionamientos)


while True:
    check, img = video.read()
    imgBN = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #se tranforma el frame img a gris
    imgBlur = cv2.GaussianBlur(imgBN,(3,3),1) #se aplica un suavizado al frame
    #aplicación del umbral
    imgTH = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
    imgMedian = cv2.medianBlur(imgTH, 5) #se elimina el ruido con la mediana
    kernel = np.ones((3,3), np.int8)
    imgDil = cv2.dilate(imgMedian, kernel) #aumenta el tamaño de los objetos
    i = 0

    for x, y, w, h in estacionamientos:
        espacio = imgDil[y:y+h, x:x+w]
        #count = cv2.countNonZero(espacio)
        count = cv2.countNonZero(255-espacio) #se cuentan los pixeles negros
        #count2 = cv2.countNonZero(espacio)
        #cv2.putText(img, str(count), (x,y+h-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,0), 1)
        
        cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,0), 2)
        if count < 17300 :
            cv2.rectangle(img, (x,y), (x+w, y+h), (0,255,0), 2)
            times.append(video.get(cv2.CAP_PROP_POS_MSEC))
            #se guarda el tiempo inicial del lugar vacío y se resta con el tiempo del mismo lugar ocupado
            total[i] =(times[-1] - times[0]) -total_1[i] 
            #se muestra el tiempo del lugar vacío
            cv2.putText(img, "Libre: {}".format(round(total[i]/1000,1)), (x,y+h-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,255,0), 1)
            
        else:
            times_1.append(video.get(cv2.CAP_PROP_POS_MSEC))
            total_1[i] = (times_1[-1] - times_1[0]) - total[i]
            cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,0), 2)
            #se muestra el tiempo del lugar ocupado
            cv2.putText(img, "Ocupado: {}".format(round(total_1[i]/1000,1)), (x,y+h-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,255,0), 1)
       
        i+=1
    cv2.namedWindow('video', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('video', 1080, 1280)
    cv2.imshow('video', img)

    #cv2.namedWindow('video TH', cv2.WINDOW_NORMAL)
    #cv2.resizeWindow('video TH', 800, 900)
    #cv2.imshow('video TH', imgTH)

    # cv2.imshow('video Median', imgMedian)

    #cv2.namedWindow('video Dilatada', cv2.WINDOW_NORMAL)
    #cv2.resizeWindow('video Dilatada', 1280, 1080)
    #cv2.imshow('video Dilatada', imgDil)
    cv2.waitKey(10)
