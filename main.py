
from selenium import webdriver
import pytesseract
import requests
from PIL import Image
import io
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import cv2
import numpy as np

browser = webdriver.Firefox()
browser.get('http://challenge.nahamcon.com:31367/')
custom_config = '--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789/*+-'

while True:
    time.sleep(1)
    response = requests.get("http://challenge.nahamcon.com:31367/static/eqn.png")
    image = np.asarray(bytearray(response.content), dtype="uint8")
    img = cv2.imdecode(image, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    invert = 255 - thresh

    # img = Image.open(io.BytesIO(response.content))

    text = pytesseract.image_to_string(invert,lang="eng+equ",config=custom_config)
    text = text.replace("°","*").replace(" ","")
    wait = WebDriverWait(browser, 30)
    countElement = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "count")))
    print(text+"  "+str(countElement.get_property('value')))
    number =  eval(text)

    inputElement = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "eqn_ans")))
    value_input = ""
    if number%1!=0:
        value_input = '{:.4f}'.format(number)
    else:
        value_input = number
    inputElement.send_keys(value_input)
    inputElement.submit()
