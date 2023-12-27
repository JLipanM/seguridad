import cv2
import os
from deepface import DeepFace


caras_db = {}
for nombre in os.listdir('dataset'):
    for foto in os.listdir(f'dataset/{nombre}'):
        caras_db[nombre] = f'dataset/{nombre}/{foto}'


captura = cv2.VideoCapture(0)

while True:

    retorno, cuadro = captura.read()

    cuadro_rgb = cuadro[:, :, ::-1]


    caras_detectadas = DeepFace.extract_faces(cuadro_rgb,enforce_detection= False)

    for cara in caras_detectadas:

        x = cara['facial_area']['x']
        y = cara['facial_area']['y']
        w = cara['facial_area']['w']
        h = cara['facial_area']['h']


        cv2.rectangle(cuadro, (x, y), (x+w, y+h), (0, 0, 255), 2)


        fuente = cv2.FONT_HERSHEY_DUPLEX
        nombre = "Desconocido"
        for nombre_conocido, ruta_archivo_img in caras_db.items():
            result = DeepFace.verify(cuadro_rgb, ruta_archivo_img, model_name='Facenet512', distance_metric='cosine', enforce_detection=False)
            if result['verified']:
                nombre = nombre_conocido
                break
        cv2.putText(cuadro, nombre, (x + 6, y - 6), fuente, 1.0, (255, 255, 255), 1)


    cv2.imshow('Video', cuadro)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


captura.release()
cv2.destroyAllWindows()