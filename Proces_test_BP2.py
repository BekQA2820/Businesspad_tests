import pytest
from selenium import webdriver
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure
import time


# Функция для создания скриншота в Allure
def attach_screenshot(driver, name):
    allure.attach(driver.get_screenshot_as_png(), name=name, attachment_type=allure.attachment_type.PNG)


# Фикстура для инициализации и завершения работы драйвера
@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()


def test_start(driver):
    wait = WebDriverWait(driver, 20)  # Инициализация WebDriverWait
    with allure.step("Открываем сайт и логинимся"):
        driver.get("https://finance.business-pad.com/")
        # Вход в систему
        driver.find_element(By.XPATH, '//*[@id=":r0:"]').send_keys("adminbp")
        driver.find_element(By.XPATH, '//*[@id=":r1:"]').send_keys("") # вставь пароль
        driver.find_element(By.XPATH, '//*[@id="root"]/div/main/div/div/div/form/div/button').click()


        try:
            # настройки
            settings_icon = wait.until(EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="root"]/div/div[1]/div/div/div[6]/div/button')
            ))
            settings_icon.click()
        except Exception as e:
            print(f"Ошибка при клике на иконку настроек: {e}")
            raise
        try:
            # список
            element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="main"]/div[2]/div/div[2]/div[1]/div/div/div[2]/a[1]'))
            )
            element.click()
            print("Успешный клик по элементу")
        except Exception as e:
            print(f"Ошибка при клике: {str(e)}")
            raise
        try:
            # Клик по +
            button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="main"]/div[2]/div/div[1]/div[1]/button'))
            )
            button.click()
            print("Клик выполнен успешно")
        except Exception as e:
            print(f"Ошибка: {str(e)}")
            raise
        try:
            # 1. Клик Названию
            tab_element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/main/div[2]/div[2]/div[1]/div/div/button[2]'))
            )
            tab_element.click()
            print("Клик по вкладке выполнен")
            # 2. Клик по полю ввода
            input_field = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//input[@placeholder="Введите название процесса"]'))
            )
            input_field.click()
            print("Клик по полю ввода выполнен")
            # 3. Очистка поля и ввод текста
            input_field.send_keys(Keys.CONTROL + 'a')
            input_field.send_keys(Keys.DELETE)
            input_field.send_keys("Автотест")
            print("Текст 'Автотест' введен")

        except Exception as e:
            print(f"Произошла ошибка: {str(e)}")
            raise
        try:
            # 1. выбор тестировщика
            menu_trigger = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH,
                                            '/html/body/div/div/main/div[2]/div[2]/div[3]/div/div[2]/div/div[1]/div/div[3]/div/div[1]/div/div/div/div/div'))
            )
            ActionChains(driver).move_to_element(menu_trigger).click().perform()
            print("Клик по меню выполнен")

            # 2. Ожидание появления всплывающего меню и поиск "Тестировщик"
            tester_element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[contains(text(), "Тестировщик")]'))
            )
            tester_element.click()
            print("Клик по 'Тестировщик' выполнен")
        except Exception as e:
            print(f"Произошла ошибка: {str(e)}")
            # Сделать скриншот при ошибке

            raise
        try:
            # Ожидание и клик по кнопке Сохранить
            button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/main/div[5]/div/button[1]'))
)
            button.click()
            print("Клик по кнопке выполнен успешно")
        except Exception as e:
            print(f"Ошибка при клике: {str(e)}")
            raise
        #Переход обратно на полотно и создаем основной процесс
        try:
            # 1. Находим и кликаем по элементу
            drag_element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/main/div[2]/div[2]/div[1]/div/div/button[1]'))
            )
            ActionChains(driver).click(drag_element).perform()
            print("Элемент найден и активирован")

            # 2. Находим draggable элемент (по классу и атрибуту draggable)
            draggable_item = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//div[@draggable="true" and contains(@class, "MuiGrid2-container")]'))
            )

            # 3. Выполняем drag-and-drop с перемещением на 200px вправо
            print("Начинаем перемещение элемента...")

            # Для headless-режима используем JavaScript + ActionChains
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", draggable_item)
            time.sleep(0.5)

            # Определяем начальные координаты
            start_x = draggable_item.location['x']
            start_y = draggable_item.location['y']
            offset = 200  # пикселей для перемещения

            # Вариант 1: Через ActionChains (может не работать в headless)
            ActionChains(driver) \
                .move_to_element(draggable_item) \
                .pause(0.5) \
                .click_and_hold() \
                .pause(0.5) \
                .move_by_offset(offset, 0) \
                .pause(0.5) \
                .release() \
                .perform()

            print("Перемещение выполнено через ActionChains")

            # Вариант 2: Через JavaScript (более надежно в headless)
            driver.execute_script("""
                var element = arguments[0];
                var offset = arguments[1];
                var rect = element.getBoundingClientRect();
                var startX = rect.left + rect.width / 2;
                var startY = rect.top + rect.height / 2;

                // Создаем события drag
                var dragStart = new DragEvent('dragstart', {
                    clientX: startX,
                    clientY: startY,
                    bubbles: true
                });
                element.dispatchEvent(dragStart);

                // Создаем события dragend с перемещением
                var dragEnd = new DragEvent('dragend', {
                    clientX: startX + offset,
                    clientY: startY,
                    bubbles: true
                });
                element.dispatchEvent(dragEnd);
            """, draggable_item, offset)

            print("Перемещение выполнено через JavaScript")

            # Пауза для визуальной проверки (в реальном тесте можно уменьшить)
            time.sleep(2)

        except Exception as e:
            print(f"Ошибка при выполнении drag-and-drop: {str(e)}")
            # Сделать скриншот для отладки

            raise
        #ПОЛОТНО!!!!!!!!!!!!!!!!!!!!!
        try:

            # 1. Находим и кликаем по элементу
            drag_element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/main/div[2]/div[2]/div[1]/div/div/button[1]'))
            )
            ActionChains(driver).click(drag_element).perform()
            print("Элемент найден и активирован")

            # 2. Находим draggable элемент (по классу и атрибуту draggable)
            draggable_item = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//div[@draggable="true" and contains(@class, "MuiGrid2-container")]'))
            )

            # 3. Выполняем drag-and-drop с перемещением на 200px вправо
            print("Начинаем перемещение элемента...")

            # Для headless-режима используем JavaScript + ActionChains
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", draggable_item)
            time.sleep(0.5)

            # Определяем начальные координаты
            start_x = draggable_item.location['x']
            start_y = draggable_item.location['y']
            offset = 200  # пикселей для перемещения

            # Вариант 1: Через ActionChains (может не работать в headless)
            ActionChains(driver) \
                .move_to_element(draggable_item) \
                .pause(0.5) \
                .click_and_hold() \
                .pause(0.5) \
                .move_by_offset(offset, 0) \
                .pause(0.5) \
                .release() \
                .perform()

            print("Перемещение выполнено через ActionChains")

            # Вариант 2: Через JavaScript (более надежно в headless)
            driver.execute_script("""
                var element = arguments[0];
                var offset = arguments[1];
                var rect = element.getBoundingClientRect();
                var startX = rect.left + rect.width / 2;
                var startY = rect.top + rect.height / 2;

                // Создаем события drag
                var dragStart = new DragEvent('dragstart', {
                    clientX: startX,
                    clientY: startY,
                    bubbles: true
                });
                element.dispatchEvent(dragStart);

                // Создаем события dragend с перемещением
                var dragEnd = new DragEvent('dragend', {
                    clientX: startX + offset,
                    clientY: startY,
                    bubbles: true
                });
                element.dispatchEvent(dragEnd);
            """, draggable_item, offset)

            print("Перемещение выполнено через JavaScript")

            # Пауза для визуальной проверки (в реальном тесте можно уменьшить)
            time.sleep(2)

        except Exception as e:
            print(f"Ошибка при выполнении drag-and-drop: {str(e)}")
            # Сделать скриншот для отладки

            raise