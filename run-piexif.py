import piexif
import sys
import os
import re

def remove_all_exif(image_names):
    for image_name in image_names:
        try:
            piexif.remove(image_name)
            print(image_name,"exif信息清除完毕")
        except Exception:
            pass


def get_images():
    all_file_names = os.listdir()
    image_names = list()
    for file_name in all_file_names:
        if re.match(r".*\.(jpg|JPG|png)",file_name):
            image_names.append(file_name)
            print("已经将",file_name,"添加到列表!")
        else:
            pass
    return image_names


def main():
    image_names = get_images()
    remove_all_exif(image_names)
    
    pass


if __name__ == "__main__":
    main()
