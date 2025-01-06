from PIL import Image
import numpy as np
import math as mt
import os

#ctes globales
path_images = 'Images/'
path_files = 'files/'
WIDTH = 1360
HEIGHT = 768

def save_report( file_path ):
    total_images = mt.ceil(os.path.getsize(file_path) / (WIDTH * HEIGHT))
    file_name = os.path.splitext(os.path.basename(file_path))[0]
    size_file = os.path.getsize(file_path)
    extension = os.path.splitext(file_path)[1]
    path_save = path_images + file_name + '/'
    os.makedirs(path_save, exist_ok=True)
    os.makedirs(path_save+'images/', exist_ok=True)

    with open(f'{path_save}info.txt', 'w') as f:
        f.write(f'{file_name}\n{file_name}_encripted\n{size_file}\n{total_images}\n{extension}')
    #1) name of file
    #2) name of file encripted
    #3) size of file
    #4) number of images
    #5) extension
    return path_save+'images/', total_images

def create_images( file_name, width=1360, height=768 ):
    chunk_size = width * height
    total_pixels = width * height
    path_save, total_images = save_report(file_name)

    with open(file_name, 'rb') as f:
        while chunk:= f.read(chunk_size):
            for i in range(total_images):
                block_pixels = chunk
                # rellena con ceros
                if len(block_pixels) < total_pixels:
                    block_pixels += bytes(total_pixels - len(block_pixels))
                # guardado de la imagen
                data_image = np.array(list(block_pixels), dtype=np.uint8).reshape((height, width))
                new_image = Image.fromarray(data_image, mode='L')
                new_image.save(f'{path_save}image_{i + 1}.png')
            #proceso de datos.
        data = f.read()


def create_file(file_report):
    with open(file_report, 'r') as f:
        data = f.read().split('\n')
    file_name = data[0]
    file_encripted = data[1]
    size_file = int(data[2])
    number_images = data[3]
    extension = data[4]
    total_written = 0

    with open(path_files+file_name+'_rearmed'+extension, 'wb') as f:
        for i in range(int(number_images)):
            with Image.open(path_images+file_name+'/images/'+f'image_{i+1}.png') as img:
                pixel_data = np.array(img)
                pixel_bytes = pixel_data.flatten().tobytes()
                remaining_size = size_file - total_written
                if remaining_size > 0:
                    # Escribir solo la cantidad necesaria
                    f.write(pixel_bytes[:remaining_size])
                    total_written += len(pixel_bytes[:remaining_size])
                    # Detenernos si alcanzamos el tamaño del archivo original
                    if total_written >= size_file:
                        break

if __name__ == '__main__':
    file_path = input('enter the file name: ')
    file_name = os.path.splitext(os.path.basename(file_path))[0]
    create_images(path_files+file_path)
    #create_file(path_images+ file_name +'/info.txt')
    print('end')
