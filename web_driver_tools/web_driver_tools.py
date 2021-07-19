import os
import time

import selenium.webdriver.support.ui as ui
from PIL import Image


class WebDriverTools:
    driver = None

    # 初始化
    def __init__(self, driver):
        self.driver = driver
        self.wait = ui.WebDriverWait(driver, 10)

    # 截图某个元素
    def screenshot_on_element(self, element, full_file_name):
        self.check_and_make_dir(full_file_name)
        # 将元素滚动到视图中，顶端对齐
        print('滚动到元素')
        self.driver.execute_script("arguments[0].scrollIntoView();", element)
        element_location = element.location
        element_size = element.size

        element_height = element_size['height']
        # window高度要使用window的innerHeight，不能使用driver.get_window_size()['height']
        window_height = self.driver.execute_script("return window.innerHeight")
        if element_height <= window_height:
            # 窗口大小足够容纳整个element
            print("窗口足够大，不需要拼接图像")
            # 计算元素在视窗的相对坐标，应对底部元素较少不足以把element置为页面顶部的情况
            body_height = self.driver.find_element_by_tag_name("body").size['height']
            element_y = element_location['y']
            top = None
            if (body_height - element_y) > window_height:
                # 底部元素足够，element置顶显示
                print("元素已置顶")
                top = 0
            else:
                # 底部元素不足，element未置顶显示
                top = window_height - (body_height - element_y)
                print("元素未置顶， top值：" + str(top))
            # 截图（整个网页）
            self.driver.save_screenshot(full_file_name)  # saves screenshot of entire page
            print("截屏完毕，开始裁剪")
            left = element_location['x']
            right = element_location['x'] + element_size['width']
            bottom = top + element_height
            # 图片裁剪（只保留element内容）
            self.crop_image(full_file_name, left, top, right, bottom)
            print("截图完毕")
        else:
            # 窗口大小不能容纳整个element
            print("窗口不够大，需要拼接图像")
            screenshot_index = 0
            left = element_location['x']
            right = element_location['x'] + element_size['width']
            step = window_height
            remain_height = element_height
            path = self.get_path_of_file(full_file_name)
            # 记录中间过程文件
            tmp_files = []
            timestamp = time.time()
            while True:
                tmp_file_name = os.path.join(path, str(timestamp) + str(screenshot_index) + '.png')
                # 截图（整个网页）
                self.driver.save_screenshot(tmp_file_name)
                tmp_files.append(tmp_file_name)
                if remain_height <= step:
                    # 最后一张，可能包含非element内容
                    self.crop_image(tmp_file_name, left, 0, right, remain_height)
                    break
                else:
                    # 不包含非element内容
                    self.crop_image(tmp_file_name, left, 0, right, step)
                # 继续滚动
                remain_height -= step
                self.driver.execute_script("scrollBy(0,arguments[0]);", step)
                screenshot_index += 1
            # 合并图像
            # 创建空白长图
            result = Image.new(Image.open(tmp_files[0]).mode, (element_size['width'], element_size['height']))
            # 拼接图片
            idx = 0
            for tmp_file in tmp_files:
                im = Image.open(tmp_file)
                result.paste(im, box=(0, idx * im.height))
                idx += 1
            # 保存图片
            result.save(full_file_name)
            # 清理临时文件
            for tmp_file in tmp_files:
                os.remove(tmp_file)
            print('截图完毕 ', full_file_name)
        pass

    def pause(self, mark):
        # input("【" + str(mark) + "】按任意键继续...")
        pass

    # 确保文件目录存在
    def check_and_make_dir(self, full_file_name):
        path = self.get_path_of_file(full_file_name)
        if not os.path.exists(path):
            os.makedirs(path)

    # 图片裁剪
    def crop_image(self, file_name, left, top, right, bottom):
        im = Image.open(file_name)
        im = im.crop((left, top, right, bottom))
        im.save(file_name)
        print('裁剪完毕，目标文件：', file_name)

    # 获取文件所属的文件夹路径
    def get_path_of_file(self, full_file_name):
        (file_path, file_name) = os.path.split(full_file_name)
        return file_path


if __name__ == '__main__':
    pass
