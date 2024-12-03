import cv2
import face_recognition as fr
import numpy as np
import mediapipe as mp
import os
from tkinter import *
from PIL import Image, ImageTk
import imutils
import math

def Profile():
    global step, conteo, UserName, OutFolderPathUser

    conteo = 0
    step = 0

    pantalla4 = Toplevel(pantalla)
    pantalla4.title("PERFIL")
    pantalla4.geometry("1280x720")

    back = Label(pantalla4, image=imagenB, text="Back")
    back.place(x=0, y=0, relwidth=1, relheight=1)

    UserFile = open(f"{OutFolderPathUser}/{UserName}.txt", 'r')
    InfoUser = UserFile.read().split(', ')
    
    Name = InfoUser[0]
    User = InfoUser[1]
    Pass = InfoUser[2]

    UserFile.close()

    if User in clases:

        #Interfaz
        texto1 = Label(pantalla4, text = f"BIENVENIDO {Name}")
        
        texto1.place(x=580, y=50)

        #Label
        lblimage = Label(pantalla4)
        lblimage.place(x=490, y=80)

        #Imagen
        PosUserImg = clases.index(User)
        UserImg = images[PosUserImg]

        ImgUser = Image.fromarray(UserImg)

        ImgUser = cv2.imread(f"{OutFolderPathFace}/{User}.png")
        ImgUser = cv2.cvtColor(ImgUser, cv2.COLOR_RGB2BGR)
        ImgUser = Image.fromarray(ImgUser)

        IMG = ImageTk.PhotoImage(image=ImgUser)

        lblimage.configure(image=IMG)
        lblimage.image = IMG

def Code_Face(images):
    listacod = []

    for img in images:
        # Correccion de color
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # Codificamos la imagen
        cod = fr.face_encodings(img)[0]
        # Almacenamos
        listacod.append(cod)

    return listacod

def Close_Window():
    global step, conteo

    conteo = 0
    step = 0
    pantalla2.destroy()

def Close_Window2():
    global step, conteo

    conteo = 0
    step = 0
    pantalla3.destroy()

def Log_Biometric():
    global pantalla, pantalla3, conteo, parpadeo, img_info, step, UserName, prueba
    
    if cap is not None:
        ret, frame = cap.read()

        frameSave = frame.copy()

        #Frame Save
        frameCopy = imutils.resize(frame, width=1280)

        #Resize
        frameFR = cv2.resize(frameCopy, (0, 0), None, 0.25, 0.25)

        #Color
        rgb = cv2.cvtColor(frameFR, cv2.COLOR_BGR2RGB)

        frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        if ret == True:
            res = FaceMesh.process(frameRGB)

            px = []
            py = []
            lista = []

    #Detección de malla facial
            if res.multi_face_landmarks:
                for rostros in res.multi_face_landmarks:
                    mpDraw.draw_landmarks(frame, rostros, FacemeshObject.FACEMESH_TESSELATION, ConfigDraw, ConfigDraw)

                    #Extracción KeyPoint
                    for id, puntos in enumerate(rostros.landmark):

                        # Info IMG
                        al, an, c = frame.shape
                        x, y = int(puntos.x * an), int(puntos.y * al)
                        px.append(x)
                        py.append(y)
                        lista.append([id, x, y])

                        # 468 KeyPoints
                        if len(lista) == 468:
                            # Ojo derecho
                            x1, y1 = lista[145][1:]
                            x2, y2 = lista[159][1:]
                            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
                            longitud1 = math.hypot(x2 - x1, y2 - y1)
                            #print(longitud1)

                            # Ojo Izquierdo
                            x3, y3 = lista[374][1:]
                            x4, y4 = lista[386][1:]
                            cx2, cy2 = (x3 + x4) // 2, (y3 + y4) // 2
                            longitud2 = math.hypot(x4 - x3, y4 - y3)
                            #print(longitud2)

                            # Parietal Derecho
                            x5, y5 = lista[139][1:]
                            # Parietal Izquierdo
                            x6, y6 = lista[368][1:]

                            # Ceja Derecha
                            x7, y7 = lista[70][1:]
                            # Ceja Izquierda
                            x8, y8 = lista[300][1:]

                            # Face Detect
                            faces = detector.process(frameRGB)

                            if faces.detections is not None:    
                                for face in faces.detections:
                                    
                                    # bboxInfo - "id","bbox","score","center"
                                    score = face.score
                                    score = score[0]
                                    bbox = face.location_data.relative_bounding_box

                                    # Threshold
                                    if score > confThreshold:
                                        # Info IMG
                                        alimg, animg, c = frame.shape

                                        # Coordenates
                                        xi, yi, an, al = bbox.xmin, bbox.ymin, bbox.width, bbox.height
                                        xi, yi, an, al = int(xi * animg), int(yi * alimg), int(an * animg), int(al * alimg)

                                        # Width
                                        offsetan = (offsetx / 100) * an
                                        xi = int(xi - int(offsetan/2))
                                        an = int(an + offsetan)
                                        xf = xi + an

                                        # Height
                                        offsetal = (offsety / 100) * al
                                        yi = int(yi - offsetal)
                                        al = int(al + offsetal)
                                        yf = yi + al

                                        # Error < 0
                                        if xi < 0: xi = 0
                                        if yi < 0: yi = 0
                                        if an < 0: an = 0
                                        if al < 0: al = 0

                                        if step == 0:
                                            cv2.rectangle(frame, (xi, yi, an, al), (255, 0, 255), 2)

                                    #STEP 0
                                            alis0, anis0, c = img_step0.shape
                                            frame[50:50 + alis0, 50:50 + anis0] = img_step0

                                    #STEP 1
                                            alis1, anis1, c = img_step1.shape
                                            frame[50:50 + alis1, 1030:1030 + anis1] = img_step1

                                    #STEP 2
                                            alis2, anis2, c = img_step2.shape
                                            frame[270:270 + alis2, 1030:1030 + anis2] = img_step2
                                      

                                    #Requerimiento 1: Ver en dirección a la cámara
                                            if x7 > x5 and x8 < x6:
                                                alch, anch, c = img_check.shape
                                                frame[165:165 + alch, 1105:1105 + anch] = img_check

                                    #Requerimiento 2: Parpadear 5 veces
                                                if longitud1 <= 12 and longitud2 <= 12 and parpadeo == False:  # Umbral reducido de 10 a 12
                                                    conteo = conteo + 1
                                                    parpadeo = True

                                                elif longitud1 > 12 and longitud2 > 12 and parpadeo == True:  # Umbral ajustado para ojos abiertos
                                                    parpadeo = False

                                                alich, anich, c = img_check.shape
                                                frame[165:165 + alich, 1105:1105 + anich] = img_check

                                                cv2.putText(frame, f'Parpadeos: {int(conteo)}', (1070, 375), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)

# Validación de parpadeos
                                                if conteo >= 3:
                                                    alich, anich, c = img_check.shape
                                                    frame[385:385 + alich, 1105:1105 + anich] = img_check

    # Ojos abiertos
                                                    if longitud1 > 14 and longitud2 > 14:
                                                        step = 1
                                                    else:
                                                        conteo = 0

                                        if step == 1:
                                            cv2.rectangle(frame, (xi, yi, an, al), (255, 0, 255), 2)

                                            alli, anli, c = img_liveness_check.shape
                                            frame[50:50 + alli, 50:50 + anli] = img_liveness_check

                                    #Encontrar rostros
                                            faces = fr.face_locations(rgb)
                                            facescod = fr.face_encodings(rgb, faces)

                                            for facecod, faceloc in zip(facescod, faces):
    # Obtener distancias y coincidencias
                                                Match = fr.compare_faces(FaceCode, facecod)
                                                simi = fr.face_distance(FaceCode, facecod)
    
    # Índice de la menor distancia
                                                min_index = np.argmin(simi)
                                                print("clases", clases)
                                                print("similitud", min_index)
                                                print("Match", Match)
    # Verificar si la coincidencia cumple el umbral
                                                if Match[min_index] and simi[min_index] < 0.8: # Ajusta el umbral según tu modelo
                                                    print(f"FaceCode: {len(FaceCode)}, Clases: {len(clases)}")
                                                    UserName = clases[min_index].upper()
                                                    Profile()
                                                else:
                                                    print("Usuario no reconocido o baja similitud.")

                            # close = pantalla3.protocol("WM_DELETE_WINDOW", Close_Window2())

      
    #Conversión
        im = Image.fromarray(frame)
        img = ImageTk.PhotoImage(image=im)

    #Mostrar video
        lblVideo.configure(image=img)
        lblVideo.image = img
        lblVideo.after(10, Log_Biometric)

    else:
        cap.release()

def Sign_Biometric():
    global pantalla, pantalla2, conteo, parpadeo, img_info, step, cap, lblVideo, RegUser

  #Validar videocaptura
    if cap is not None:
        ret, frame = cap.read()

        frameSave = frame.copy()

        frame = imutils.resize(frame, width=1280)

        frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        if ret == True:
            res = FaceMesh.process(frameRGB)

            px = []
            py = []
            lista = []

    #Detección de malla facial
            if res.multi_face_landmarks:
                for rostros in res.multi_face_landmarks:
                    mpDraw.draw_landmarks(frame, rostros, FacemeshObject.FACEMESH_TESSELATION, ConfigDraw, ConfigDraw)

                    #Extracción KeyPoint
                    for id, puntos in enumerate(rostros.landmark):

                        # Info IMG
                        al, an, c = frame.shape
                        x, y = int(puntos.x * an), int(puntos.y * al)
                        px.append(x)
                        py.append(y)
                        lista.append([id, x, y])

                        # 468 KeyPoints
                        if len(lista) == 468:
                            # Ojo derecho
                            x1, y1 = lista[145][1:]
                            x2, y2 = lista[159][1:]
                            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
                            longitud1 = math.hypot(x2 - x1, y2 - y1)
                            #print(longitud1)

                            # Ojo Izquierdo
                            x3, y3 = lista[374][1:]
                            x4, y4 = lista[386][1:]
                            cx2, cy2 = (x3 + x4) // 2, (y3 + y4) // 2
                            longitud2 = math.hypot(x4 - x3, y4 - y3)
                            #print(longitud2)

                            # Parietal Derecho
                            x5, y5 = lista[139][1:]
                            # Parietal Izquierdo
                            x6, y6 = lista[368][1:]

                            # Ceja Derecha
                            x7, y7 = lista[70][1:]
                            # Ceja Izquierda
                            x8, y8 = lista[300][1:]

                            # Face Detect
                            faces = detector.process(frameRGB)

                            if faces.detections is not None:
                                for face in faces.detections:

                                    # bboxInfo - "id","bbox","score","center"
                                    score = face.score
                                    score = score[0]
                                    bbox = face.location_data.relative_bounding_box

                                    # Threshold
                                    if score > confThreshold:
                                        # Info IMG
                                        alimg, animg, c = frame.shape

                                        # Coordenates
                                        xi, yi, an, al = bbox.xmin, bbox.ymin, bbox.width, bbox.height
                                        xi, yi, an, al = int(xi * animg), int(yi * alimg), int(
                                            an * animg), int(al * alimg)

                                        # Width
                                        offsetan = (offsetx / 100) * an
                                        xi = int(xi - int(offsetan/2))
                                        an = int(an + offsetan)
                                        xf = xi + an

                                        # Height
                                        offsetal = (offsety / 100) * al
                                        yi = int(yi - offsetal)
                                        al = int(al + offsetal)
                                        yf = yi + al

                                        # Error < 0
                                        if xi < 0: xi = 0
                                        if yi < 0: yi = 0
                                        if an < 0: an = 0
                                        if al < 0: al = 0

                                    if step == 0:
                                        cv2.rectangle(frame, (xi, yi, an, al), (255, 0, 255), 2)

                                    #STEP 0
                                        als0, ans0, c = img_step0.shape
                                        frame[50:50 + als0, 50:50 + ans0] = img_step0

                                    #STEP 1
                                        als1, ans1, c = img_step1.shape
                                        frame[50:50 + als1, 1030:1030 + ans1] = img_step1

                                    #STEP 2
                                        als2, ans2, c = img_step2.shape
                                        frame[270:270 + als2, 1030:1030 + ans2] = img_step2
                                      

                                    #Requerimiento 1: Ver en dirección a la cámara
                                        if x7 > x5 and x8 < x6:
                                            alch, anch, c = img_check.shape
                                            frame[165:165 + alch, 1105:1105 + anch] = img_check

                                    #Requerimiento 2: Parpadear 5 veces
                                        if longitud1 <= 10 and longitud2 <= 10 and parpadeo == False:
                                            conteo = conteo  +1
                                            parpadeo = True
                                        
                                        elif longitud1 > 10 and longitud2 > 10 and parpadeo == True:
                                           parpadeo = False

                                        cv2.putText(frame, f'Parpadeos: {int(conteo)}', (1070, 375), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)

                                        #Validación de parpadeos
                                        if conteo >= 3:
                                            alch, anch, c = img_check.shape
                                            frame[385:385 + alch, 1105:1105 + anch] = img_check

                                            #Ojos abiertos
                                            if longitud1 > 14 and longitud2 > 14:
                                               cut = frameSave[yi:yf, xi:xf]

                                               cv2.imwrite(f"{OutFolderPathFace}/{RegUser}.png", cut)

                                               step = 1
                                        
                                    else:
                                       conteo = 0

                                if step == 1:
                                    cv2.rectangle(frame, (xi, yi, an, al), (255, 0, 255), 2)

                                    alli, anli, c = img_liveness_check.shape
                                    frame[50:50 + alli, 50:50 + anli] = img_liveness_check

                            # close = pantalla2.protocol("WM_DELETE_WINDOW", Close_Window())
      
    #Conversión
        im = Image.fromarray(frame)
        img = ImageTk.PhotoImage(image=im)

    #Mostrar video
        lblVideo.configure(image=img)
        lblVideo.image = img
        lblVideo.after(10, Sign_Biometric)

    else:
        cap.release()

def Log():
    global LogUser, LogPass, OutFolderPath, cap, lblVideo, pantalla3, FaceCode, clases, images

    LogUser, LogPass = InputUserLog.get(), InputPasswordLog.get()

    images = []
    clases = []
    lista = os.listdir(OutFolderPathFace)

    for lis in lista:
        #Leer imagen
        imgdb = cv2.imread(f"{OutFolderPathFace}/{lis}")
        #Guardar imagen
        images.append(imgdb)

        clases.append(os.path.splitext(lis)[0])

    FaceCode = Code_Face(images)

    pantalla3 = Toplevel(pantalla)
    pantalla3.title("BIOMETRIC SIGN UP")
    pantalla3.geometry("1280x720")

    lblVideo = Label(pantalla3)
    lblVideo.place(x=0, y=0)

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap.set(3, 1280)
    cap.set(4, 720)
    Log_Biometric()

def Sign():
  global RegName, RegUser, RegPassword, InputNameReg, InputUserReg, InputPasswordReg, cap, lblVideo, pantalla2
  # Extracción de datos: Name - User - Password
  RegName, RegUser, RegPassword = InputNameReg.get(), InputUserReg.get(), InputPasswordReg.get()

  #Formulario incompleto
  if len(RegName) == 0 or len(RegUser) == 0 or len(RegPassword) == 0:
    print("Formulario incompleto")
  else:
    #Validar usuarios
    UserList = os.listdir(PathUserCheck) #Lista de usuarios

    UserName = []

    for list in UserList:
      User = list
      User = User.split(".")
      print("Nombre de usuario", User)
      UserName.append(User[0])

    if RegUser in UserName:
      print("Usuario ya registrado")

    else:
      info.append(RegName)
      info.append(RegUser)
      info.append(RegPassword)

      #Exportar información
      f = open(f"{OutFolderPathUser}/{RegUser}.txt", "w")

      f.write(RegName + ', ' + RegUser + ', ' + RegPassword)
      f.close()

      InputNameReg.delete(0, END)
      InputUserReg.delete(0, END)
      InputPasswordReg.delete(0, END)

      pantalla2 = Toplevel(pantalla)
      pantalla2.title("LOGIN BIOMÉTRICO")
      pantalla2.geometry("1280x720")

      # Video
      lblVideo = Label(pantalla2)
      lblVideo.place(x=0, y=0)

      cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
      cap.set(3, 1280)
      cap.set(4, 720)
      Sign_Biometric()

#Rutas
OutFolderPathUser = 'C:/Users/Usuario/Desktop/RecognitionSystem/DataBase/Users'
PathUserCheck = 'C:/Users/Usuario/Desktop/RecognitionSystem/DataBase/Users/'
OutFolderPathFace = 'C:/Users/Usuario/Desktop/RecognitionSystem/DataBase/Faces'

#Lectura de imágenes
img_info = cv2.imread("C:/Users/Usuario/Desktop/RecognitionSystem/SetUp/Info.png")
img_check = cv2.imread("C:/Users/Usuario/Desktop/RecognitionSystem/SetUp/check.png")
img_step0 = cv2.imread("C:/Users/Usuario/Desktop/RecognitionSystem/SetUp/Step0.png")
img_step1 = cv2.imread("C:/Users/Usuario/Desktop/RecognitionSystem/SetUp/Step1.png")
img_step2 = cv2.imread("C:/Users/Usuario/Desktop/RecognitionSystem/SetUp/Step2.png")
img_liveness_check = cv2.imread("C:/Users/Usuario/Desktop/RecognitionSystem/SetUp/LivenessCheck.png")

#Variables
parpadeo = False
conteo = 0 
step = 0
muestra = 0

offsety = 40
offsetx = 20

confThreshold = 0.5

mpDraw = mp.solutions.drawing_utils
ConfigDraw = mpDraw.DrawingSpec(thickness=1, circle_radius=1)

FacemeshObject = mp.solutions.face_mesh
FaceMesh = FacemeshObject.FaceMesh(max_num_faces = 1)

#Detección de rostros
FaceObject = mp.solutions.face_detection
detector = FaceObject.FaceDetection(min_detection_confidence=0.5, model_selection=1)

#Lista de información
info = []

#Ventana principal
pantalla = Tk()
pantalla.title("FACE RECOGNITION")
pantalla.geometry("1280x720")

#Fondo
imagenF = PhotoImage(file='C:/Users/Usuario/Desktop/RecognitionSystem/SetUp/Inicio.png')
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

#Botones
#Registro
imagenBR = PhotoImage(file='C:/Users/Usuario/Desktop/RecognitionSystem/SetUp/BtLogin.png')
BtReg = Button(pantalla, text="Registro", image=imagenBR,  height="40", width="200", command=Sign)
BtReg.place(x=300, y=580)

imagenB = PhotoImage(file="C:/Users/Usuario/Desktop/RecognitionSystem/SetUp/Back2.png")

#Inicio
imagenBI = PhotoImage(file='C:/Users/Usuario/Desktop/RecognitionSystem/SetUp/BtSign.png')
BtInicio = Button(pantalla, text="Registro", image=imagenBI,  height="40", width="200", command=Log)
BtInicio.place(x=900, y=580)

pantalla.mainloop()