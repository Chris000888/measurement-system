import sys,pygame
import cv2
# from MeasurementSystem import *
from tkinter.filedialog import * 
from fastapi import FastAPI, File, UploadFile
from base64 import encodebytes
from pydantic import BaseModel
from PIL import Image
import os
import io
import json

app = FastAPI()

@app.post("/getSize")
async def getSize(file: bytes = File(...)):
    # Save received image in specific file
    pygame.init()
    script_dir = os.path.dirname(__file__)
    file_path = "./images/input.jpg"
    file.save('./images/input.jpg')
    file_path = "./images/input.jpg"
    imgPath = file_path
    image = pygame.image.load(imgPath)

    # Get real dimensions on the image
    imagerect = image.get_rect()
    realWidth, realHeight = imagerect.size

    # Create blank image object
    scaleWidth, scaleHeight = 400,600
    image = pygame.transform.scale(image,(scaleWidth,scaleHeight))
    imagerect = image.get_rect()
    pygame.display.set_caption("Measurement System")

    # Write datas on image and save
    global contourBoxes
    contourBoxes = FindShapes(imgPath) 
    image = pygame.image.load("RESULT.png")
    image = pygame.transform.scale(image,(400,600))
    image = pygame.image.load("RESULT.png")
    image = pygame.transform.scale(image,(400,600))
    
    # Preparing image for return
    image_result = Image.open("./RESULT.png","r")
    byte_arr = io.BytesIO()
    image_saved = image_result.save(byte_arr, format='PNG') # convert the PIL image to byte array
    encoded_img = encodebytes(byte_arr.getvalue()).decode('ascii') # encode as base64
    
    
    img_w, img_h = image_result.size
    background = Image.new('RGBA', (1440, 900), (255, 255, 255, 255))
    bg_w, bg_h = background.size
    offset = ((bg_w - img_w) // 2, (bg_h - img_h) // 2)
    background.paste(image_result, offset)
    background.save('out.png')
    
    data = {
        'realWidth': realWidth,
        'realHeight': realHeight,
        # 'image': "data:image/png;base64,{}".format(str(encoded_img)),
        'suggested_size': "XL",
    }

    # return flask.send_from_directory('./', 'RESULT.png')
    return json.dumps(data)