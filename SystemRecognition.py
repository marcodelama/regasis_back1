import cv2
import face_recognition as fr
import numpy as np
import mediapipe as mp
import os
from tkinter import *
from PIL import Image, ImageTk

#Rutas
OutFolderPathUser = 'C:/Users/Usuario/Desktop/RecognitionSystem/DataBase/Users'
OutFolderPathFace = 'C:/Users/Usuario/Desktop/RecognitionSystem/DataBase/Faces'

pantalla = Tk()
pantalla.title("FACE RECOGNITION")
pantalla.geometry("1280x720")

# Lista de usuarios y sus imágenes
images = []
clases = []

# Cargar imágenes de los usuarios para la comparación
def Code_Face(images):
    listacod = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        cod = fr.face_encodings(img)[0]
        listacod.append(cod)
    return listacod

# Verificar si la imagen coincide con un usuario almacenado
def verify_image(image_path):
    global images, clases

    # Cargar imágenes de los usuarios y sus nombres
    images.clear()
    clases.clear()

    for filename in os.listdir(OutFolderPathFace):
        if filename.endswith(".png") or filename.endswith(".jpg"):
            img_path = os.path.join(OutFolderPathFace, filename)
            img = cv2.imread(img_path)
            if img is not None:
                images.append(img)
                clases.append(os.path.splitext(filename)[0])  # Nombre del archivo como clase

    # Generar códigos faciales
    FaceCode = Code_Face(images)
    if not FaceCode:
        print("No se encontraron códigos faciales almacenados.")
        return None

    # Cargar la imagen a verificar
    img_to_verify = cv2.imread(image_path)
    if img_to_verify is None:
        print("La imagen no se pudo cargar. Verifica la ruta.")
        return None

    img_rgb = cv2.cvtColor(img_to_verify, cv2.COLOR_BGR2RGB)
    face_locations = fr.face_locations(img_rgb)
    face_encodings = fr.face_encodings(img_rgb, face_locations)

    if not face_encodings:
        print("No se detectaron rostros en la imagen a verificar.")
        return None

    for face_encoding in face_encodings:
        matches = fr.compare_faces(FaceCode, face_encoding)
        face_distances = fr.face_distance(FaceCode, face_encoding)

        if len(face_distances) == 0:
            print("No hay distancias faciales disponibles para comparar.")
            continue

        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            print(f"Usuario reconocido: {clases[best_match_index]}")
            return clases[best_match_index]
        else:
            print("Usuario no reconocido o baja similitud.")
            return None

# Mostrar el perfil del usuario si la imagen coincide
def Profile(UserName):
    global step, conteo, OutFolderPathUser

    conteo = 0
    step = 0

    pantalla_perfil = Toplevel(pantalla)
    pantalla_perfil.title("PERFIL")
    pantalla_perfil.geometry("1280x720")

    # Fondo de pantalla
    imagenB = PhotoImage(file="C:/Users/Usuario/Desktop/RecognitionSystem/SetUp/Back2.png")
    back = Label(pantalla_perfil, image=imagenB, text="Back")
    back.place(x=0, y=0, relwidth=1, relheight=1)

    # Leer la información del usuario
    UserFile = open(f"{OutFolderPathUser}/{UserName}.txt", 'r')
    InfoUser = UserFile.read().split(', ')

    Name = InfoUser[0]
    User = InfoUser[1]
    Pass = InfoUser[2]

    UserFile.close()

    # Verificar si el usuario existe
    if User in clases:
        # Interfaz de bienvenida
        texto1 = Label(pantalla_perfil, text=f"BIENVENIDO {Name}")
        texto1.place(x=580, y=50)

        # Label para la imagen
        lblimage = Label(pantalla_perfil)
        lblimage.place(x=490, y=80)

        # Obtener la imagen del usuario
        PosUserImg = clases.index(User)
        UserImg = images[PosUserImg]
        ImgUser = Image.fromarray(UserImg)

        # Cargar la imagen del usuario desde el archivo
        ImgUser = cv2.imread(f"{OutFolderPathFace}/{User}.png")
        ImgUser = cv2.cvtColor(ImgUser, cv2.COLOR_RGB2BGR)
        ImgUser = Image.fromarray(ImgUser)

        IMG = ImageTk.PhotoImage(image=ImgUser)

        # Mostrar la imagen
        lblimage.configure(image=IMG)
        lblimage.image = IMG

# Ejecutar el código de verificación e iniciar el perfil
if __name__ == "__main__":
    # Ruta de la imagen a verificar
    image_path = "C:/Users/Usuario/Desktop/RecognitionSystem/DataBase/prueba2.jpg"

    # Verificar si la imagen coincide con un usuario almacenado
    result = verify_image(image_path)

    if result:
        print(f"Bienvenido, {result}!")
        Profile(result)
    else:
        print("Acceso denegado.")
        pantalla_perfil = Toplevel(pantalla)
        pantalla_perfil.title("Acceso Denegado")
        pantalla_perfil.geometry("400x200")
        Label(pantalla_perfil, text="Usuario no reconocido.").pack(padx=20, pady=20)

# Iniciar la interfaz
pantalla.mainloop()