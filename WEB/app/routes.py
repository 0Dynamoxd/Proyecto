from flask import request, jsonify, render_template, current_app
import cv2
import numpy as np
import mediapipe as mp
import os

# Inicialización de MediaPipe
mp_hands = mp.solutions.hands

def detectar_letra(image_bytes):
    objeto_hands = mp_hands.Hands(static_image_mode=True, max_num_hands=1, min_detection_confidence=0.5)
    nparr = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    alto, ancho, _ = image.shape
    RGBframe = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    resultados = objeto_hands.process(RGBframe)

    letra_detectada = "No detectada"
    if resultados.multi_hand_landmarks:
        for puntos in resultados.multi_hand_landmarks:
            dedo_pulgar = puntos.landmark[4]
            dedo_indice = puntos.landmark[8]
            dedo_medio = puntos.landmark[12]
            dedo_anular = puntos.landmark[16]
            dedo_menique = puntos.landmark[20]
            punto_central = puntos.landmark[9]
            punto_superior = puntos.landmark[5]

            coorPlgY = int(dedo_pulgar.y * alto)
            coorIndY = int(dedo_indice.y * alto)
            coorMedY = int(dedo_medio.y * alto)
            coorAnlY = int(dedo_anular.y * alto)
            coorMnqY = int(dedo_menique.y * alto)
            coorCenY = int(punto_central.y * alto)
            coorSupY = int(punto_superior.y * alto)

            if coorIndY > coorCenY and coorMedY > coorCenY and coorAnlY > coorCenY and coorMnqY > coorCenY and coorPlgY < coorSupY:
                letra_detectada = "A"
            elif coorPlgY > coorCenY and coorIndY > coorSupY and coorMedY > coorSupY and coorAnlY > coorSupY and coorMnqY > coorSupY:
                letra_detectada = "E"
            elif coorMnqY < coorCenY and coorIndY > coorCenY and coorMedY > coorCenY and coorAnlY > coorCenY:
                letra_detectada = "I"
            elif coorIndY < coorCenY and coorPlgY < coorCenY:
                letra_detectada = "O"
            elif coorIndY < coorCenY and coorMedY < coorCenY and coorAnlY > coorCenY and coorMnqY > coorCenY:
                letra_detectada = "U"

    return letra_detectada

# Ruta principal
@current_app.route('/')
def index():
    return render_template('index.html')

# Ruta para análisis de imagen
@current_app.route('/analyze', methods=['POST'])
def analyze():
    image = request.files['image'].read()
    resultado = detectar_letra(image)
    return jsonify({"letra_detectada": resultado})

# Ruta para lista de videos
@current_app.route('/api/videos')
def get_videos():
    video_folder = os.path.join(current_app.static_folder, 'videos')
    try:
        videos = [f for f in os.listdir(video_folder) if f.endswith('.mp4')]
        return jsonify(videos)
    except Exception as e:
        return jsonify({"error": str(e)})
