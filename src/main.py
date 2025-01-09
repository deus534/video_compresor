from PIL import Image
import numpy as np
import math as mt
import os
import cv2

#ctes globalsImages/
path_images = '/home/brian/Documentos/repositorios/video_compresor/images'
path_files = '/home/brian/Documentos/repositorios/video_compresor/files/'

def save_report( file_path, number_images ):
    file_name = os.path.splitext(os.path.basename(file_path))[0]
    size_file = os.path.getsize(file_path)
    extension = os.path.splitext(file_path)[1]
    path_save = path_images + file_name + '/'
    os.makedirs(path_save, exist_ok=True)
    os.makedirs(path_save+'images/', exist_ok=True)

    with open(f'{path_save}info.txt', 'w') as f:
        f.write(f'{file_name}\n{file_name}_encripted\n{size_file}\n{number_images}\n{extension}')
    #1) name of file
    #2) name of file encripted
    #3) size of file
    #4) number of images
    #5) extension
    return path_save+'images/'

def create_images( file_name, width=1360, height=768 ):
    chunk_size = width * height
    total_pixels = width * height

    with open(file_name, 'rb') as f:
        data = f.read()
    total_images = mt.ceil(len(data) / total_pixels)
    path_save = save_report(file_name, total_images)

    for i in range(total_images):
        start = i * total_pixels
        end = start + total_pixels
        block_pixels = data[start:end]
        #rellena con ceros
        if len(block_pixels) < total_pixels:
            block_pixels += bytes(total_pixels - len(block_pixels))

        #guardado de la imagen
        data_image = np.array(list(block_pixels), dtype=np.uint8).reshape((height, width))
        new_image = Image.fromarray(data_image, mode='L')
        new_image.save(f'{path_save}image_{i+1}.png')

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

def create_video_from_images(image_folder, output_video, frame_rate=30):
    # Obtener la lista de imágenes en la carpeta
    images = [img for img in os.listdir(image_folder) if img.endswith((".png", ".jpg", ".jpeg"))]
    images.sort()  # Asegurarse de que estén ordenadas numéricamente o alfabéticamente

    # Leer la primera imagen para obtener el tamaño del video
    first_image_path = os.path.join(image_folder, images[0])
    frame = cv2.imread(first_image_path)
    height, width, layers = frame.shape

    # Configurar el VideoWriter
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # Codec para archivo MP4
    video = cv2.VideoWriter(output_video, fourcc, frame_rate, (width, height))

    # Loop a través de todas las imágenes y agregar cada una al video
    for image in images:
        image_path = os.path.join(image_folder, image)
        frame = cv2.imread(image_path)

        # Asegúrate de que todas las imágenes tienen la misma resolución
        if frame.shape[:2] != (height, width):
            frame = cv2.resize(frame, (width, height))

        video.write(frame)  # Escribir el frame en el video

    # Liberar el VideoWriter
    video.release()
    print(f"Video creado correctamente: {output_video}")

if __name__ == '__main__':
    #file_path = input('enter the file name: ')
    #file_name = os.path.splitext(os.path.basename(file_path))[0]
    #tarda en crear las imagenes....
    #create_images(path_files+file_path)
    #rapido para reconstruirlo
    #create_file(path_images+ file_name +'/info.txt')

    create_video_from_images('Images/video/images/', 'output_video.mkv', frame_rate=30)
    print('end')