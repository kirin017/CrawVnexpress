import requests
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import pandas as pd
from tqdm import tqdm

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
# Khởi tạo driver
driver = webdriver.Chrome(executable_path="chromedriver_win32/chromedriver.exe", options=chrome_options)
driver.get("https://vnexpress.net/")

# Khai báo một danh sách lưu trữ dữ liệu thu thập được
data = []

soup = BeautifulSoup(driver.page_source, 'html.parser')
links = []
for link in soup.find_all('a'):
    href = link.get('href')
    if href.startswith('https://vnexpress.net/') and href.endswith('.html'):
        links.append(href)
# Lặp qua từng bài viết
for link in links:
    driver.get(link)
    soup_page = BeautifulSoup(driver.page_source, 'html.parser')
    # Lấy tiêu đề của bài viết
    if soup_page.find('h1', "title-detail") != None:
        continue
    title = soup_page.find('h1', "title-detail").text
    content = driver.find_element_by_class_name("fck_detail").text
    # Lấy comment
    comments = soup.find_all('div', "content-comment")
    comment_list = []
    for comment in comments:
        text = comment.find_element_by_class_name("full_content").text
        # Lấy tên của người đăng bình luận
        user = comment.find_element_by_class_name("txt-name").text
        # Lấy thời gian đăng bình luận
        time = comment.find_element_by_class_name("time-com").text
        # Lưu thông tin bình luận vào danh sách
        comment_list.append({"user": user, "time": time, "text": text})
        # Lưu thông tin của bài viết và bình luận vào danh sách
        data.append({"title": title, "content": content, "comments": comment_list})
        # Quay trở lại trang chủ
        driver.quit()
print(data)
df = pd.DataFrame(data)

# Xuất dữ liệu thành file CSV
df.to_csv("vnexpress_data.csv", index=False)
print("hello")