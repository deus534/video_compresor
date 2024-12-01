from PIL import Image
import numpy as np
import os

def imagenes_a_archivo(ruta_imagenes, salida_archivo):
    archivos_imagenes = sorted(
        [os.path.join(ruta_imagenes, img) for img in os.listdir(ruta_imagenes) if img.endswith('.png')]
    )
    
    datos_recuperados = bytearray()

    for imagen in archivos_imagenes:
        with Image.open(imagen) as img:
            matriz = np.array(img)
            datos_recuperados.extend(matriz.flatten())

    # Guardar los datos recuperados como un archivo binario
    with open(salida_archivo, 'wb') as archivo:
        archivo.write(datos_recuperados)
    
    print(f"Archivo recuperado guardado como {salida_archivo}")

# Ejemplo de uso
# Carpeta con las imágenes generadas anteriormente
imagenes_a_archivo('./', 'archivo_recuperado.pdf')

