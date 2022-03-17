from pprint import pprint

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions


s = Service('./chromedriver')
opt = Options()
opt.add_argument('start-maximized')

driver = webdriver.Chrome(service=s, options=opt)
driver.get('https://tass.ru/')

next_btn = True
arrow_down = 0
while next_btn and arrow_down < 200:
    try:
        wait = WebDriverWait(driver, 30)
        btn_more = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='news-feed-column news-feed-column_opened']//a")))
        btn_more.send_keys(Keys.ARROW_DOWN)
        arrow_down += 1
        continue
    except exceptions.ElementNotInteractableException:
        next_btn = False
    break

all_news = driver.find_elements(By.XPATH, "//div[@class='news-feed-column news-feed-column_opened']//a[contains(@class, 'news-feed-item')]")
news_list = []

for num, news in enumerate(all_news, 1):
    data = news.text.split('\n')
    time = data[0].split(' ')[0]
    header = data[1]
    news = dict(id=num, name=header, time_at=time)
    news_list.append(news)

pprint(news_list)