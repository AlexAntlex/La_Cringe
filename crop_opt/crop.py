import os
from PIL import Image
im1 = Image.open("123.jpg")

width = im1.size[0]
height = im1.size[1]

if width < height: #Если изображение вертикальное - отрезает сверху и снизу одинаковые куски => получается квадрат
    y = height - width
    y = y/2
    y2 = height - y
    im_crop = (0,y,width,y2)
    im2 = im1.crop(im_crop)
    im2.save("im2.jpg")

if width > height: #Если изображение горизонтальное - отрезает слева и справа одинаковые куски => получается квадрат
    x = width - height
    x = x/2
    x2 = width - x
    im_crop = (x,0,x2,height)
    im2 = im1.crop(im_crop)


if width == height:
    im2 = im1
im2.save("123_crop.jpg")
os.system("cjpeg -quant-table 2 -quality 60 -outfile 123_crop_opt.jpg 123_crop.jpg")
print(im2.size)