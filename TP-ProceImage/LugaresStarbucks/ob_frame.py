import cv2

cap = cv2.VideoCapture('LugaresStarbucks/starbuck.mp4') #abriendo video

if not cap.isOpened():
    print("No se pudo abrir el video.")
    exit()

ret, frame = cap.read()

if not ret:
    print("No se pudo leer el primer frame del video.")
    exit()

cv2.imwrite('frame_inicial.png', frame) #guardando el primer frame para usarlo como captura para las áreas interés

cap.release()
#print(frame.shape)