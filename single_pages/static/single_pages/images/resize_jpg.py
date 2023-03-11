from PIL import Image
import os
import re

def get_jepg_file():
    fname, pattern = "", r"\.(jpe?g)$"
    while True:
        fname = input("파일명:")
        if re.search(pattern, fname, re.IGNORECASE):
            break
        print(f"{fname}은 jepg 또는 jpg가 아닙니다.")
    return fname

def resize(fname:str):
    path = os.path.dirname(os.path.abspath(__file__))
    img_file = os.path.join(path, fname)

    img = Image.open(img_file)
    resized_img = img.resize((int(img.width*0.25), int(img.height*0.25)))

    new_img_file = img_file

    new_fname = os.path.splitext(fname)[0] + '_original.jpg'
    new_original_file = os.path.join(path, new_fname)

    os.rename(img_file, new_original_file)
    resized_img.save(new_img_file)
    img.close()

def main():
    fname = get_jepg_file()
    resize(fname)
    print("파일을 25% 축소했습니다.")

main()
