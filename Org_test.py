import pytest
from selenium import webdriver
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure
import time
def attach_screenshot(driver, name):
    allure.attach(driver.get_screenshot_as_png(), name=name, attachment_type=allure.attachment_type.PNG)
@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

def test_process_flow(driver):
    wait = WebDriverWait(driver, 20)
    with allure.step("1. Авторизация"):
        driver.get("https://finance.business-pad.com/")
        driver.find_element(By.ID, ":r0:").send_keys("adminbp")
        driver.find_element(By.ID, ":r1:").send_keys("AtVFpd3hFeEc" + Keys.RETURN)
        attach_screenshot(driver, "После логина")
        time.sleep(1)
    try:
        with allure.step("Клик по иконке настроек"):
            # Ожидаем и кликаем по иконке Settings
            settings_icon = wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, '[aria-label="Настройки"]')))
            # Делаем элемент полностью видимым через JS
            driver.execute_script("""
                arguments[0].style.opacity = '1';
                arguments[0].style.visibility = 'visible';
                arguments[0].style.pointerEvents = 'auto';
            """, settings_icon)
            # Кликаем через ActionChains
            ActionChains(driver) \
                .move_to_element(settings_icon) \
                .pause(0.3) \
                .click() \
                .perform()
            attach_screenshot(driver, "После клика по иконке настроек")
        with allure.step("Клик по 'Оргструктуре'"):
            # Ожидаем и кликаем по тексту
            bp_list = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//a[contains(@class, 'MuiLink-root')]//div[contains(text(), 'Оргструктура')]")))
            # Двойной клик для надежности
            ActionChains(driver) \
                .move_to_element(bp_list) \
                .pause(0.2) \
                .click() \
                .pause(0.1) \
                .click() \
                .perform()
            attach_screenshot(driver, "После клика по списку Оргструктуре")
    except Exception as e:
        attach_screenshot(driver, "Ошибка при выполнении действий")
        print(f"Ошибка при выполнении: {str(e)}")
    #Клик по трем точкам и выбор черновика
    with allure.step("Кликнуть по кнопке меню (три точки)"):
        menu_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.MuiButtonBase-root.MuiButton-root.MuiButton-textPrimary.css-1mut0en")))
        menu_button.click()
        allure.attach(driver.get_screenshot_as_png(), name="menu_clicked",
                      attachment_type=allure.attachment_type.PNG)
    with allure.step("Выбрать 'Перейти к черновику'"):
        draft_option = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//li[contains(., 'Перейти к черновику')]"))
        )
        draft_option.click()
        allure.attach(driver.get_screenshot_as_png(), name="draft_selected",
                      attachment_type=allure.attachment_type.PNG)
#редактирование
    #Отдаление$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    with allure.step("Добавим сотрудников в отдел руководителя"):
        with allure.step("Редактирование"):
            buttons = WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'button.css-1kg133f')))
        # клик по второй кнопке (индекс 1)
        buttons[0].click()
        allure.attach(driver.get_screenshot_as_png(), name="draft_selected",
                      attachment_type=allure.attachment_type.PNG)
        element = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//li[contains(@class, 'MuiMenuItem-root') and contains(., 'Редактировать')]")))
        element.click()
        element1 = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.MuiAccordionSummary-root")))  # Клик по общему меню
        element1.click()
        element = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//h6[contains(., 'Участники')]")))
    element.click()
    with allure.step("Пробуем нажать 'Добавить' или 'Изменить'"):
        try:
            button = WebDriverWait(driver, 7).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Добавить')]")))
            button.click()
            print("Нажата кнопка 'Добавить'")
        except:
            button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Изменить')]")))
            button.click()
            print("Кнопка 'Добавить' не найдена, нажата 'Изменить'")
    time.sleep(5)
