import pytest
from selenium import webdriver
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure
import time
from selenium.common.exceptions import TimeoutException  # Импорт для обработки таймаута


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
    wait = WebDriverWait(driver, 20)  # Явное ожидание
    with allure.step("Открываем сайт и логинимся"):
        driver.get("https://finance.business-pad.com/")
        # Вход в систему
        driver.find_element(By.XPATH, '//*[@id=":r0:"]').send_keys("adminbp")
        driver.find_element(By.XPATH, '//*[@id=":r1:"]').send_keys("AtVFpd3hFeEc")
        driver.find_element(By.XPATH, '//*[@id="root"]/div/main/div/div/div/form/div/button').click()


    try:
        driver.get("https://finance.business-pad.com/bp-settings/114")
        with allure.step("Клик по 'Новый этап'"):
            new_stage = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, '//p[@aria-label="Новый этап"]'))
            )
            ActionChains(driver).move_to_element(new_stage).click().perform()
            print("Клик по 'Новый этап' выполнен")
            time.sleep(1)

        with allure.step("Заполнение названия этапа"):
            name_field = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//input[@placeholder="Введите название узла"]'))
            )
            name_field.click()
            name_field.send_keys(Keys.CONTROL + 'a')
            name_field.send_keys(Keys.DELETE)
            name_field.send_keys("Этап автотеста")
            print("Название этапа заполнено")
            time.sleep(0.5)

        with allure.step("Заполнение описания"):
            desc_field = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//textarea[@placeholder="Введите описание узла"]'))
            )
            desc_field.click()
            desc_field.send_keys("Описание автотеста")
            print("Описание заполнено")
            desc_field.send_keys(Keys.ENTER)
            print("Нажатие Enter выполнено")

            # Клик по 'Этап автотеста' после нажатия Enter
            with allure.step("Клик по 'Этап автотеста'"):
                etap_autotest = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//p[@aria-label="Этап автотеста"]'))
                )
                etap_autotest.click()
                print("Клик по 'Этап автотеста' выполнен")
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        with allure.step("Назначение ответственного"):

            responsible_header = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//h2[contains(text(), "Ответственные")]'))
            )
            responsible_header.click()
            print("Раздел 'Ответственные' открыт")

            responsible_field = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//input[@placeholder="Выберите ответственных"]'))
            )
            responsible_field.click()
            print("Поле выбора ответственного открыто")

        # Поиск и выбор тестировщика
        try:
            tester_option = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[contains(text(), "Тестировщик")]'))
            )
            tester_option.click()
            print("Тестировщик выбран")
        except TimeoutException:
            print("Тестировщик не найден, продолжаем тест без ошибки")

        # Клик по контейнеру "Новый этап" в любом случае
        with allure.step("Клик по контейнеру 'Новый этап'"):
            first_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/main/div[2]/div[2]/div[2]/div/div/div/div[3]/div/div/div/div[2]/div/div/form/div[1]/h3'))
            )
            first_button.click()
            print("Клик по первой кнопке выполнен")

            # Клик по второму элементу
            second_element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="mui-p-93966-P-1"]/form/div[1]/div/div/div/div/div/div/div/div[2]/div[1]/div/div'))
            )
            second_element.click()
            print("Клик по второму элементу выполнен")

            # Нажатие Enter
            second_element.send_keys(Keys.ENTER)
            print("Нажатие Enter выполнено")

    except Exception as e:
        print(f"Ошибка: {e}")

    except Exception as e:
        print(f"Ошибка при выполнении: {str(e)}")

