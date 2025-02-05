from PIL import Image
import numpy as np
import math as mt
import os
import cv2
#constants globals
path_output = '/home/brian/Documentos/repositorios/video_compresor/output/'
path_files = '/home/brian/Documentos/repositorios/video_compresor/files/'
WIDTH = 1280
HEIGHT = 720
def save_report( file_path, number_images ):
    file_name = os.path.splitext(os.path.basename(file_path))[0]
    size_file = os.path.getsize(file_path)
    extension = os.path.splitext(file_path)[1]
    path_save = path_output + file_name + '/'
    os.makedirs(path_save, exist_ok=True)
    os.makedirs(path_save+'images/', exist_ok=True)
    print(path_save)
    with open(f'{path_save}info.txt', 'w') as f:
        f.write(f'{file_name}\n{file_name}_encripted\n{size_file}\n{number_images}\n{extension}')
    #1) name of file
    #2) name of file encripted
    #3) size of file
    #4) number of images
    #5) extension
    return path_save+'images/'

def create_images( file_path, width=WIDTH, height=HEIGHT ):
    chunk_size = width * height
    total_pixels = width * height

    with open(file_path, 'rb') as f:
        data = f.read()
    total_images = mt.ceil(len(data) / total_pixels)
    path_save = save_report(file_path, total_images)

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
            with Image.open(path_output+file_name+'/images/'+f'image_{i+1}.png') as img:
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
    video = cv2.VideoWriter(output_video, fourcc, frame_rate, (width, height), isColor=False)

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

def save_info(file_path, number_images):
    name_file = os.path.splitext(os.path.basename(file_path))[0]
    size_file = os.path.getsize(file_path)
    extension = os.path.splitext(file_path)[1]
    path_save = path_output + name_file + '/'
    os.makedirs(path_save, exist_ok=True)
    with open(f'{path_save}info.txt', 'w') as f:
        f.write(f'{name_file}\n{name_file}_encripted\n{size_file}\n{number_images}\n{extension}')
    return path_save

def file_to_video(file, output_video, height = HEIGHT, width = WIDTH ,frame_rate=30):
    with open(file, 'rb') as f:
        data = f.read()
    #configuracion del archivo
    total_pixels = width * height
    total_images = mt.ceil(len(data) / total_pixels)
    path_save = save_info(file, total_images)
    destination_path = os.path.join(path_save, output_video)
    # Configurar el VideoWriter
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # Codec para archivo MP4
    video = cv2.VideoWriter(destination_path, fourcc, frame_rate, (width, height))

    #inicio
    for i in range(total_images):
        start = i * total_pixels
        end = start + total_pixels
        block_pixels = data[start:end]
        #rellena con ceros
        if len(block_pixels) < total_pixels:
            block_pixels += bytes(total_pixels - len(block_pixels))
        #creacion de la imagen
        data_image = np.array(list(block_pixels), dtype=np.uint8).reshape((height, width))
        brg_image = cv2.cvtColor(data_image, cv2.COLOR_GRAY2BGR)
        cv2.imwrite(path_save + f'image_{i+1}.png', brg_image)
        video.write(brg_image)  #Escribir el frame en el video
    # Liberar el VideoWriter
    video.release()

def video_to_file(file_path):
    with open(file_path + 'info.txt', 'r') as f:
        file_name, file_encripted, size_file, number_images, extension = f.read().split('\n')

    total_written = 0
    video = cv2.VideoCapture(file_path + file_name + '_video.mkv')
    with open( file_path + file_name + extension, 'wb') as f:
        while True:
            success, frame = video.read()
            if not success:
                break
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            cv2.imwrite(file_path + file_name + '_image.png', frame)
            pixel_data = np.array(frame, dtype=np.uint8)
            pixel_bytes = pixel_data.flatten().tobytes()
            remaining_size = int(size_file) - total_written
            if remaining_size > 0:
                # Escribir solo la cantidad necesaria
                f.write(pixel_bytes[:remaining_size])
                total_written += len(pixel_bytes[:remaining_size])
                # Detenernos si alcanzamos el tamaño del archivo original
                if total_written >= int(size_file):
                    break
    f.close()
    video.release()

def version_programa():
    print('version 1.0')
    print('Hello, welcome to the video compression program. \n')
    print('select the option: \n')
    print('1) file to video \n2) video to file \n3) exit \n')
    choise = int(input('enter the choise: '))

    if choise == 1:
        file_path = input('enter the path file to compress: ')
        file_name = os.path.splitext(os.path.basename(file_path))[0]
        file_to_video(file_path, file_name+'_video.mkv')
    elif choise == 2:
        file_path = input('enter the path file to decompress: ')
        file_name = os.path.splitext(os.path.basename(file_path))[0]
        video_to_file(file_path)

#todo casi funcional, solo que no guarda bien los archivos, por ahora quisiera
#tratar de realizarlo leyendo de otra manera los frames
if __name__ == '__main__':

    version_programa()

    #file_path = input('enter the path file to compress: ')
    #create_images(file_path)
    #create_file(file_path+'info.txt')