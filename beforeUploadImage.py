import os
import random
import string

from PIL import Image


def crop_center(pil_img, crop_width: int, crop_height: int) -> Image:
    img_width, img_height = pil_img.size
    return pil_img.crop(((img_width - crop_width) // 2,
                         (img_height - crop_height) // 2,
                         (img_width + crop_width) // 2,
                         (img_height + crop_height) // 2))


def crop_max_square(pil_img):
    return crop_center(pil_img, min(pil_img.size), min(pil_img.size))


def image_crop(img, UPLOAD_FOLDER_USER, filename):
    im = Image.open(img)
    im_new = crop_max_square(im)
    im_new = im_new.resize((300, 300))
    im_new.save(UPLOAD_FOLDER_USER + "miniature/" + filename)


def image_crop_avatar(img, UPLOAD_FOLDER_USER, filename):
    im = Image.open(img)
    im_new = crop_max_square(im)
    im_new = im_new.resize((300, 300))
    im_new.save(UPLOAD_FOLDER_USER + filename)


def rename_image(ext, path):
    let = string.ascii_letters + string.digits
    name = ''.join(random.choice(let) for i in range(42)) + f'.{ext}'
    while os.path.exists(path + name):
        name = ''.join(random.choice(let) for i in range(42)) + f'.{ext}'
    return name
