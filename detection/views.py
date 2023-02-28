from django.shortcuts import render
import os
from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from pcb_detection import settings
from django.conf import settings
from base64 import b64decode

# PCB检测
def detect(image_file):
    # image_file = '/home/huhao/workface/PCB_DATASET/images/01_missing_hole_03.jpg'
    os.system("python /home/huhao/workface/PaddleDetection/deploy/python/infer.py \
                        --model_dir=/home/huhao/workface/inference_model/faster_rcnn_swin_tiny_fpn_3x_coco \
                        --image_file=%s \
                        --device=CPU" %image_file)
    # output_image = '/home/huhao/workface/Django-PCB-Detection/pcb_detection/output/'+ image_file.split('/')[-1]
    output_image = image_file.split('/')[-1]
    print(output_image)
    return output_image


def upload(request):
    if request.method == 'POST':
        # f = request.FILES['img_data']
        # filePath = os.path.join(settings.MEDIA_ROOT,f.name)
        # with open(filePath,'wb') as fp:
        #     for info in f.chunks():
        #         fp.write(info)
        url = request.POST.get('img')
        img = url.split(',')[1]
        bytes = b64decode(img, validate=True)
        filePath = os.path.join(settings.MEDIA_ROOT,'test.jpg')
        with open(filePath,'wb') as fp:
            fp.write(bytes)
        imagePath = '/home/huhao/workface/Django-PCB-Detection/pcb_detection/'+ filePath
        # 在这里进行目标检测，并返回结果
        result = detect(imagePath)
        context = {'result': result}
        print(context)
        return render(request, 'upload.html', context=context)
    elif request.method == 'GET':
        return render(request,'upload.html')

def camera(request):
    if request.method == 'POST':
        url = request.POST.get('img')
        img = url.split(',')[1]
        bytes = b64decode(img, validate=True)
        filePath = os.path.join(settings.MEDIA_ROOT,'test.jpg')
        with open(filePath,'wb') as fp:
            fp.write(bytes)
        # imagePath = '/home/huhao/workface/Django-PCB-Detection/pcb_detection/'+ filePath
        # 在这里进行目标检测，并返回结果
        # result = detect(imagePath)
        imagePath = '../' + filePath
        context = {'imagePath': imagePath}
        print(context)
        return render(request, 'camera.html', context=context)
    elif request.method == 'GET':
        return render(request, 'camera.html')

def popup(request):
    return render(request, 'popup.html')

def capture(request):
    return render(request,'capture.html')
