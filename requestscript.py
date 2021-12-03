import time
import random
from selenium import webdriver

driver = webdriver.Chrome()
driver.get("https://randomus.ru/name?type=101&sex=10&count=10")
list_begin = driver.find_element_by_xpath(".//div[@class=\"field is-grouped is-grouped-multiline\"]")
names = list_begin.text.split("\n")
driver.get("https://randomall.ru/bookname")
books = []
for i in range(10):
    but = driver.find_element_by_xpath(".//button[@class=\"btn btn-custom\"]")
    but.click()
    time.sleep(1)
    books.append(driver.find_element_by_xpath(".//div[@class=\"section result\"]").text)
for book in books:
    query = f"insert into books(author, title, publish_year) values ({random.choice(names)}, {book}, {})"
