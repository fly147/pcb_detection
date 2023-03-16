<<<<<<< HEAD
from django.shortcuts import render, redirect
import os
from django.http import HttpResponse, JsonResponse
from pcb_detection import settings
from django.conf import settings
import base64
from PIL import Image
import io
from django.template import loader
from . import models
import hashlib
from datetime import datetime


# PCB检测
def detect(image_file):
    os.system("python D:\\Develop\\PaddleDetection\\deploy\\python\\infer.py \
                        --model_dir=D:\\Develop\\inference_model\\faster_rcnn_swin_tiny_fpn_3x_coco \
                        --image_file=%s \
                        --output_dir=D:\\Develop\\pcb_detection\\static\\output \
                        --device=CPU" % image_file)
    output_image = image_file.split('\\')[-1]
    print("output_image:", output_image)
    return output_image

# 压缩base64的图片
def compress_image_bs4(b64, mb=100, k=0.9):
    """不改变图片尺寸压缩到指定大小
    :param outfile: 压缩文件保存地址
    :param mb: 压缩目标，KB
    :param step: 每次调整的压缩比率
    :param quality: 初始压缩比率
    :return: 压缩文件地址，压缩文件大小
    """
    f = base64.b64decode(b64)
    with io.BytesIO(f) as im:
        o_size = len(im.getvalue()) // 1024
        if o_size <= mb:
            return b64
        im_out = im
        while o_size > mb:
            img = Image.open(im_out)
            x, y = img.size
            out = img.resize((int(x * k), int(y * k)), Image.ANTIALIAS)
            im_out.close()
            im_out = io.BytesIO()
            out.save(im_out, 'jpeg')
            o_size = len(im_out.getvalue()) // 1024
        b64 = base64.b64encode(im_out.getvalue())
        im_out.close()
        return str(b64, encoding='utf8')


def upload(request):
    if request.method == 'POST':
        url = request.POST.get('img')
        img = url.split(',')[1]
        bytes = base64.b64decode(img, validate=True)
        filePath = os.path.join(settings.MEDIA_ROOT, 'test.jpg')
        with open(filePath, 'wb') as fp:
            fp.write(bytes)
        # imagePath = '/home/huhao/workface/Django-PCB-Detection/pcb_detection/'+ filePath
        imagePath = 'D:\\Develop\\pcb_detection\\'+ filePath
        # 在这里进行目标检测，并返回结果
        deImagePath = detect(imagePath)
        deImagePath = 'D:\\Develop\\pcb_detection\\output\\'+ deImagePath
        pic = open(deImagePath, "rb")
        b64 = base64.b64encode(pic.read())
        pic.close()
        result = compress_image_bs4(b64)
        print("result:",result)
        context = {'result': result,}
        print(context)
        # t = loader.get_template("upload.html")
        # c = {"result": result}
        # return HttpResponse(t.render(c, request), content_type="application/xhtml+xml")
        return render(request, 'upload.html', locals())
        # return render(request, 'upload.html')
    else:
        return render(request, 'upload.html')


def camera(request):
    if request.method == 'POST':
        if request.session.get('is_login', None):
            user = models.User.objects.get(
                username=request.session.get('user_name'))
        url = request.POST.get('img')
        img = url.split(',')[1]
        bytes = base64.b64decode(img, validate=True)
        nowtime = datetime.now()
        file_name = nowtime.strftime('%Y-%m-%d-%H-%M-%S') + '.jpg'
        file_path = os.path.join(settings.MEDIA_ROOT, file_name)  # 原始图片
        with open(file_path, 'wb') as fp:
            fp.write(bytes)
        imagePath = 'D:\\Develop\\pcb_detection\\' + file_path  # 原始图片
        # 在这里进行目标检测，并返回结果
        detect(imagePath)
        check_image_path = os.path.join(
            settings.OUTPUT_ROOT, file_name)  # 检测图片
        # 保存至数据库
        new_check = models.Check.objects.create()
        new_check.check_time = nowtime
        new_check.origin_picture = file_path
        new_check.check_picture = check_image_path
        new_check.check_pepole = user
        new_check.save()
        return render(request, 'camera.html', locals())
    elif request.method == 'GET':
        return render(request, 'camera.html')


def popup(request):
    return render(request, 'popup.html')


def check(request):
    return render(request, 'check.html')

# 注册登录


def hash_code(s, salt='pcb'):  # 加点盐
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())  # update方法只接收bytes类型
    return h.hexdigest()



def login(request):
    if request.session.get('is_login', None):
        return redirect('/show_check/')
    if request.method == "POST":
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        if username and password:  # 确保用户名和密码都不为空
            username = username.strip()
            try:
                user = models.User.objects.get(username=username)
                if user.password == hash_code(password):
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.username
                    return redirect('/show_check/')
                else:
                    message = "密码不正确！"
            except:
                message = "用户名不存在！"
        return render(request, 'login.html', {"message": message})
    return render(request, 'login.html')


def register(request):
    if request.session.get('is_login', None):
        # 登录状态不允许注册。你可以修改这条原则！
        return redirect("/show_check/")
    if request.method == "POST":
        username = request.POST.get('username', None)
        password1 = request.POST.get('password1', None)
        password2 = request.POST.get('password2', None)
        message = "请检查填写的内容！"
        if password1 != password2:  # 判断两次密码是否相同
            message = "两次输入的密码不同！"
            return render(request, 'register.html', locals())
        else:
            same_name_user = models.User.objects.filter(username=username)
            if same_name_user:  # 用户名唯一
                message = '用户已经存在，请重新选择用户名！'
                return render(request, 'register.html', locals())
            # 当一切都OK的情况下，创建新用户
            new_user = models.User.objects.create()
            new_user.username = username
            new_user.password = hash_code(password1)
            new_user.save()
            return redirect('/login/')  # 自动跳转到登录页面
    return render(request, 'register.html', locals())


def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/login/")
    request.session.flush()
    return redirect("/login/")


# 用户界面

def show_book_func(request):
    # book_obj_list = models.Book.objects.all()
    return render(request, 'show_book.html', locals())


def show_check_func(request):
    if request.method == 'POST':
        if request.session.get('is_login', None):
            user = models.User.objects.get(
                username=request.session.get('user_name'))
        url = request.POST.get('img')
        img = url.split(',')[1]
        bytes = base64.b64decode(img, validate=True)
        nowtime = datetime.now()
        file_name = nowtime.strftime('%Y-%m-%d-%H-%M-%S') + '.jpg'
        file_path = os.path.join(settings.MEDIA_ROOT, file_name)  # 原始图片路径
        with open(file_path, 'wb') as fp:
            fp.write(bytes)
        imagePath = 'D:\\Develop\\pcb_detection\\' + file_path  # 原始图片绝对路径
        detect(imagePath)  # 在这里进行目标检测
        check_image_path = os.path.join(
            settings.OUTPUT_ROOT, file_name)  # 检测图片路径
        prefix = 'http://127.0.0.1:8000/'
        # 保存至数据库
        new_check = models.Check.objects.create()
        new_check.check_time = nowtime
        new_check.origin_picture = prefix+file_path
        new_check.check_picture = prefix+check_image_path
        new_check.check_pepole = user
        new_check.save()
        data = {'check_image_path': new_check.check_picture}
        return JsonResponse(data)
        # return render(request, 'show_check.html', {'check_image_path': check_image_path})
        # return render(request, 'show_check.html', locals())
    elif request.method == 'GET':
        # return render(request, 'show_check.html')
        return render(request, 'show_check.html', locals())


def show_defect(request):
    defect_obj_list = models.Check.objects.all()
    return render(request, 'show_defect.html', locals())
=======
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
>>>>>>> acd14c039019ca311530c0592841de386bbb920c
