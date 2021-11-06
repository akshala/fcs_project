from captcha.image import ImageCaptcha
from io import BytesIO
import time
import random
import string
import os



def check_captcha(captcha_text):
    


def create_image_captcha(captcha_text):
    image_captcha = ImageCaptcha()
    image = image_captcha.generate_image(captcha_text)

    image_file = "captcha_"+captcha_text + ".png"
    imgByteArr = BytesIO()
    image.save(imgByteArr, format='PNG')
    imgByteArr = imgByteArr.getvalue()
    open(image_file, "wb").write(imgByteArr)

    print(image_file + " has been created.")
    time.sleep(30)
    delete_captcha(image_file)

def delete_captcha(image_file):
    os.system("rm " + image_file)

# img = ImageCaptcha(width = 280, height = 90)

captcha_text = ''

for i in range(8):
    captcha_text += random.choice(string.ascii_uppercase + string.digits[2:])


create_image_captcha(captcha_text)
# data = img.generate(captcha_text)
# data = ImageCaptcha.create_noise_dots(img, (0, 255, 255), number= 100)
# img.write(captcha_text, 'Captcha.png')