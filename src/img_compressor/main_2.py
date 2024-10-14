import cv2
import numpy as np
import os
import sys
import time

#1) de esta manera escribo en un archivo un byte que esta en tipo uint8
#2) Para leer el archivo, simplemento lo leo como un char.....
def write_arch( nam_arch ):
	with open(nam_arch, "w") as archivo:
		#Transformo de char a uint8_t
		#----
		char = 'C'
		data_u = int.from_bytes(char.encode(), 'big')
		#----
		#Transformo de uint8_t a char
		#...
		d_ui = chr(data_u)
		#...
		#escribo en el archivo los chars.....
		archivo.write(d_ui)



if __name__ == '__main__':

    if len(sys.argv) < 2:
    	print( 'Introduce el nombre del path' )
    	sys.exit(1)

    write_arch(sys.argv[1])


