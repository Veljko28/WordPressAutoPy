import cv2
import numpy as np

# Pomocna funkcija koja sacuva sliku
def getImage(url, driver):
    driver.get(url)

    imageName = url.split('/')[-1]

    with open(imageName, 'wb') as file:
        file.write(driver.find_element_by_tag_name("img").screenshot_as_png)

    return imageName

def removeImageBorder(imagePath):
    img = cv2.imread(imagePath)
    h, w, c = img.shape
    crop_img = img[10:h, 10:w]
    cv2.imwrite(imagePath, crop_img)

def resizeImage(imagePath):
    removeImageBorder(imagePath)
    img = cv2.imread(imagePath)
    ht, wd, cc = img.shape
    ww = 800
    hh = 800
    color = (255, 255, 255)
    result = np.full((hh, ww, cc), color, dtype=np.uint8)

    xx = (ww - wd) // 2
    yy = (hh - ht) // 2
    result[yy:yy + ht, xx:xx + wd] = img

    cv2.imwrite(imagePath, result)
