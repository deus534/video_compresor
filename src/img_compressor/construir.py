import numpy as np
from PIL import Image
import sys

# Función para leer el archivo como bytes
def leer_archivo(archivo):
    with open(archivo, 'rb') as f:
        data = f.read()
    return data

# Función para convertir los datos a una imagen de tamaño fijo
def datos_a_imagen(data, ancho=1280, alto=720):
    # Cada imagen tiene ancho * alto píxeles
    max_bytes = ancho * alto

    # Rellenar con ceros si el bloque de datos es menor que el tamaño máximo
    datos_numericos = list(data)
    datos_numericos += [0] * (max_bytes - len(datos_numericos))

    # Crear una matriz NumPy de tamaño (alto, ancho)
    matriz = np.array(datos_numericos, dtype=np.uint8).reshape((alto, ancho))

    # Convertir la matriz en una imagen en escala de grises
    imagen = Image.fromarray(matriz, mode='L')  # Escala de grises
    return imagen

# Función para dividir los datos en bloques del tamaño adecuado para las imágenes
def guardar_en_imagenes(data, ancho=1280, alto=720):
    max_bytes = ancho * alto  # Tamaño máximo de datos por imagen
    total_bytes = len(data)

    # Calcular cuántas imágenes se necesitan
    num_imagenes = (total_bytes + max_bytes - 1) // max_bytes  # Redondea hacia arriba

    # Dividir los datos en bloques y guardar cada bloque en una imagen
    for i in range(num_imagenes):
        start = i * max_bytes
        end = min(start + max_bytes, total_bytes)
        bloque = data[start:end]
        
        imagen = datos_a_imagen(bloque, ancho, alto)
        imagen.save(f'imagenes/salida_{i+1}.png')  # Guardar cada imagen con un nombre secuencial
        print(f"Guardando imagen {i+1} con datos desde byte {start} hasta {end}")

if __name__ == '__main__':
	if len(sys.argv) < 2:
		print('Introduce el archivo')
		sys.exit(1)



	# Ruta del archivo a convertir en imágenes
	ruta_archivo = sys.argv[1]

	# Leer los datos del archivo
	data = leer_archivo(ruta_archivo)

	# Guardar los datos en múltiples imágenes de 1280x720 píxeles
	guardar_en_imagenes(data)
