

import cv2
import os
import argparse
from time import time as timeStamp

class point():
    def __init__(self) -> None:
        self.x = 0
        self.y = 0

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--vertical", 
                            help="longitud vertical del recorte",
                            type=int, 
                            default=150)
    parser.add_argument("--horizontal", 
                            help="longitud horizontal del recorte",
                            type=int, 
                            default=150)
    parser.add_argument("--color", 
                            help="Color del rectangulo (en GBR)",
                            type=tuple, 
                            default=(0,0,255) )

    args = parser.parse_args()
    return args
    
def BuenaEntrada(img_path):
    image = cv2.imread(img_path)
    if image is None:
        return False
    return True

def CalcularEsquinas(x,y,vertical,horizontal): 
    h, v = horizontal//2, vertical//2
    
    return ( (x-h , y-v ) ,     # <- Esquina Superior izquierda
             (x+h , y+v )  )    # <- Esquina Inferior derecha

def procesarImagen(file_name,img_path,of_path,args):
    
    vertical,horizontal = args.vertical , args.horizontal
    color = args.color
    image = cv2.imread(img_path)   
    cv2.imshow(file_name,image)
    

    copiar_img = image.copy
    mostrar_imagen = cv2.imshow
    Boton_izquierdo = cv2.EVENT_LBUTTONDOWN
    Boton_derecho = cv2.EVENT_RBUTTONDOWN
    guardar_img = cv2.imwrite
    path_OK =of_path + "/OK/"
    path_NG = of_path + "/NG/"
    path_NL = of_path + "/Not_Label/"
    
    last_position = point()
    def cv_event_handler(event, x, y, flags,userdata:point):

        if event == cv2.EVENT_MOUSEMOVE: 
            userdata.x = x 
            userdata.y = y 

    cv2.setMouseCallback(file_name,cv_event_handler,last_position)   
    
    centinela = True      
    modoDeSuma = 1
    opcion=0
    esperar = cv2.waitKey
    while centinela:
        
        imgCopy = copiar_img()
        ESI , EID = CalcularEsquinas(last_position.x,last_position.y,vertical,horizontal)
        cv2.rectangle(imgCopy,  
            ESI,                #Esquina superior izquierda
            EID,                #Esquina inferior derecha
            color,              #Color de linea
            1,                  #Grosor de linea
            cv2.LINE_AA,        #Tipo de linea
            )               
        mostrar_imagen(file_name, imgCopy)

        k = esperar(1) 
        if k ==27:
            opcion = 0
            centinela=False
        
        k = k & 0xFF
        if k == ord('w'):
            vertical+= 10
        elif k == ord('s'):
            vertical-= 10 
        elif k == ord('a'):
            horizontal-= 10
        elif k == ord('d'):
            horizontal+= 10 
        elif k == ord('h'):
            horizontal+= modoDeSuma        
        elif k == ord('v'):
            vertical+= modoDeSuma 
        elif k == ord('i'):
            vertical+= modoDeSuma *15 
        elif k == ord('j'):
            horizontal+= modoDeSuma*15
        elif k == ord('+'):
            modoDeSuma = 1
        elif k == ord('-'):
            modoDeSuma=-1
        elif k == ord('q'):
            opcion = -1
            centinela=False
        elif k == ord('e'):
            opcion = 1
            centinela=False
        elif k == ord('1'):
            status = guardar_img("./1/" + str(timeStamp()) + ".jpg",image)
            print(status)
            print("1")
        elif k == ord('2'):
            status = guardar_img("./2/" + str(timeStamp()) + ".jpg",image)
            print(status)
            print("2")
        elif k == ord('3'):
            status = guardar_img("./3/" + str(timeStamp()) + ".jpg",image)
            print(status)
            print("3")
        elif k == ord('4'):
            #ESI , EID = CalcularEsquinas(last_position.x,last_position.y,vertical,horizontal)
            #recorte = image[ ESI[1]:EID[1],ESI[0]:EID[0] ]
            status = guardar_img(path_OK + str(timeStamp()) + ".jpg",image)
            print(status)
            print("OK")
        
                    
        
    cv2.destroyAllWindows()
    return opcion

def main():

    args = get_args()
    if_path = "./image_input_folder"
    of_path = "."
    
    
    files_names = os.listdir(if_path)   
    cantidad_fotos = len(files_names) 

    index=0
    opcion = 1
    while(opcion != 0):
        file_name = files_names[index]
        img_path = if_path + "/" + file_name
        if BuenaEntrada(img_path):
            opcion = procesarImagen(file_name,img_path,of_path,args)
        index += opcion
        index = index%cantidad_fotos
                                     

if __name__ == "__main__":
    main()
