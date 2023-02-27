from django.db import models
import os
import matplotlib.pyplot as plt 
import cv2


class PCBModel:
    # PCB检测
    def detect(image_file):
        # image_file = '/home/huhao/workface/PCB_DATASET/images/01_missing_hole_03.jpg'
        os.system("python /home/huhao/workface/PaddleDetection/deploy/python/infer.py \
                        --model_dir=/home/huhao/workface/inference_model/faster_rcnn_swin_tiny_fpn_3x_coco \
                        --image_file=%s \
                        --device=CPU" %image_file)
        output_image = '/home/huhao/workface/PaddleDetection/output/'+ image_file.split('/')[-1]
        print(output_image)
        infer_img = cv2.imread(output_image)
        plt.figure(figsize=(15, 10))
        plt.imshow(cv2.cvtColor(infer_img, cv2.COLOR_BGR2RGB))
        plt.show()
        return output_image