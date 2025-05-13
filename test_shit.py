import pytest
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC, wait
import random
import time
import allure


# открываем браузер
@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()


def test_add_and_edit_counteragent(driver):
    # Открываем основной сайт
    driver.get("https://team.business-pad.com/")

    # Открываем генератор ИНН в новой вкладке
    driver.execute_script("window.open('https://randvar.ru/generator/personal/inn', '_blank');")
    driver.switch_to.window(driver.window_handles[1])

    # Ждем, пока элемент с ИНН станет кликабельным и кликаем по нему
    inn_element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "div.result-item[role='button']"))
    )
    inn_element.click()

    # Получаем значение ИНН из элемента
    inn_value = inn_element.text

    # Закрываем вкладку с генератором ИНН и возвращаемся обратно
    driver.close()
    driver.switch_to.window(driver.window_handles[0])

    # Теперь можно использовать inn_value для дальнейших действий
    print(f"Сгенерированный ИНН: {inn_value}")