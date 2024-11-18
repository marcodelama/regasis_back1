import mediapipe as mp

# # Intenta acceder al módulo drawing_utils
# try:
#     mp_drawing = mp.solutions.drawing_utils
#     print("drawing_utils está disponible:", mp_drawing)
# except AttributeError:
#     print("drawing_utils no está disponible en esta versión de MediaPipe.")

import cv2
import imutils

# cap = cv2.VideoCapture(0)
# if not cap.isOpened():
#     print("No se pudo acceder a la cámara")
# else:
#     ret, frame = cap.read()
#     if ret:
#         print("La cámara funciona correctamente")
#     else:
#         print("No se pudo leer el frame de la cámara")
#     cap.release()

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

mp_drawing = mp.solutions.drawing_utils
drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)


def Log_Biometric():
    global pantalla2, conteo, parpadeo, img_info, step, cap, lblVideo

    if cap is not None:
        ret, frame = cap.read()
        
        if ret:
            # Redimensionar el frame
            frame = imutils.resize(frame, width=1280)
            
            # Convertir a RGB (MediaPipe requiere RGB)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Procesar el frame con MediaPipe
            results = face_mesh.process(frame_rgb)
            
            # Dibujar la malla facial si se detecta un rostro
            if results.multi_face_landmarks:
                for face_landmarks in results.multi_face_landmarks:
                    mp_drawing.draw_landmarks(
                        image=frame,
                        landmark_list=face_landmarks,
                        connections=mp_face_mesh.FACEMESH_TESSELATION,
                        landmark_drawing_spec=drawing_spec,
                        connection_drawing_spec=drawing_spec
                    )
            
            # Convertir el frame procesado a formato RGB para Tkinter
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Convertir a formato PIL
            im = Image.fromarray(frame_rgb)
            img = ImageTk.PhotoImage(image=im)
            
            # Actualizar la imagen en la interfaz
            lblVideo.configure(image=img)
            lblVideo.image = img
            lblVideo.after(10, Log_Biometric)
    else:
        if cap is not None:
            cap.release()