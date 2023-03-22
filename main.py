from selenium import webdriver
from time import sleep
import random
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.by import By
import pandas as pd
import csv
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome(executable_path="D:\\FILEPhanMem\\ChormeDrive\\chromedriver.exe")
data_comment = []
url_list = []
#url_list = ["https://www.booking.com/hotel/vn/mai-gia-huy.vi.html?"]

with open('Da_lat.csv', newline='') as inputfile:
    for row in csv.reader(inputfile):
        url_list.append(row[1])
url_list.pop(0)

for url_l in url_list[10:15]:
    # Open URL
    driver.get(url_l)
    sleep(10)

    # Click vao danh gia cua khach hang
    count = 0
    a = driver.find_elements(By.CSS_SELECTOR, 'li.a0661136c9')
    for A in a:
        count = count + 1

    if count == 5:
      next_pagination_cmt = driver.find_element(By.XPATH,'/html/body/div[4]/div/div[4]/div[1]/div[1]/div[1]/div/div[2]/div[1]/div/ul/li[5]/a')
      next_pagination_cmt.click()
      sleep(random.randint(2, 4))
    else:
        next_pagination_cmt = driver.find_element(By.XPATH,'/html/body/div[4]/div/div[4]/div[1]/div[1]/div[1]/div/div[2]/div[1]/div/ul/li[4]/a')
        next_pagination_cmt.click()
        sleep(random.randint(2, 4))
    # Click vao Ngon ngu
    try:
        next_pagination_cmt = driver.find_element(By.XPATH,
                                                  '/html/body/div[4]/div/div[4]/div[1]/div[1]/div[1]/div/div[2]/div[13]/div/div[1]/div[2]/div/div[3]/div[1]/div[2]/div[3]/button')
        next_pagination_cmt.click()
        sleep(2)
        # Click vao tieng viet
        next_pagination_cmt = driver.find_element(By.XPATH,
                                                  '/html/body/div[4]/div/div[4]/div[1]/div[1]/div[1]/div/div[2]/div[13]/div/div[1]/div[2]/div/div[3]/div[1]/div[2]/div[3]/div/div/ul/li[2]/button/span[1]')
        next_pagination_cmt.click()
        sleep(2)
    except NoSuchElementException:
        continue

    while True:
        try:
            Page = driver.find_element(By.ID, "review_list_page_container")
            Person = Page.find_elements(By.CSS_SELECTOR, 'div.c-review-block')
            cm1 = ""
            for p in Person:
                date = p.find_element(By.CSS_SELECTOR, 'span.c-review-block__date')
                name = p.find_element(By.CSS_SELECTOR, 'span.bui-avatar-block__title')
                div = p.find_element(By.CSS_SELECTOR, 'div.bui-grid__column-11')
                cm = div.find_element(By.XPATH, "//h3[@lang='vi']")
                rating = p.find_element(By.CSS_SELECTOR, 'div.bui-review-score__badge')
                c_review = p.find_element(By.CSS_SELECTOR, 'div.c-review')
                c_review_body = c_review.find_elements(By.CSS_SELECTOR, 'span.c-review__body')
                n = 0
                cm2 = ""
                for l1 in c_review_body:
                    if n == 0:
                        cm1 = l1.text
                        n = 1
                    else:
                        cm2 = l1.text
                if cm1 != 'Không có bình luận nào cho đánh giá này':
                    data_comment.append(
                        {'review_title': cm.text, 'review_positive_comments': cm1, 'review_negative_comments': cm2,
                         'rating': rating.text, 'date': date.text, 'name': name.text, 'hotel_url': url_l})
                else:
                    break
            try:
                if cm1 == 'Không có bình luận nào cho đánh giá này':
                    break
                svg_element = driver.find_element(By.CSS_SELECTOR, 'a.pagenext svg')
                svg_element.click()
                sleep(4)
            except NoSuchElementException:
                break
        except ElementNotInteractableException:
            print("Element Not Interactable Exception!")
            break

##lu csv
df = pd.DataFrame(data_comment)
df.to_csv('comment_da_lat_3.csv')



