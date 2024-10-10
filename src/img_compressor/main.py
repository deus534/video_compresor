import cv2
import numpy as np
import os
import sys

def factores_primos(n):
    factores = []
    
    # Comienza con el primer número primo
    divisor = 2
    
    # Mientras el número sea mayor que 1
    while n > 1:
        # Si el divisor divide n sin residuo
        while n % divisor == 0:
            factores.append(divisor)  # Agrega el divisor a la lista de factores
            n //= divisor  # Divide n por el divisor
        
        # Incrementa el divisor
        divisor += 1
    
    return factores
def show_img( path ):
    img = cv2.imread( path )
    cv2.imshow("img: "+path, img )

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
   
def create_imgs(name_arch, path_save, width, heigth ):
    img = np.zeros( (width, heigth), dtype="uint8" )
    TAM_BLOQUE = 1
    i = 0
    j = 0
    #imprimir_encabezado....
    #START_pdf:  -> de esta manera sera mi encabezado
    #END_pdf:    -> de esta manera sera mi fin..
    data_a_escribir = ('S', 'T', 'A', 'R', 'T', '_', 'p','d','f')
    start_ascii = [ord(c) for c in data_a_escribir]
    img[0, :len(start_ascii)] = start_ascii
    
    nro_img = 0;
    name_img = 'image_'; 
    with open(name_arch, 'rb') as archivo:
        while True:
            byte = archivo.read(TAM_BLOQUE)
            if not byte:               
                break
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
        data_a_escribir = ('E', 'N', 'D', '_','p','d','f')
        end_ascii = [ord(c) for c in data_a_escribir]
        for k in range(len(end_ascii)):
            if j==heigth:
                j=0
                i+=1
            img[i][j+k] = end_ascii[k]
        name = path_save + name_img + str(nro_img) + '.png'
        cv2.imwrite( name, img)

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
def recrear_archivo( imgs ):
    for img in imgs:
        alto, ancho = img.shape
        print(f'alto: {alto}, ancho: {ancho}')

        start = False
        end = True
        start_code = ""
        end_code = ""
        name_arch = "reconstruido.pdf"
        n = 0

        with open("reconstruido.pdf", "wb") as archivo:
            for y in range(ancho):
                for x in range(alto):
                    pixel = img[x,y]
                    end_code += chr(pixel)
                    start_code += chr(pixel)
                    if( start_code=="START_pdf" ):
                        print(start_code)
                    if( end_code=="END_pdf" ):
                        print(end_code)
                    if( start_code==9 ):
                        start_code=""
                    if( len(end_code)==7 ):
                        end_code = ""                        
                        end = False
                    if n>=9 and end_code!="END_pdf" :
                            archivo.write(pixel)
    #                        archivo.write(struct.pack('B', pixel))
                        #escribo en el archivo
                    n+=1;
                    #else:
                    #    start_code+=chr(pixel)
                    #    print( start_code )
                    #    if start_code=="START_pdf":
                    #        start = True


        

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
