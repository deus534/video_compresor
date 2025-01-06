from PIL import Image
import numpy as np
import math
import sys
import os

def archivo_a_imagenes(ruta_archivo, ancho, alto, salida_base):
    with open(ruta_archivo, 'rb') as archivo:
        datos = archivo.read()

    # Calcular el número de píxeles por imagen
    total_pixeles_por_imagen = ancho * alto
    total_imagenes = math.ceil(len(datos) / total_pixeles_por_imagen)

    for i in range(total_imagenes):
        # Extraer un bloque de datos para esta imagen
        inicio = i * total_pixeles_por_imagen
        fin = inicio + total_pixeles_por_imagen
        bloque = datos[inicio:fin]

        # Rellenar con ceros si no completa una imagen
        if len(bloque) < total_pixeles_por_imagen:
            bloque += bytes(total_pixeles_por_imagen - len(bloque))

        # Convertir el bloque a matriz e imagen
        matriz = np.array(list(bloque), dtype=np.uint8).reshape((alto, ancho))
        imagen = Image.fromarray(matriz, 'L')

        # Guardar la imagen
        ruta_guardado = 'Images'
        os.mkdir(ruta_guardado)
        nombre_imagen = f"{ruta_guardado}/{salida_base}_{i+1}.png"
        imagen.save(nombre_imagen)
        print(f"Imagen {i+1} guardada como {nombre_imagen}")

if __name__=='__main__':
    if len(sys.argv)>1:
        archivo_a_imagenes(sys.argv[1], 1360, 768, 'salida')
        print(f'Nombre del projecto: {sys.argv[0]}')
        print(f'este es la entrada: {sys.argv[1]}')
    else:
        print('Introduce el nombre del archivo')