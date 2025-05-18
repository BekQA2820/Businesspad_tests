import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import allure
from selenium.webdriver import Keys, ActionChains

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
        driver.get("https://team.business-pad.com/")
        # Вход в систему
        driver.find_element(By.XPATH, '//*[@id=":r0:"]').send_keys("K.Bekir")
        driver.find_element(By.XPATH, '//*[@id=":r1:"]').send_keys("") # вставь пароль
        driver.find_element(By.XPATH, '//*[@id="root"]/div/main/div/div/div/div[2]/div/form/div/div[4]').click()
        attach_screenshot(driver, "После логина")

    with allure.step("Переход на вкладку 'Процессы'"):
        try:
            # Ожидание, пока элемент не станет кликабельным
            process_link = wait.until(EC.element_to_be_clickable(
                (By.XPATH, '//a[@class="css-t7enrq" and contains(., "Процессы")]')))
            process_link.click()
            attach_screenshot(driver, "После перехода на вкладку 'Процессы'")
        except Exception as e:
            attach_screenshot(driver, "Ошибка при переходе на вкладку 'Процессы'")
            pytest.fail(f"Не удалось найти или кликнуть на вкладку 'Процессы': {e}")

    with allure.step("Клик по кнопке на странице процессов"):
        try:
            # Ожидание, пока кнопка не станет кликабельной
            create_button = wait.until(EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="main"]/div/div/div[1]/div[1]/button')))
            create_button.click()
            attach_screenshot(driver, "После клика по кнопке")
        except Exception as e:
            attach_screenshot(driver, "Ошибка при клике по кнопке")
            pytest.fail(f"Не удалось найти или кликнуть по кнопке: {e}")

    time.sleep(2)  # Пауза для наглядности (можно убрать в production)

    # Заполняем данные
    with allure.step("Выбор процесса 'Развитие QA тестирования в BP'"):
        try:
            # Клик по выпадающему меню
            process_dropdown = wait.until(EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="main"]/div[1]/div/div[2]/div/div[1]/div[2]/div/div/div/div/div')))
            process_dropdown.click()

            # Выбор пункта "Развитие QA тестирования в BP"
            qa_testing_option = wait.until(EC.element_to_be_clickable(
                (By.XPATH, '//li[contains(text(), "Развитие QA тестирования в BP")]')))
            qa_testing_option.click()
            attach_screenshot(driver, "После выбора процесса")
        except Exception as e:
            attach_screenshot(driver, "Ошибка при выборе процесса")
            pytest.fail(f"Не удалось выбрать процесс: {e}")

    with allure.step("Ввод названия экземпляра процесса"):
        try:
            # Ввод названия "Автотест Процесс"
            process_name_input = wait.until(EC.element_to_be_clickable(
                (By.XPATH, '//input[contains(@class, "MuiInputBase-input") and @placeholder="Введите название экземпляра процесса"]')))
            process_name_input.send_keys("Автотест Процесс")
            attach_screenshot(driver, "После ввода названия")
        except Exception as e:
            attach_screenshot(driver, "Ошибка при вводе названия")
            pytest.fail(f"Не удалось ввести название: {e}")
#Описание
    with allure.step("Ввод описания 'Автотест по бизнес процессам'"):
        try:
            # Ввод описания
            description_input = wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, 'textarea[name="description"]')))
            description_input.send_keys("Автотест по бизнес процессам")
            attach_screenshot(driver, "После ввода описания")
        except Exception as e:
            attach_screenshot(driver, "Ошибка при вводе описания")
            pytest.fail(f"Не удалось ввести описание: {e}")
#Валюта
    with allure.step("Выбор валюты 'USD'"):
        try:
            # Прокрутка страницы вниз
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)  # Небольшая пауза для завершения прокрутки

            # Клик по полю выбора валюты
            currency_input = wait.until(EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="main"]/div[1]/div/div[2]/div/div[4]/div[2]/div/div[1]/div/div/div/div/div')))
            currency_input.click()

            # Выбор валюты "USD"
            usd_option = wait.until(EC.element_to_be_clickable(
                (By.XPATH, '//li[contains(text(), "USD")]')))
            usd_option.click()
            attach_screenshot(driver, "После выбора валюты")
        except Exception as e:
            attach_screenshot(driver, "Ошибка при выборе валюты")
            pytest.fail(f"Не удалось выбрать валюту: {e}")
        # Участники
    element = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="main"]/div[1]/div/div[2]/div/div[3]/div[2]/div/div[1]/div/div/div')
    ))
    # Использование ActionChains для ввода текста
    actions = ActionChains(driver)
    actions.move_to_element(element).click().send_keys("Бекир Кумехов").send_keys(Keys.ENTER).perform()
    actions.move_by_offset(0, 50).click().perform()
    attach_screenshot(driver, "выбрал участника")
# Нажимаем добавить
    with allure.step("Нажатие на кнопку 'Далее'"):
        try:
            wait = WebDriverWait(driver, 10)  # Убедимся, что wait объявлен
            next_button = wait.until(EC.element_to_be_clickable((By.ID, ":rf:")))
            next_button.click()
            attach_screenshot(driver, "После нажатия кнопки 'Далее'")
        except Exception as e:
            attach_screenshot(driver, "Ошибка при нажатии кнопки 'Далее'")
            pytest.fail(f"Не удалось нажать на кнопку 'Далее': {e}")
            time.sleep(3)
            attach_screenshot(driver, "Ошибка при нажатии кнопки 'Далее'")
#Редактирование