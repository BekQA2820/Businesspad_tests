import pytest
from selenium import webdriver
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure
import time
import random
# Функция для создания скриншота в Allure
def attach_screenshot(driver, name):
    allure.attach(driver.get_screenshot_as_png(),
                  name=name,
                  attachment_type=allure.attachment_type.PNG)

# Фикстура для инициализации и завершения работы драйвера
@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()
def test_start(driver):
    wait = WebDriverWait(driver, 20)
    # Шаг 1: Авторизация
    with allure.step("Открываем сайт и логинимся"):
        try:
            driver.get("https://dev.business-pad.com/")
        # Вход в систему
            driver.find_element(By.XPATH, '//*[@id=":r0:"]').send_keys("adminbp")
            driver.find_element(By.XPATH, '//*[@id=":r1:"]').send_keys("") # вставь пароль
            driver.find_element(By.XPATH, '//*[@id="root"]/div/main/div/div/div/div[2]/div/form/div/div[4]').click()
            time.sleep(2)
            driver.get("https://dev.business-pad.com/bp-settings/92")
        except Exception as e:
            pytest.fail(f"Ошибка авторизации: {str(e)}")
    # Шаг 2: Переход в настройки
    with allure.step("Переходим на страницу настроек и получаем data-id"):
        try:
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//p[contains(text(), "Закрытие сделки")]'))
            )
            element.click()
            # Получаем data-id
            parent_div = driver.find_element(By.XPATH, '//p[contains(text(), "Закрытие сделки")]/ancestor::div[@data-id]')
            data_id1 = parent_div.get_attribute('data-id')
            print(f"Найденный data-id: {data_id1}")
            allure.attach(f"Полученный data-id: {data_id1}", name="Data ID Info")
            attach_screenshot(driver, "После получения data-id")
        except Exception as e:
            pytest.fail(f"Ошибка при работе со страницей настроек: {str(e)}")


    time.sleep(10)