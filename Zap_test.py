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
            driver.get("https://testbp1.business-pad.com/")
            driver.find_element(By.XPATH, '//*[@id=":r0:"]').send_keys("adminbp")
            driver.find_element(By.XPATH, '//*[@id=":r1:"]').send_keys("") # вставь пароль
            driver.find_element(By.XPATH, '//*[@id="root"]/div/main/div/div/div/div[2]/div/form/div/div[4]').click()
            attach_screenshot(driver, "После логина")
        except Exception as e:
            pytest.fail(f"Ошибка авторизации: {str(e)}")
    # Шаг 2: Переход в настройки
    with allure.step("Переход в настройки"):
        try:
            settings_icon = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "svg[data-testid='SettingsIcon']")))
            ActionChains(driver).move_to_element(settings_icon).click().perform()
            attach_screenshot(driver, "После клика по настройкам")
        except Exception as e:
            pytest.fail(f"Ошибка перехода в настройки: {str(e)}")


    #Пользователь и роли
    with allure.step("Создаем пользователя"):
        try:
            account_button = WebDriverWait(driver, 15).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div/div[1]/div/div[3]/a[3]'))
            )
            ActionChains(driver).move_to_element(account_button).double_click().perform()

            # Нажатие кнопки добавления
            plus_button = WebDriverWait(driver, 15).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="main"]/div/div/div[1]/button'))
            )
            ActionChains(driver).move_to_element(plus_button).double_click().perform()

            ActionChains(driver).move_to_element(plus_button).double_click().perform()
            name_input = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[name="firstName"]'))
            )
            ActionChains(driver).move_to_element(name_input).double_click().perform()
            name_input.send_keys("Bekirr2")
            fam_input = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[name="lastName"]'))
            )
            ActionChains(driver).move_to_element(fam_input).double_click().perform()
            fam_input.send_keys("Kumehovw")
            log_input = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[name="username"]'))
            )
            ActionChains(driver).move_to_element(log_input).double_click().perform()
            log_input.send_keys("admi28202")
            pas_input = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[name="password"]'))
            )
            ActionChains(driver).move_to_element(pas_input).double_click().perform()
            pas_input.send_keys("xdpIW22223")
            podr_input = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[name="department"]'))
            )
            ActionChains(driver).move_to_element(podr_input).double_click().perform()
            podr_input.send_keys("qa1")
            position_input = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[name="position"]'))
            )
            ActionChains(driver).move_to_element(position_input).double_click().perform()
            position_input.send_keys("test1")
            email_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="email"]'))
            )
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", email_input)
            email_input.click()
            email_input.send_keys("tefxs3@gmail.com")
            phone_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="phone"]'))
            )
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", phone_input)
            phone_input.click()
            phone_input.send_keys("88007583535")
            save_but = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//button[contains(text(), "Сохранить")]'))
            )
            save_but.click()
        except Exception as e:
            pytest.fail(f"Ошибка пользователя: {str(e)}")
    # Список сотрудников
    with allure.step("Список сотрудников"):
        try:
            account_button = WebDriverWait(driver, 15).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div/div[1]/div/div[3]/a[3]'))
            )
            ActionChains(driver).move_to_element(account_button).double_click().perform()
        except Exception as e:
            pytest.fail(f"Ошибка Списка сотрудников: {str(e)}")
    # !!!!!!!!
    with allure.step("кликаем по аватару"):
        try:
            avatar_button = WebDriverWait(driver, 15).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, 'img[alt="avatar"]'))
            )
            ActionChains(driver).move_to_element(avatar_button).double_click().perform()
            time.sleep(1)
            add_button = driver.find_element(By.XPATH,
                                             '//*[@id="main"]/div[2]/form/div[1]/div/div[3]/div[1]/div/button')
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", add_button)
            add_button.click()
        except Exception as e:
            pytest.fail(f"Ошибка пользователя: {str(e)}")
        # Добавляем роль
    with allure.step("добавляем роль"):
        try:
            role_field = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="main"]/div[3]/form/div[1]/div/div/div/div[1]/div')))
            role_field.click()
            add_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.MuiButton-contained.css-lmp1wz')))
            add_button.click()
        except Exception as e:
            pytest.fail(f"Ошибка : {str(e)}")
        # Экономист
    with allure.step("Ввод названия роли"):
        try:
            role_input = WebDriverWait(driver, 55).until(
                EC.visibility_of_element_located((By.NAME, "name")))
            role_input.click()
            role_input.clear()
            role_input.send_keys("Экономист")
            driver.find_element(By.XPATH, '//button[contains(text(), "Редактирование")]').click() #ПЕРВОЕ РЕДАКТИРОВАНИЕ
            driver.find_element(By.XPATH, '//span[contains(text(), "Редактирование основной информации экземпляров БП")]/preceding-sibling::span/input').click() #Первый чекбокс
            driver.find_element(By.XPATH, '//span[text()="Редактирование сущностей экземпляров БП"]/preceding-sibling::span//input').click() #Второй чекбокс
            driver.find_element(By.XPATH, '//span[text()="Смена этапов экземпляров БП"]/preceding-sibling::span').click() #Третий чекбокс
            driver.find_element(By.XPATH, '//span[contains(@class, "MuiTypography-body1") and contains(text(), "Редактирование участников")]/preceding-sibling::span[contains(@class, "MuiCheckbox-root")]').click() #Четвертый чекбокс
            driver.find_element(By.XPATH, '//*[@id="main"]/div[4]/form/div[1]/div/div[2]/div[3]/div[2]/div/button[3]').click() # ВТОРОЕ РЕДАКТИРОВАНИЕ
            driver.find_element(By.XPATH, '//span[text()="Редактирование основной информации задач"]/preceding-sibling::span').click() #Первый чекбокс
            driver.find_element(By.XPATH, '//span[contains(text(), "Редактирование сущностей задач")]/..').click() #Второй чекбокс
            driver.find_element(By.XPATH, '//*[@id="main"]/div[4]/form/div[1]/div/div[2]/div[4]/div[2]/div/button[2]').click() #ТРЕТИЙ ПРОСМОТР
            #Скрол и клик по нижним чекбоксам!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            element = driver.find_element(By.XPATH, '//span[text()="Редактирование тегов в экземплярах БП и задачах"]/preceding-sibling::span')
            driver.execute_script("arguments[0].scrollIntoView();", element)
            element.click()
            element = driver.find_element(By.XPATH, "//span[contains(text(), 'Движение средств')]/../span[1]")
            driver.execute_script("arguments[0].scrollIntoView();", element)
            element.click()
            element = driver.find_element(By.XPATH, '//span[contains(text(), "Вычисляемое")]/../span[1]')
            driver.execute_script("arguments[0].scrollIntoView();", element)
            element.click()
            #"Сохранить"
            save_button = driver.find_element(By.XPATH, '//*[@id="main"]/div[4]/form/div[2]/div/div')
            driver.execute_script("arguments[0].scrollIntoView();", save_button)
            save_button.click()
        except Exception as e:
            pytest.fail(f"Ошибка при вводе названия роли: {str(e)}. Скриншот: role_input_error.png")