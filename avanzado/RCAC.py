import cv2
import os
import imutils

def ejecutar(nombre_carpeta):
    
    rutadata = "C:/Users/ariad/OneDrive/Documentos/achinti/trabajo_nacional/data"
    personadata = os.path.join(rutadata, nombre_carpeta)

    if not os.path.exists(personadata):
        print("Carpeta creada:", personadata)
        os.makedirs(personadata)

    cap = cv2.VideoCapture(0)

    faceclasif = cv2.CascadeClassifier('C:/Users/ariad/OneDrive/Documentos/achinti/trabajo_nacional/base de datos/haarcascade_frontalface_default.xml')
    count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = imutils.resize(frame, width=320)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        auxframe = frame.copy()

        faces = faceclasif.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            rostro = auxframe[y:y+h, x:x+w]
            rostro = cv2.resize(rostro, (720, 720), interpolation=cv2.INTER_CUBIC)
            filename = f'rostro_{count}.jpg'
            path = os.path.join(personadata, filename)
            cv2.imwrite(path, rostro)
            count += 1

        cv2.imshow("RCAC", frame)

        k = cv2.waitKey(1)
        if k == 27 or count >= 200:
            break

    cap.release()
    cv2.destroyAllWindows()