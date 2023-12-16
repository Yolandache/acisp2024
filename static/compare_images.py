import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim

def compare_images(image1_path, image2_path):
    # 读取图像
    image1 = cv2.imread(image1_path)
    image2 = cv2.imread(image2_path)

    # 将图像调整为相同大小
    target_shape = (300, 300)  # 根据需要修改大小
    image1_resized = cv2.resize(image1, target_shape)
    image2_resized = cv2.resize(image2, target_shape)

    # 将图像转换为灰度图
    gray1 = cv2.cvtColor(image1_resized, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(image2_resized, cv2.COLOR_BGR2GRAY)

    # 计算图像的结构相似性指数（SSIM）
    ssim_index, _ = ssim(gray1, gray2, full=True)

    return ssim_index

# 两个图标的文件路径
# icon1_path = "D:/fakeapp/dist_f2/res/mipmap-hdpi/icon.png"
# icon2_path = "D:/fakeapp/dist_t2/res/mipmap-hdpi/ic_launcher.png"
# 两个图标的文件路径
icon1_path = 'D:/fakeapp/dist_f/res/mipmap-hdpi/app_icon.png'
icon2_path = "D:/fakeapp/dist_t2/res/mipmap-hdpi/ic_launcher.png"

# 比较图标相似度
similarity_index = compare_images(icon1_path, icon2_path)
print(f"SSIM图标相似度: {similarity_index}")
