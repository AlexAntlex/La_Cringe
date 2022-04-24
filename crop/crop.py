from PIL import Image

def crop(image):
    im1 = Image.open(image)

    width = im1.size[0]
    height = im1.size[1]

    if width < height: #Если изображение вертикальное - отрезает сверху и снизу одинаковые куски => получается квадрат
        y = height - width
        y = y/2
        y2 = height - y
        im_crop = (0, y, width, y2)
        im2 = im1.crop(im_crop)
        im2.save(f"static/user_files/crop/{image}")

    if width > height:     #Если изображение горизонтальное - отрезает слева и справа одинаковые куски => получается квадрат
        x = width - height
        x = x/2
        x2 = width - x
        im_crop = (x, 0, x2, height)
        im2 = im1.crop(im_crop)
        im2.save(f"static/user_files/crop/{image}")

    if width == height:         #Просто перезаписывает картинку, если она уже квадратная
        im1.save(f"static/user_files/{image}")
