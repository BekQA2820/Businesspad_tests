import pytest
from selenium import webdriver
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure
import time
# Сделай уже функции для повторного кода, че ты как дурак !!!!

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
            # Ожидаем и кликаем по иконке Нстроек
            time.sleep(1)
            settings_icon = wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, '[aria-label="Настройки"]')))
            driver.execute_script("""
                arguments[0].style.opacity = '1';
                arguments[0].style.visibility = 'visible';
                arguments[0].style.pointerEvents = 'auto';
            """, settings_icon)
            ActionChains(driver) \
                .move_to_element(settings_icon) \
                .pause(0.1) \
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
                .pause(0.1) \
                .click() \
                .pause(0.1) \
                .click() \
                .perform()
            attach_screenshot(driver, "После клика по списку Оргструктуре")
    except Exception as e:
        attach_screenshot(driver, "Ошибка при выполнении действий")
        pytest.fail(f"Ошибка при выполнении: {str(e)}")
    # Клик по трем точкам и выбор черновика
    with allure.step("Кликнуть по кнопке меню (три точки)"):
        menu_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button.MuiButtonBase-root.MuiButton-root.MuiButton-textPrimary.css-1mut0en")))
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
    # Клик по трем точкам руководителя и добавление 2х отделов!!!!!!!!!!!!!!!!!!
    with allure.step("Кликнуть по кнопке меню (три точки) руководителя"):
        menu_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.css-1kg133f")))
        menu_button.click()
        allure.attach(driver.get_screenshot_as_png(), name="menu_clicked",
                      attachment_type=allure.attachment_type.PNG)
    with allure.step("Добавление отделов"):
        draft_option = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//li[contains(., 'Добавить отдел в подчинение')]"))
        )
        draft_option.click()
        allure.attach(driver.get_screenshot_as_png(), name="draft_selected",
                      attachment_type=allure.attachment_type.PNG)
    with allure.step("Кликнуть по кнопке меню (три точки) руководителя 2"):
        time.sleep(0.8)
        menu_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.css-1kg133f")))
        menu_button.click()
        allure.attach(driver.get_screenshot_as_png(), name="menu_clicked",
                      attachment_type=allure.attachment_type.PNG)
    with allure.step("Добавление отделов 2"):
        draft_option = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//li[contains(., 'Добавить отдел в подчинение')]"))
        )
        draft_option.click()
        allure.attach(driver.get_screenshot_as_png(), name="draft_selected",
                      attachment_type=allure.attachment_type.PNG)
        # ПОДОТДЕЛЫ 1
    with allure.step("Добавление отделов подотдела"):
        time.sleep(0.5)
        buttons = driver.find_elements(By.CSS_SELECTOR, 'button.css-1kg133f')
        # клик по второй кнопке (индекс 1)
        buttons[1].click()
        allure.attach(driver.get_screenshot_as_png(), name="draft_selected",
                      attachment_type=allure.attachment_type.PNG)
        element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (
                By.XPATH, "//li[contains(@class, 'MuiMenuItem-root') and contains(., 'Добавить отдел в подчинение')]")))
        element.click()
        # Второй раз
        time.sleep(0.5)
        buttons = driver.find_elements(By.CSS_SELECTOR, 'button.css-1kg133f')
        # клик по второй кнопке (индекс 1)
        buttons[1].click()
        allure.attach(driver.get_screenshot_as_png(), name="draft_selected",
                      attachment_type=allure.attachment_type.PNG)
        element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (
                By.XPATH, "//li[contains(@class, 'MuiMenuItem-root') and contains(., 'Добавить отдел в подчинение')]")))
        element.click()
        # ПОДОТДЕЛЫ 2
    with allure.step("Добавление отделов подотдела"):
        time.sleep(0.5)
        buttons = driver.find_elements(By.CSS_SELECTOR, 'button.css-1kg133f')
        # клик по второй кнопке (индекс 1)
        buttons[2].click()
        allure.attach(driver.get_screenshot_as_png(), name="draft_selected",
                      attachment_type=allure.attachment_type.PNG)
        element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (
                By.XPATH, "//li[contains(@class, 'MuiMenuItem-root') and contains(., 'Добавить отдел в подчинение')]")))
        element.click()
    # редактирование!!!!!!!!!!!!!!!!!!!!!!!!!!!
    #Подраздел2!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    with allure.step("Редактирование"):
        pane = driver.find_element(By.CSS_SELECTOR, "div.react-flow__pane")
        ActionChains(driver).move_to_element_with_offset(pane, 100, 100).click().perform()
        buttons = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located(((By.CSS_SELECTOR, 'button.css-1kg133f'))))
        # клик по второй кнопке (индекс 1)
        buttons[2].click()
        allure.attach(driver.get_screenshot_as_png(), name="draft_selected",
                      attachment_type=allure.attachment_type.PNG)
        element = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//li[contains(@class, 'MuiMenuItem-root') and contains(., 'Редактировать')]")))
        element.click()
        element1 = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.MuiAccordionSummary-root")))  # Клик по общему меню
        element1.click()
    with allure.step("Очистить поле 'Название отдела' и ввести 'Подраздел 2'"):
        input_field = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='name']")))
    # Кликаем, выделяем текст и удаляем
    input_field.click()
    input_field.send_keys(Keys.CONTROL + "a")  # Выделить всё (Windows/Linux)
    input_field.send_keys(Keys.DELETE)  # Удалить
    # Вводим новый текст
    input_field.send_keys("Подраздел 2")
    input_field.send_keys(Keys.ENTER)
    # Скриншот для отчета
    allure.attach(
        driver.get_screenshot_as_png(),
        name="field_edited",
        attachment_type=allure.attachment_type.PNG)

    with allure.step("Кликнуть на 'Участники'"):
        with allure.step("Редактирование"):
            buttons = WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'button.css-1kg133f')))
        # клик по второй кнопке (индекс 1)
        buttons[2].click()
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
    button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Добавить')]")))
    button.click()
    with allure.step("Выбираем из сотрудников Юлию"):
        checkbox = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.XPATH, '//p[contains(text(), "Плюхина")]/..//input')
            )
        )
    driver.execute_script("arguments[0].click();", checkbox)
    with allure.step("Клик по последней кнопке 'Подтвердить'"):
        confirm_buttons = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//button[contains(., 'Подтвердить')]"))
        )
    # Дополнительно проверяем, что последняя кнопка кликабельна
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(confirm_buttons[-1])
    ).click()
    #Подраздел1!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    with allure.step("Редактирование"):
        time.sleep(1)
        pane = driver.find_element(By.CSS_SELECTOR, "div.react-flow__pane")
        ActionChains(driver).move_to_element_with_offset(pane, 110, 100).click().perform()
        buttons = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'button.css-1kg133f')))
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(buttons[1])
        ).click()
        allure.attach(driver.get_screenshot_as_png(), name="draft_selected",
                      attachment_type=allure.attachment_type.PNG)
        element = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//li[contains(@class, 'MuiMenuItem-root') and contains(., 'Редактировать')]")))
        element.click()
        element1 = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.MuiAccordionSummary-root")))  # Клик по общему меню
        element1.click()
    with allure.step("Очистить поле 'Название отдела' и ввести 'Подраздел 2'"):
        input_field = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='name']")))
    # Кликаем, выделяем текст и удаляем
    input_field.click()
    input_field.send_keys(Keys.CONTROL + "a")  # Выделить всё (Windows/Linux)
    input_field.send_keys(Keys.DELETE)  # Удалить
    # Вводим новый текст
    input_field.send_keys("Подраздел 1")
    input_field.send_keys(Keys.ENTER)
    # Скриншот для отчета
    allure.attach(
        driver.get_screenshot_as_png(),
        name="field_edited",
        attachment_type=allure.attachment_type.PNG)

    with allure.step("Кликнуть на'Участники' "):
        with allure.step("Редактирование"):
            buttons = WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'button.css-1kg133f')))
        # клик по второй кнопке (индекс 1)
        buttons[1].click()
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
    button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Добавить')]")))
    button.click()
    #Добавляем
    with allure.step("Виктор"):
        checkbox = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.XPATH, '//p[contains(text(), "Victor")]/..//input')
            )
        )
    driver.execute_script("arguments[0].click();", checkbox)
    with allure.step("Дария"):
        checkbox = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.XPATH, '//p[contains(text(), "Daria")]/..//input')
            )
        )
    driver.execute_script("arguments[0].click();", checkbox)
    with allure.step("Сергей"):
        checkbox = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.XPATH, '//p[contains(text(), "Понарин")]/..//input')
            )
        )
    with allure.step("Клик по последней кнопке 'Подтвердить'"):   # ПОДТВЕРЖДАЕМ
        confirm_buttons = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//button[contains(., 'Подтвердить')]")))
    # Дополнительно проверяем, что последняя кнопка кликабельна
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(confirm_buttons[-1])
    ).click()
    #Подраздел3!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    with allure.step("Редактирование"):
        ActionChains(driver).send_keys(Keys.ENTER).perform()
        pane = driver.find_element(By.CSS_SELECTOR, "div.react-flow__pane")
        ActionChains(driver).move_to_element_with_offset(pane, 100, 100).click().perform()
        buttons = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located(((By.CSS_SELECTOR, 'button.css-1kg133f'))))
        # клик по кнопке (индекс 3)
        buttons[3].click()
        allure.attach(driver.get_screenshot_as_png(), name="draft_selected",
                      attachment_type=allure.attachment_type.PNG)
        element = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//li[contains(@class, 'MuiMenuItem-root') and contains(., 'Редактировать')]")))
        element.click()
        element1 = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.MuiAccordionSummary-root")))  # Клик по общему меню
        element1.click()
    with allure.step("Очистить поле 'Название отдела' и ввести 'Подраздел 3'"):
        input_field = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='name']")))
    # Кликаем, выделяем текст и удаляем
    input_field.click()
    input_field.send_keys(Keys.CONTROL + "a")  # Выделить всё (Windows/Linux)
    input_field.send_keys(Keys.DELETE)  # Удалить
    # Вводим новый текст
    input_field.send_keys("Подраздел 3")
    input_field.send_keys(Keys.ENTER)
    # Скриншот для отчета
    allure.attach(
        driver.get_screenshot_as_png(),
        name="field_edited",
        attachment_type=allure.attachment_type.PNG)

    with allure.step("Кликнуть на 'Участники' "):
        with allure.step("Редактирование"):
            ActionChains(driver).send_keys(Keys.ENTER).perform()
            buttons = WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'button.css-1kg133f')))
        # клик по кнопке (индекс 3)
        buttons[3].click()
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
    button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Добавить')]")))
    button.click()
    with allure.step("Беатрис"):
        checkbox = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.XPATH, '//p[contains(text(), "Беатрис")]/..//input')
            )
        )
    driver.execute_script("arguments[0].click();", checkbox)
    with allure.step("Клик по последней кнопке 'Подтвердить'"):
        confirm_buttons = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//button[contains(., 'Подтвердить')]"))
        )
    # Дополнительно проверяем, что последняя кнопка кликабельна
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(confirm_buttons[-1])
    ).click()
    #Подраздел4 УДАЛЕНИЕ!!!!!!!!!!!
    with allure.step("Кликнуть на 'Участники' "):
        with allure.step("Редактирование"):
            ActionChains(driver).send_keys(Keys.ENTER).perform()
            pane = driver.find_element(By.CSS_SELECTOR, "div.react-flow__pane")
            ActionChains(driver).move_to_element_with_offset(pane, 100, 100).click().perform()
            buttons = WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'button.css-1kg133f')))
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(buttons[4])
            ).click()
        allure.attach(driver.get_screenshot_as_png(), name="draft_selected",
                      attachment_type=allure.attachment_type.PNG)
        element = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//li[contains(@class, 'MuiMenuItem-root') and contains(., 'Удалить')]")))
        element.click()
        with allure.step("Клик по последней кнопке 'Подтвердить'"):
            confirm_buttons = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, "//button[contains(., 'Подтвердить')]"))
            )
    # Дополнительно проверяем, что последняя кнопка кликабельна
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(confirm_buttons[-1])
    ).click()
    #Назначить Руководителя!!!!!!!!!!!!!!!
    with allure.step("Редактирование"):
        time.sleep(0.5)
        pane = driver.find_element(By.CSS_SELECTOR, "div.react-flow__pane")
        ActionChains(driver).move_to_element_with_offset(pane, 100, 100).click().perform()
        buttons = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located(((By.CSS_SELECTOR, 'button.css-1kg133f'))))
        # клик по второй кнопке (индекс 1)
        buttons[3].click()
        allure.attach(driver.get_screenshot_as_png(), name="draft_selected",
                      attachment_type=allure.attachment_type.PNG)
        element = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//li[contains(@class, 'MuiMenuItem-root') and contains(., 'Редактировать')]")))
        element.click()
        element1 = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.MuiAccordionSummary-root")))  # Клик по общему меню
        element1.click()
        element1 = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.MuiAccordionSummary-root")))  # Клик по общему меню
        element1.click()
        element = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//h6[contains(., 'Участники')]")))
    element.click()
    button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Назначить')]")))
    button.click()
    with allure.step("Андрей руководитель"):
        checkbox = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.XPATH, '//p[contains(text(), "Андрей")]/..//input')
            )
        )
    driver.execute_script("arguments[0].click();", checkbox)
    with allure.step("Клик по последней кнопке 'Подтвердить'"):
        confirm_buttons = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//button[contains(., 'Подтвердить')]"))
        )
    # Дополнительно проверяем, что последняя кнопка кликабельна
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(confirm_buttons[-1])
    ).click()

    #Переименовывание подраздела 5!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    with allure.step("Редактирование"):
        pane = driver.find_element(By.CSS_SELECTOR, "div.react-flow__pane")
        ActionChains(driver).move_to_element_with_offset(pane, 100, 100).click().perform()
        buttons = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located(((By.CSS_SELECTOR, 'button.css-1kg133f'))))
        # клик по второй кнопке (индекс 4)
        buttons[4].click()
        allure.attach(driver.get_screenshot_as_png(), name="draft_selected",
                      attachment_type=allure.attachment_type.PNG)
        element = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//li[contains(@class, 'MuiMenuItem-root') and contains(., 'Редактировать')]")))
        element.click()
        element1 = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.MuiAccordionSummary-root")))  # Клик по общему меню
        element1.click()
    with allure.step("Очистить поле 'Название отдела' и ввести 'Подраздел 4'"):
        input_field = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='name']")))
    # Кликаем, выделяем текст и удаляем
    input_field.click()
    input_field.send_keys(Keys.CONTROL + "a")  # Выделить всё (Windows/Linux)
    input_field.send_keys(Keys.DELETE)  # Удалить
    # Вводим новый текст
    input_field.send_keys("Подраздел 4")
    input_field.send_keys(Keys.ENTER)
    # Скриншот для отчета
    allure.attach(
        driver.get_screenshot_as_png(),
        name="field_edited",
        attachment_type=allure.attachment_type.PNG)
    #Добавим сотрудников в отдел руководителя
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
            button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Добавить')]")))
            button.click()
            print("Нажата кнопка 'Добавить'")
        except:
            button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Изменить')]")))
            button.click()
            print("Кнопка 'Добавить' не найдена, нажата 'Изменить'")
    with allure.step("Вадим"):
        checkbox = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.XPATH, '//p[contains(text(), "Vadim")]/..//input')
            )
        )
    driver.execute_script("arguments[0].click();", checkbox)
    with allure.step("Руслан"):
        checkbox = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.XPATH, '//p[contains(text(), "Руслан")]/..//input')
            )
        )
    driver.execute_script("arguments[0].click();", checkbox)
    #Подтверждаем
    with allure.step("Клик по последней кнопке 'Подтвердить'"):
        confirm_buttons = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//button[contains(., 'Подтвердить')]")))
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(confirm_buttons[-1])).click()
    #Отдаление$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    with allure.step("Отдалить"):
        element = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//button[.//*[contains(@d, "M18 13H6")]]'))
        )
    ActionChains(driver).move_to_element(element).click().perform()
    ActionChains(driver).move_to_element(element).click().perform()
    ActionChains(driver).move_to_element(element).click().perform()
    ActionChains(driver).move_to_element(element).click().perform()
    ActionChains(driver).move_to_element(element).click().perform()
    ActionChains(driver).move_to_element(element).click().perform()
    allure.attach(driver.get_screenshot_as_png(), name="zoom_out",
                  attachment_type=allure.attachment_type.PNG)
    with allure.step("Приблизить"):
        draft_option = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.MuiButtonBase-root[type="button"] svg[data-testid="SettingsOverscanRoundedIcon"]'))
        )
        draft_option.click()
        allure.attach(driver.get_screenshot_as_png(), name="zoom_button",
                      attachment_type=allure.attachment_type.PNG)
    #Опубликовываем
    with allure.step("Кликнуть по кнопке меню (три точки)"):
        menu_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button.MuiButtonBase-root.MuiButton-root.MuiButton-textPrimary.css-1mut0en")))
        menu_button.click()
        allure.attach(driver.get_screenshot_as_png(), name="menu_clicked",
                      attachment_type=allure.attachment_type.PNG)
    with allure.step("Выбрать 'Опубликовать'"):
        draft_option = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//li[contains(., 'Опубликовать')]"))
        )
        draft_option.click()
        public_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Подтвердить")]'))
        )
        public_button.click()
        allure.attach(driver.get_screenshot_as_png(), name="draft_selected",
                      attachment_type=allure.attachment_type.PNG)

