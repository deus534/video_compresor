import imageio as Img
import numpy as np
import cv2

def create_video(file_name, video_output,width=1280, height=720):
    video = Img.get_writer(video_output, fps=30, codec='ffv1')
    with open(file_name, 'rb') as f:
        data = f.read()
        while len(data)<(width*height):
            data += bytes(width*height - len(data))
        frame = np.array(list(data), dtype=np.uint8).reshape((height, width))
        frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
        print(f'shape: {frame.shape}, type: {frame.dtype}')
        Img.imwrite('image_input.png', frame )
        video.append_data(frame)
    video.close()

def create_images( video_name ):
    video = Img.get_reader(video_name)
    for i, frame in enumerate(video):
        print(f'shape: {frame.shape}, type: {frame.dtype}')
        Img.imwrite('image_output.png', frame)
def compare_images( img_1, img_2):
    img1 = cv2.imread(img_1)
    img2 = cv2.imread(img_2)
    if img1.shape == img2.shape:
        difference = cv2.subtract(img1, img2)
        b, g, r = cv2.split(difference)
        if cv2.countNonZero(b) == 0 and cv2.countNonZero(g) == 0 and cv2.countNonZero(r) == 0:
            print(cv2.countNonZero(b))
            print(cv2.countNonZero(g))
            print(cv2.countNonZero(r))
            print("The images are exactly the same")
        else:
            print("The images are not exactly the same")

create_video('prueba.pdf', 'video.avi')
create_images('video.avi')
compare_images('image_input.png', 'image_output.png')





