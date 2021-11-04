import os
from PIL import Image
import cv2
import numpy as np


def resize_image(img_path):
    mywidth = 200

    try:
        img = Image.open(img_path)
        width_percent = (mywidth / float(img.size[0]))
        height_size = int((float(img.size[1]) * float(width_percent)))
        resizedimg = img.resize((mywidth, height_size), Image.ANTIALIAS)
        return resizedimg

    except:
        print('[DEBUG]: Não foi possível abrir a imagem')
        return False


def encode_image_to_uint8(img_path):
    valid_extensions = ('.jpg', '.png', '.jpeg')  # Extenções validas de arquivo.

    # Verifica se a varíavel "img_path" é realmente um arquivo
    # e se termina com uma das extenções válidas
    if not os.path.isfile(img_path) and img_path.endswith(valid_extensions):
        print('A imagem não é válida (ou não tenho permissão para acessá-la).')
        return

    # Le o binário do arquivo com "rb" (read binary) -> salva em uma variável
    with open(img_path, 'rb') as f:
        image_bytes = f.read()  # Salva o binário em "image_bytes"

    f.close()  # Fecha o arquivo

    return image_bytes


def decode_image_from_uint8(image_bytes):
    try:
        nparr = np.frombuffer(image_bytes, np.uint8)  # Decodifica os bytes de uint8 para um array de bytes (imagem)
        img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)  # Transforma os bytes da imagem em um objeto de imagem
        return img_np
    except Exception as E:
        print(f'[DEBUG]: erro na função decode_image_from_uint8: {E}')
