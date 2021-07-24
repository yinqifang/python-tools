import os

from PIL import Image


# 图片工具
class ImageTools:

    # 图片拼接
    def combine(self, new_file_name, src_file_name_list, delete_src_files_after_combine=False):
        """
        拼接图片
        :param new_file_name: 拼接后的图片，完整路径
        :param src_file_name_list: 要拼接的图片列表，必须是个list
        :param delete_src_files_after_combine: 拼接后是否删除原图片，True表示删除
        :return:
        """
        # 确保目标文件夹存在
        self.check_and_make_dir(new_file_name)

        # 计算图片总长度和最大宽度
        height = 0
        width = 0
        for src_file in src_file_name_list:
            img = Image.open(src_file)
            (tmp_width, tmp_height) = img.size
            height += tmp_height
            if width < tmp_width:
                width = tmp_width
            pass

        # 创建空白长图
        result = Image.new(Image.open(src_file_name_list[0]).mode, (width, height))
        # 拼接图片
        cursor_height = 0
        for src_file in src_file_name_list:
            im = Image.open(src_file)
            result.paste(im, box=(0, cursor_height))
            cursor_height += im.height
        # 保存图片
        result.save(new_file_name)
        # 清理临时文件
        if delete_src_files_after_combine:
            for src_file in src_file_name_list:
                os.remove(src_file)
        print('截图完毕 ', new_file_name)
        pass

    # 确保文件目录存在
    def check_and_make_dir(self, full_file_name):
        path = self.get_path_of_file(full_file_name)
        if not os.path.exists(path):
            os.makedirs(path)

    # 获取文件所属的文件夹路径
    def get_path_of_file(self, full_file_name):
        (file_path, file_name) = os.path.split(full_file_name)
        return file_path

if __name__ == '__main__':
    pass
