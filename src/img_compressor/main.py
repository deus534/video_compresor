import cv2
import numpy as np
import os
import sys
import time

def factores_primos(n):
    factores = []
    divisor = 2
    while n > 1:
        while n % divisor == 0:
            factores.append(divisor)
            n //= divisor
        divisor += 1
    return factores

#---x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x---#
#---x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x---#
#---x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x---#

def show_img( path ):
    img = cv2.imread( path )
    cv2.imshow("img: "+path, img )

#---x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x---#
#---x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x---#
#---x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x---#

def read_arch_in_img( path, width, heigth ):
    img = np.zeros( (width, heigth), dtype="uint8" )
    TAM_BLOQUE = 1
    i = 0
    j = 0
    msj = 'termino'
    nro_img = 0;
    
    with open(path, 'rb') as archivo:
        while True:
            byte = archivo.read(TAM_BLOQUE)
            if not byte:               
                break
            data = int.from_bytes(byte,'big')
            img[i][j] = data
            j+=1
            if i==(width-1):
                msj = 'falto memoria'
                break
            if j==heigth:
                j=0
                i+=1
            #char = byte.decode('utf-8', errors='replace')
            #print(char,end='')
    return [img, msj]

#---x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x---#
#---x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x---#
#---x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x---#

def new_img( img, data, width, heigth ):
    for i in range( width ):
        for j in range( heigth ):
            img[i,j] = data[i,j]


#---x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x---#
#---x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x---#
#---x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x---#
   
def create_imgs(name_arch, path_save, width, heigth ):
    img = np.zeros( (width, heigth), dtype="uint8" )
    extension = name_arch.split('.')[-1] if '.' in name_arch else ''
    TAM_BLOQUE = 1
    i = 0
    j = 0
    encabezado_inicio = list(extension + '_' + "start" + "_")
    encabezado_fin = list("_end_")
    for x in range( len(encabezado_inicio) ):
        img[0][x] = int.from_bytes(encabezado_inicio.pop(0).encode(),'big')
    nro_img = 0;
    name_img = 'image_'; 
    flag = True

    with open(name_arch, 'rb') as archivo:
        while flag:
            byte = archivo.read(TAM_BLOQUE)
            if not byte:
                if not data:
                    break
                data = encabezado_fin.pop(0)
                data = data.encode()
            data = int.from_bytes(byte,'big')
            img[i][j] = data
            j+=1
            if i==(width-1):
                name = path_save + name_img + str(nro_img) + '.png'
                nro_img+=1
                cv2.imwrite( name, img);
                i = 0;
                j = 0;
            if j==heigth:
                j=0
                i+=1
        name = path_save + name_img + str(nro_img) + '.png'
        cv2.imwrite( name, img)

#---x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x---#
#---x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x---#
#---x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x---#

def read_imgs( path ):
    ret_imgs = []
    for name_arch in os.listdir( path ):
        if name_arch.endswith('.png'):
           path_img = os.path.join( path, name_arch )
           img = cv2.imread( path_img,cv2.IMREAD_GRAYSCALE )
           if img is not None:
               ret_imgs.append(img)
               print( 'Imagen cargada ' )
           else:
               print('error')
    return ret_imgs
#recivo la o las imagenes a las que lleve

#---x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x---#
#---x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x---#
#---x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x---#

def recrear_archivo( imgs ):

    with open("reconstruido.pdf", "w") as archivo:
        for img in imgs:
            alto, ancho = img.shape
            print(f'alto: {alto}, ancho: {ancho}')

            enc_ini = ""
            enc_fin = ""
            extension = ""
            #encabezado_inicio = list(extension + '_' + "start" + "_")
            #encabezado_fin = list("_end_")
            name_arch = "reconstruido."
            for y in range(ancho):
                for x in range(alto):
                    pixel_data = chr( img[x,y] ).encode('utf-8')
                    print( pixel_data, end="")
                    time.sleep(0.001) 
                    if enc_ini.endswith("_start_"):
                        #extension = enc_ini[:3]
                        archivo.write(pixel_data)
                    #else:
                        #enc_ini += pixel_data
                    #if enc_fin.endswith("_end_"):
                    #    break
                    #else:
                    #    if len(enc_fin)==5:
                    #        enc_fin = ""
                        #enc_fin+=pixel_data
        name_arch += extension
        print()
        print(f'archivo guardado como {name_arch}')
#---x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x---#
#---x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x---#
#---x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x---#

        

#path_imgs = "../Images/"

#leer imagenes
#show_img( path_imgs+"Img_1.png" ) 


#crear nuevas imagenes
#1) con 3 canales es decir que es de tipo RGB
#new_img = np.ones((400,400,3), dtype="uint8")*255  #fondo 255=blanco, 1=negro
#cv2.circle( new_img, (200,200), 50, (255,0,0), 2)  #crea un circulo
#cv2.line( new_img, (0,0), (400,400), (0,0,255), 1 )
#cv2.imshow("nueva_imagen", new_img)


#.....2) Con 1 canal en escala de grises...
#width = 720
#heigth = 1280
#arch = 'prueba.pdf'
#img = np.ones( (width, heigth), dtype="uint8" )*255
#[img, msj] = read_arch_in_img( arch, width, heigth )
#cv2.imshow("Imagen escala grises", img)
#cv2.imwrite("imgs/prueba.png", img)
#size = os.path.getsize(arch)


#print(f'tamanio necesario: {size}')
#print(f'primos: {factores_primos(size)}')
#print(f'tamnio utilizado: {width*heigth}')
#print(msj)
#mostrar la imagen, hasta que la cierre...
#cv2.waitKey(0)
#cv2.destroyAllWindows()

#-----------------------3) prueba_creador de imagenes----------------

def compresor():
    #leo archivo y lo transformo en imagenes
    if len(sys.argv) < 2:
        print( 'Introducec el nombre del archivo' )
        sys.exit(1)
    width = 720
    heigth = 1280
    path_save = 'imgs/'
    name_arch = sys.argv[1]
    create_imgs( name_arch, path_save, width, heigth )
def decodifer():
    #leo imagenes y los pongo en un vector
    if len(sys.argv) < 2:
        print( 'Introduce el nombre del path' )
        sys.exit(1)
    
    imagenes = read_imgs( sys.argv[1] )
    recrear_archivo(imagenes)
#recibo el nombre del archivo a tratar...
if __name__ == '__main__':

#    compresor()
    decodifer()
