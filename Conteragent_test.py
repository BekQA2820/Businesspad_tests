import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time

# Фикстура для запуска и закрытия браузера
@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")  # Запуск в развернутом окне
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()


def test_login_and_open_menu(driver):
    # 1. Открываем сайт
    driver.get("https://team.business-pad.com/")

    # 2. Ввод логина
    username_input = driver.find_element(By.XPATH, '//*[@id=":r0:"]')
    username_input.send_keys("K.Bekir")

    # 3. Ввод пароля
    password_input = driver.find_element(By.XPATH, '//*[@id=":r1:"]')
    password_input.send_keys("Team.Bekir")

    # 4. Нажимаем кнопку Войти
    login_button = driver.find_element(By.XPATH, '//*[@id="root"]/div/main/div/div/div/div[2]/div/form/div/div[4]')
    login_button.click()
    time.sleep(7)




    # 6. Нажимаем кнопку "Меню" (замени XPATH)
    #menu_button = driver.find_element(By.XPATH, "XPATH_КНОПКИ_МЕНЮ")
    #menu_button.click()

    # 7. Проверяем, что меню открылось (можно проверить, например, заголовок меню)
    #assert "НазваниеМеню" in driver.page_source