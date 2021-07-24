from image_tools import ImageTools

if __name__ == '__main__':
    tar_file = 'd:/pt/combine.png'
    src_files = ['d:/pt/40324599211.png', 'd:/pt/40324599212.png']
    img_tools = ImageTools()
    img_tools.combine(tar_file, src_files)
    pass
