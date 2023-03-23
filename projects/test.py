from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd
import time

# selenium 라이브러리 이용하여 브라우저 제어

# 브라우저 옵션 설정
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)

# 웹페이지 해당 주소 이동
driver.get("https://www.naver.com")
driver.implicitly_wait(2)

# 검색어 입력
driver.find_element(By.CSS_SELECTOR,'#query').send_keys("삼쩜삼")
time.sleep(1)
#검색 버튼 클릭
driver.find_element(By.CSS_SELECTOR, '#search_btn').send_keys(Keys.ENTER)
time.sleep(1)
# 뉴스탭 이동
driver.find_element(By.CSS_SELECTOR, '#lnb > div.lnb_group > div > ul > li:nth-child(3) > a').send_keys(Keys.ENTER)
time.sleep(1)
# 뉴스 최신순으로 정렬
driver.find_element(By.CSS_SELECTOR, '#snb > div.api_group_option_filter._search_option_simple_wrap > div > div.option_area.type_sort > a:nth-child(2)').send_keys(Keys.ENTER)


# BeautifulSoup 라이브러리를 이용하여 뉴스 기사 크롤링
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

articles = soup.select('#main_pack > section.sc_new.sp_nnews._prs_nws > div > div.group_news > ul > li')
results = []
# 첫번째 페이지 뉴스 크롤링
for article in articles:
    title = article.select_one('div > div.news_area > a').text
    date = article.select_one('div > div > div.news_info > div.info_group > span').text
    href = article.select_one('div > div.news_area > a')['href']
    print(title, date, href)
    temp = []
    temp.append(title)
    temp.append(date)
    temp.append(href)
    results.append(temp)

# 2번째 페이지로 이동 후 뉴스 크롤링
driver.find_element(By.CSS_SELECTOR, '#main_pack > div.api_sc_page_wrap > div > div > a:nth-child(2)').send_keys(Keys.ENTER)
time.sleep(1)

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

articles = soup.select('#main_pack > section.sc_new.sp_nnews._prs_nws > div > div.group_news > ul > li')
for article in articles:
    title = article.select_one('div > div.news_area > a').text
    date = article.select_one('div > div > div.news_info > div.info_group > span').text
    href = article.select_one('div > div.news_area > a')['href']
    print(title, date, href)
    temp = []
    temp.append(title)
    temp.append(date)
    temp.append(href)
    results.append(temp)

# pandas 라이브러리 이용하여 데이터 csv 파일 만들기
data = pd.DataFrame(results)
data.columns = ['제목', '날짜', 'url']
print(data.head())
data.to_csv('result.csv', encoding='cp949')





