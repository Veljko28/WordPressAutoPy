from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains

from slika import getImage, resizeImage, removeImageBorder, imageClear
import time
import sys
import re
import os

chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9000")

driver = webdriver.Chrome(executable_path='C:/Users/Sasha/chromedriver.exe', options=chrome_options)


# CMD komande za startovanje broweser-a
# cd C:\Program Files (x86)\Google\Chrome\Application
# chrome.exe --remote-debugging-port=9000 --user-data-dir=C:\Users\Sasha\Desktop\Artisoft\pyTest\ChromeData
# cd C:\Users\Sasha\Desktop\Artisoft\pyTest\MoneyMaker
# py filename.py

def getSection(section):
    driver.get(section)
    try:
        products = driver.find_element_by_id("elements")
        list = products.find_elements_by_class_name("product-component")
        # hrefs = []
        #for prod in list:
        #    anchor = prod.find_element_by_tag_name("a")
        #    ext = anchor.get_attribute('href')
        #    hrefs.append('https://savacoop.rs/'+ext)

        return list
    except:
        print("Greska pri dobijanji sekcija")

def getInfo(link):
    driver.get(link)
    try:
        name = driver.find_element_by_xpath('/html/body/div[2]/main/div[2]/div[1]/div[1]/div/div/div[2]/h1');
        main_title = name.get_attribute('innerHTML')
        table = driver.find_element_by_xpath('/html/body/div[2]/main/div[2]/div[1]/div[1]/div/div/div[2]/div[2]/table')
        table_str = table.get_attribute('outerHTML')

        driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
        time.sleep(5)

        spec = driver.find_element_by_xpath('//*[@id="product-description"]/p[2]')
        ActionChains(driver).move_to_element(spec).perform()
        specifikacija = spec.get_attribute('innerHTML')

        img = driver.find_element_by_xpath('/html/body/div[2]/main/div[2]/div[1]/div[1]/div/div/div[1]/div/div[2]/div/div[1]/a/img')
        imageName = getImage(img.get_attribute('src'), driver)
        return main_title, table_str, imageName, specifikacija
    except:
        print("Unexpected error:", sys.exc_info()[0])
    finally:
        time.sleep(2)


def wordpress_actions(name, table_str, imageName, specifikacija):
    driver.get("https://www.poljokomerc.rs/wp-admin/edit.php?post_type=product")
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
    WebDriverWait(driver, 10).\
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
    textbox.send_keys(table_str)

    # SPECIFIKACIJA
    box = driver.find_element_by_xpath(
        '//*[@id="visual_composer_content"]/div/div[2]/div/div[1]/div[2]/div/div[2]/div[2]')
    controls = driver.find_element_by_xpath(
        '//*[@id="visual_composer_content"]/div/div[2]/div/div[1]/div[2]/div/div[2]/div[1]')
    edit = driver.find_element_by_xpath(
        '/html/body/div[1]/div[2]/div[3]/div[1]/div[5]/form/div/div/div[3]/div[1]/div[1]/div[2]/div[2]/div[1]/div/div[2]/div/div[1]/div[2]/div/div[2]/div[1]/div/a[2]')
    ActionChains(driver).move_to_element(box).move_to_element(controls).move_to_element(edit).click().perform()

    time.sleep(5)
    # textBtn = driver.find_element_by_xpath(
    #    "/html/body/div[1]/div[11]/div[1]/div[2]/div/div/div/div[1]/div[1]/div[2]/div/div[1]/div[2]/button[2]")
    # textBtn.click()
    # time.sleep(5)

    if 'Savacoop' in specifikacija:
        specifikacija = ''

    frame = driver.find_element_by_id('wpb_tinymce_content_ifr')
    driver.switch_to_frame(frame)
    ptag = driver.find_element_by_xpath('/html/body/p')
    ptag.clear()
    ptag.send_keys(specifikacija)
    driver.switch_to_default_content()

    save = driver.find_element_by_xpath('//*[@id="vc_ui-panel-edit-element"]/div[1]/div[3]/div/div/span[2]')
    save.click()
    WebDriverWait(driver, 5)

    #tag = driver.find_element_by_id("new-tag-product_tag")
    #tag.click()
    #tag.clear()
    #tag.send_keys(product_tag)
    #add_tag = driver.find_element_by_xpath('//*[@id="product_tag"]/div/div[2]/input[2]')
    #ActionChains(driver).move_to_element(add_tag).click().perform()

    #WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="publish"]')))
    #publish_button = driver.find_element_by_id("wpb-save-post")
    #ActionChains(driver).move_to_element(publish_button).double_click().perform()

    driver.execute_script('window.scrollTo(0,0)')
    time.sleep(3)
    driver.find_element_by_xpath('//*[@id="publishing-action"]').click()
    time.sleep(5)
    driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')


def template(section, scroll, items):
    driver.get(section)
    hrefs = []
    for i in range(scroll):
        driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
        time.sleep(3)

    for i in range(1, items):
        prod = driver.find_element_by_xpath('/html/body/div[2]/main/div[2]/div/div[2]/div[2]/div[1]/div['+str(i)+']/div/div[1]/a')
        hrefs.append(prod.get_attribute('href'))
    for href in hrefs:
        main_title, table_str, imageName, specifikacija = getInfo(href)
        wordpress_actions(main_title, table_str, imageName, specifikacija)

    imageClear()
    driver.quit()
