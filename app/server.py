import os



import subprocess
proc = subprocess.Popen('apt-get -y update', shell=True, stdin=None)
proc.wait()
proc = subprocess.Popen('apt-get install -y libgtk2.0-dev', shell=True, stdin=None)
proc.wait()
# subprocess.run("apt-get install -y libgtk2.0-dev")


import aiohttp
import asyncio
import uvicorn
from io import BytesIO
from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import HTMLResponse, JSONResponse
from starlette.staticfiles import StaticFiles

import sys
import numpy as np
import cv2
from pathlib import Path
import datetime
import easyocr


basedir = os.path.abspath(os.path.dirname(__file__))


path = Path(__file__).parent
path2 = os.getcwd()



#convert 4 channels to 3
def remove_fourth_channel(img):
    if len(img.shape) > 2 and img.shape[2] == 4:
        #convert the image from RGBA2RGB
        image = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
    elif len(img.shape) < 2:
        image = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
    else:
        image = img
    return image

###routine 3
def prep(img):
    #check image channels
    if len(img.shape) > 2 and img.shape[2] == 3:
        pass
    else:
        img = remove_fourth_channel(img)
    
    
    return img

###routine1
def get_age(sess, img):
    img = cv2.resize(img, (224, 224))
    # print(img)
    img = img/255.0
    # print(img)
    img[:,:,0] = (img[:,:,0] - mean[0])/std[0]
    img[:,:,1] = (img[:,:,1] - mean[1])/std[1]
    img[:,:,2] = (img[:,:,2] - mean[2])/std[2]

    # img  = np.array(normalized_img)
    # print(img.shape)
    img = img.transpose((2, 0, 1))
    # print(img.shape)
    im = img[np.newaxis, :, :, :]
    # print(im.shape)
    im = im.astype(np.float32)
    input_name = sess.get_inputs()[0].name
    label_name = sess.get_outputs()[0].name
    result = sess.run(None, {input_name: im})
    # print(result)
    oup = result[0].item()
    return oup

def preproc(img):
    # print(img)
    img = img/255.0
    # print(img)
    img[:,:,0] = (img[:,:,0] - mean[0])/std[0]
    img[:,:,1] = (img[:,:,1] - mean[1])/std[1]
    img[:,:,2] = (img[:,:,2] - mean[2])/std[2]

    # img  = np.array(normalized_img)
    # print(img.shape)
    img = img.transpose((2, 0, 1))
    # print(img.shape)
    im = img[np.newaxis, :, :, :]
    # print(im.shape)
    im = im.astype(np.float32)
    return im


app = Starlette()
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_headers=['X-Requested-With', 'Content-Type'])
app.mount('/static', StaticFiles(directory='app/static'))


async def download_file(url, dest):
    if dest.exists(): return
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.read()
            with open(dest, 'wb') as f:
                f.write(data)


async def setup_learner():
    # await download_file(export_file_url, path / export_file_name)
    try:
        sess =  easyocr.Reader(['en'])
        return sess
    except RuntimeError as e:
        if len(e.args) > 0 and 'CPU-only machine' in e.args[0]:
            print(e)
            message = "\n\nModel couldn't load"
            raise RuntimeError(message)
        else:
            raise


loop = asyncio.get_event_loop()
tasks = [asyncio.ensure_future(setup_learner())]
sess = loop.run_until_complete(asyncio.gather(*tasks))[0]
loop.close()


@app.route('/')
async def homepage(request):
    html_file = path / 'view' / 'index.html'
    return HTMLResponse(html_file.open().read())


@app.route('/analyze', methods=['POST'])
async def analyze(request):
    img_data = await request.form()
    img_bytes = await (img_data['file'].read())
    img = cv2.imdecode(np.fromstring(img_bytes, np.uint8), cv2.IMREAD_UNCHANGED)
def preproc(img):
    img = (img)
    reader.readtext(img)

    for detection in result: 
        text = detection[1]
        res_op = text +'\n'
        
    return JSONResponse({'result': res_op})


if __name__ == '__main__':
    if 'serve' in sys.argv:
        uvicorn.run(app=app, host='0.0.0.0', port=5000, log_level="info")
