import cv2
import numpy as np
<<<<<<< HEAD
import uuid
import os
=======
>>>>>>> 2b5624d21d18d26e2922e2fdfa5681a22832592a

# Pomocna funkcija koja sacuva sliku
def getImage(url, driver):
    driver.get(url)

<<<<<<< HEAD
    imageName = str(uuid.uuid4()) + ".png"
=======
    imageName = url.split('/')[-1]
>>>>>>> 2b5624d21d18d26e2922e2fdfa5681a22832592a

    with open(imageName, 'wb') as file:
        file.write(driver.find_element_by_tag_name("img").screenshot_as_png)

    return imageName

def removeImageBorder(imagePath):
    img = cv2.imread(imagePath)
    h, w, c = img.shape
    crop_img = img[10:h, 10:w]
    cv2.imwrite(imagePath, crop_img)

def resizeImage(imagePath):
<<<<<<< HEAD
    #removeImageBorder(imagePath)
    img = cv2.imread(imagePath)
    ht, wd, cc = img.shape
    ww = 1000
    hh = 1000
    b, g, r = (img[0, 0])
    color = (r, g, b)
=======
    removeImageBorder(imagePath)
    img = cv2.imread(imagePath)
    ht, wd, cc = img.shape
    ww = 800
    hh = 800
    color = (255, 255, 255)
>>>>>>> 2b5624d21d18d26e2922e2fdfa5681a22832592a
    result = np.full((hh, ww, cc), color, dtype=np.uint8)

    xx = (ww - wd) // 2
    yy = (hh - ht) // 2
    result[yy:yy + ht, xx:xx + wd] = img

    cv2.imwrite(imagePath, result)
<<<<<<< HEAD

def imageClear():
    for file in os.listdir('C:\\Users\\Sasha\\Desktop\\Artisoft\\pyTest\\MoneyMaker'):
        if file.endswith('.png') or file.endswith('.jpg') or file.endswith('.jpeg'):
            os.remove(file)


if __name__ == "__main__":
    imageClear()
=======
>>>>>>> 2b5624d21d18d26e2922e2fdfa5681a22832592a
