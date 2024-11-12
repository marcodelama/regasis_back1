import cv2
import face_recognition as fr
import numpy as np
import mediapipe as mp
import os
from tkinter import *
from PIL import Image, ImageTk
import imutils
import math

#Rutas
OutFolderPathUser = 'C:/Users/mbarr/OneDrive/Escritorio/SistemaReconocimiento/DataBase/Users'
PathUserCheck = 'C:/Users/mbarr/OneDrive/Escritorio/SistemaReconocimiento/DataBase/Users/'
OutlFolderPathFace = 'C:/Users/mbarr/OneDrive/Escritorio/SistemaReconocimiento/DataBase/Faces'

#Lista de información
info = []

#Ventana principal
pantalla = Tk()
pantalla.title("FACE RECOGNITION")
pantalla.geometry("1280x720")

#Fondo
imagenF = PhotoImage(file='C:/Users/mbarr/OneDrive/Escritorio/SistemaReconocimiento/SetUp/Inicio.png')
background = Label(image = imagenF, text="Inicio")
background.place(x=0, y=0, relheight=1, relwidth=1)

#Entradas de texto
InputNameReg = Entry(pantalla)
InputNameReg.place(x=110, y=320)

InputUserReg = Entry(pantalla)
InputUserReg.place(x=110, y=430)

InputPasswordReg = Entry(pantalla)
InputPasswordReg.place(x=110, y=540)

#Inicio de sesión
InputUserLog = Entry(pantalla)
InputUserLog.place(x=750, y=380)

InputPasswordLog = Entry(pantalla)
InputPasswordLog.place(x=750, y=500)

pantalla.mainloop()