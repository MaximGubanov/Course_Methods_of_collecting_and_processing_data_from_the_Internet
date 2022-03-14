from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


s = Service('./chromedriver')
opt = Options()
opt.add_argument('start-maximized')

driver = webdriver.Chrome(service=s, options=opt)
driver.get('https://mail.ru')
"""Пробовал и такие ссылки, но я так понимаю тут тоже всплывающие блоки"""
# driver.get('https://e.mail.ru/login?from=portal')
# driver.get('https://e.mail.ru/login')

wait = WebDriverWait(driver, 30)

"""Это единственный блок кода, который выполняется (нажатие на кнопку 'Войти')"""
btn = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'resplash-btn')))
btn.send_keys(Keys.ENTER)

"""Тут пытался перехватить фрэйм, возможно неправильно, но пробовал разные блоки этого popup выцепить"""
# driver.switch_to.frame(driver.find_element(By.ID, 'login-content'))
# driver.switch_to.frame('iframe')

"""Далее всплывает модальное окно и не могу найти не один элемент в нем, делал с ожиданием и без, и time.sleep тоже...
selenium.common.exceptions.NoSuchElementException: Message: no such element: Unable to locate element: {"method":"css 
selector","selector":"[id="login-content"]"}, либо лювлю таймаут"""
input_login = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'input-0-2-71')))
input_login.send_keys('study.ai_172@mail.ru')

btn_login = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'base-0-2-79 primary-0-2-93')))
btn_login.click()