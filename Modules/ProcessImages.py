"""
Author: Big Panda
Created Time: 17.03.2025 11:51
Modified Time: 17.03.2025 11:51
Description:
    Nake background of our pets transparent
"""
import sys

from PIL import Image  # Pillow 库


def process_image(input_path, output_path):
    """
    使用 Pillow 去除图片的白色背景并保存为透明背景的 PNG 文件
    """
    # 打开图片
    image = Image.open(input_path).convert("RGBA")  # 转换为 RGBA 模式（支持透明度）

    # 获取图片数据
    data = image.getdata()

    # 将白色背景（RGB 接近 (255, 255, 255)）转换为透明
    new_data = []
    for item in data:
        # 判断是否为白色背景（可以根据需要调整阈值）
        if item[0] > 240 and item[1] > 240 and item[2] > 240:
            new_data.append((255, 255, 255, 0))  # 设置为完全透明
        else:
            new_data.append(item)  # 保留其他颜色

    # 更新图片数据
    image.putdata(new_data)

    # 保存处理后的图片
    image.save(output_path, "PNG")


if __name__ == "__main__":
    # input_path_ = r'C:\Project\PythonProject\LongSitReminder\Pets\MengJi.png'
    # output_path_ = r'C:\Project\PythonProject\LongSitReminder\Pets\MengJi_pro.png'

    # input_path_ = r'C:\Project\PythonProject\LongSitReminder\Pets\MengJi_Orange.png'
    # output_path_ = r'C:\Project\PythonProject\LongSitReminder\Pets\MengJi_Orange_pro.png'

    # input_path_ = r'C:\Project\PythonProject\LongSitReminderPet\DrawingData\MengJi_Orange_Drag.png'
    # output_path_ = r'C:\Project\PythonProject\LongSitReminderPet/Pets/MengJi_Orange_Drag.png'

    # input_path_ = r'C:\Project\PythonProject\LongSitReminderPet\DrawingData\MengJi_White_Drag.png'
    # output_path_ = r'C:\Project\PythonProject\LongSitReminderPet/Pets/MengJi_White_Drag.png'

    input_path_ = r'C:\Project\PythonProject\LongSitReminderPet\DrawingData\Icon.png'
    output_path_ = r'C:\Project\PythonProject\LongSitReminderPet/Icons/Icon.png'
    process_image(input_path_, output_path_)
