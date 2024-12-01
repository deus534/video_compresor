from PIL import Image
import numpy as np
import sys

# Función para leer una imagen y extraer los datos
def imagen_a_datos(imagen_path):
    imagen = Image.open(imagen_path)
    matriz = np.array(imagen)
    datos_numericos = matriz.flatten().tolist()
    
    # Eliminar los ceros de relleno al final
    return bytes(datos_numericos)

# Función para reconstruir el archivo desde múltiples imágenes
def reconstruir_archivo(num_imagenes, archivo_salida):
    datos_totales = bytearray()

    # Leer cada imagen secuencialmente y agregar los datos
    for i in range(num_imagenes):
        imagen_path = f'imagenes/salida_{i+1}.png'
        datos = imagen_a_datos(imagen_path)
        datos_totales.extend(datos)

    # Guardar los datos de vuelta en un archivo binario
    with open(archivo_salida, 'wb') as f:
        f.write(datos_totales)

if __name__ == '__main__':
	if len(sys.argv) < 2:
		print('Introduce el nro de imagenes ')
		sys.exit(1)
	nro_imgs = int(sys.argv[1])
	# Reconstruir el archivo desde las imágenes
	reconstruir_archivo(num_imagenes=nro_imgs, archivo_salida='archivo_reconstruido.pdf')
