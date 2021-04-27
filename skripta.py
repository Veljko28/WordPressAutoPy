from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
 
from slika import getImage, resizeImage, removeImageBorder
import time
import sys
import re


chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9000")

driver = webdriver.Chrome(executable_path='C:/Users/Sasha/chromedriver.exe', options=chrome_options)


# CMD komande za startovanje broweser-a
# cd C:\Program Files (x86)\Google\Chrome\Application
# chrome.exe --remote-debugging-port=9000 --user-data-dir=C:\Users\Sasha\Desktop\Artisoft\pyTest\ChromeData


# Uzima sve linkove sajtova jedne sekcije
def getSection(start):

    driver.get(start)
    try: 
       products = driver.find_element_by_class_name("product-list")
       links = products.find_elements_by_tag_name("a")
       hrefs = []
       for i in links:
           link = i.get_attribute('href')
           website = link.split('.')[1]
           if link not in hrefs and website != 'youtube':
               hrefs.append(i.get_attribute('href'))
       return hrefs
    except:
        print("Greska pri dobijanji sekcija")


# Uzima podatke sa datog sajta i vraca ih
def getinfo(website):
    driver.get(website)
    try:
        name = website.split('/')[-1].replace("-", " ")
        info = driver.find_element_by_class_name("product-details")
        table = driver.find_element_by_class_name("product-harvest")
        anchors = table.find_elements_by_tag_name("a")
        for a in anchors:
            driver.execute_script("arguments[0].setAttribute('href',arguments[1])", a, "")
            driver.execute_script("arguments[0].setAttribute('style',arguments[1])", a, "pointer-events: none; \
            cursor: default; color: #333")

        harvest = driver.find_element_by_class_name("product-harvest")

        info_str = info.get_attribute('outerHTML')
        harvest_str = harvest.get_attribute('outerHTML')
        #print(name)
        #print(data.get_attribute('outerHTML') + '\n')
        #print(harvest.get_attribute('outerHTML'))

        product = driver.find_element_by_class_name("product")
        slika = product.find_element_by_class_name("image")
        image = slika.find_element_by_tag_name("img")
        time.sleep(3)

        imageName = getImage(image.get_attribute("src"), driver)
        while imageName is None:
            time.sleep(3)
        resizeImage(imageName)

        return name, info_str, harvest_str, imageName
    except:
        print("Unexpected error:", sys.exc_info()[0])
    finally:
        time.sleep(2)

# Duplicira poslednju stranicu i prepisuje podatke iz getInfo


def wordpress_actions(name, info_str, harvest_str, imageName, product_tag):
    driver.get("http://127.0.0.1:81/wordpress/wp-admin/edit.php?post_type=product")

    table = driver.find_element_by_id("the-list")
    last_post = table.find_element_by_class_name("name")
    wp_actions = last_post.find_element_by_class_name("row-actions")
    duplicate = wp_actions.find_element_by_class_name("duplicate")

    ActionChains(driver).move_to_element(last_post).move_to_element(duplicate).click().perform()

    post_title = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "title")))

    # UPIS NAZIVA
    title = driver.find_element_by_id("title")
    title.clear()
    title.send_keys(name)

    # SLIKA
    imageDiv = driver.find_element_by_id("postimagediv")
    handleDiv = imageDiv.find_element_by_class_name("handlediv")

    if handleDiv.get_attribute("aria-expanded") == "false":
        open_image_div = ActionChains(driver)
        open_image_div.move_to_element(handleDiv).click().perform()

    imageDiv.find_element_by_class_name("attachment-266x266").click()
    imagePath = "C:\\Users\\Sasha\\Desktop\\Artisoft\\pyTest\\MoneyMaker\\" + imageName

    input_file = "//input[starts-with(@id,'html5_')]"
    driver.find_element_by_xpath(input_file).send_keys(imagePath)
    WebDriverWait(driver, 5).\
        until(EC.element_to_be_clickable((By.XPATH, "//*[@id='__wp-uploader-id-0']/div[4]/div/div[2]/button")))
    driver.find_element_by_xpath("//*[@id='__wp-uploader-id-0']/div[4]/div/div[2]/button").click()

    # INFO I TABELA
    data_form = driver.find_element_by_id("postexcerpt")
    open_button = data_form.find_element_by_class_name("handlediv")

    if open_button.get_attribute("aria-expanded") == "false":
        open_area = ActionChains(driver)
        open_area.move_to_element(open_button).click().perform()

    html_form = data_form.find_element_by_id("excerpt-html")
    open_form = ActionChains(driver)
    open_form.move_to_element(html_form).click().perform()

    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "excerpt")))
    textbox = data_form.find_element_by_class_name("wp-editor-area")
    textbox.click()
    textbox.clear()
    textbox.send_keys(info_str)
    textbox.send_keys(harvest_str)

    tag = driver.find_element_by_id("new-tag-product_tag")
    tag.click()
    tag.clear()
    tag.send_keys(product_tag)
    add_tag = driver.find_element_by_xpath('//*[@id="product_tag"]/div/div[2]/input[2]')
    ActionChains(driver).move_to_element(add_tag).click().perform()

    #WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="publish"]')))
    #publish_button = driver.find_element_by_id("wpb-save-post")
    #ActionChains(driver).move_to_element(publish_button).double_click().perform()

    driver.execute_script('window.scrollTo(0,0)')
    time.sleep(3)
    driver.find_element_by_xpath('//*[@id="publishing-action"]').click()
    time.sleep(5)
    driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')


if __name__ == "__main__":
    section = "https://www.agromarket.rs/srb/zastita-bilja/20/Pomocna-sredstva"
    links = getSection(section)
    product_tag = section.split('/')[-1][:-1]


    # for href in links:
    #     name, info_str, harvest_str, imageName = getinfo(href)
    #     info = " ".join(info_str.split())
    #     harvest = " ".join(harvest_str.split())
    #    # wordpress_actions(name, info, harvest, imageName, product_tag)

    name, info_str, harvest_str, imageName = getinfo('https://www.agromarket.rs/srb/proizvod/287/Pomocna-sredstva/SMARTWET')
    info = " ".join(info_str.split())
    harvest = " ".join(harvest_str.split())
    wordpress_actions(name, info, harvest, imageName, product_tag)

    driver.quit()









