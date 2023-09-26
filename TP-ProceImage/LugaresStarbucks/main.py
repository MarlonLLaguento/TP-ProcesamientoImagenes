import cv2
import pickle

img = cv2.imread('LugaresStarbucks/frame_inicial.png') #abriendo el primer frame

espacios = []

for x in range(12):
    cv2.namedWindow('espacio', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('espacio', 800, 600) #redimencionar la ventana para seleccionar las áreas de interés
    espacio = cv2.selectROI('espacio', img, False) #seleccionar las áreas de interés
    
    cv2.destroyWindow('espacio') #guardar las areas de interés con la tecla espacio
    espacios.append(espacio)

for x, y, w, h in espacios:
    cv2.rectangle(img, (x, y), (x+w, y+h), (255,0,0), 2)

with open('espacios.pkl','wb') as file: #guardado de las coordenadas en un archivo pkl
    pickle.dump(espacios, file)