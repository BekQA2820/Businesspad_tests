import pytest
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import time
import allure

# Функция для создания скриншота в Allure
def attach_screenshot(driver, name):
    allure.attach(driver.get_screenshot_as_png(), name=name, attachment_type=allure.attachment_type.PNG)

# Генерация уникального названия компании
def generate_unique_company_name(base_name="Автотест"):
    unique_suffix = f"{base_name}_{int(time.time())}_{random.randint(1000, 9999)}"
    return unique_suffix


# Генерация уникального номера телефона
def generate_unique_phone_number():
    return f"+7{random.randint(900000000, 999999999)}"


# Генерация уникального email
def generate_unique_email():
    return f"test{int(time.time())}@example.com"


# Генерация уникального ФИО
def generate_unique_full_name():
    first_names = ["Иван", "Алексей", "Дмитрий", "Сергей", "Михаил"]
    last_names = ["Иванов", "Петров", "Сидоров", "Кузнецов", "Попов"]
    middle_names = ["Иванович", "Алексеевич", "Дмитриевич", "Сергеевич", "Михайлович"]

    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    middle_name = random.choice(middle_names)

    return f"{first_name} {last_name} {middle_name}"

# открываем браузер
@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()


def test_add_and_edit_counteragent(driver):
    driver.get("https://team.business-pad.com/")

    # Вход в систему

    driver.find_element(By.XPATH, '//*[@id=":r0:"]').send_keys("K.Bekir")
    driver.find_element(By.XPATH, '//*[@id=":r1:"]').send_keys("Team.Bekir")
    driver.find_element(By.XPATH, '//*[@id="root"]/div/main/div/div/div/div[2]/div/form/div/div[4]').click()

    wait = WebDriverWait(driver, 1)
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[1]/div/div[2]/a[4]/div')))

    # Открытие настроек и добавление контрагента
    with allure.step("добавление контрагента"):
        driver.find_element(By.XPATH, '//*[@id="root"]/div/div[1]/div/div[2]/a[4]/div').click()

    wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="main"]/div/div/div[2]/div[3]/div[2]/div/div/div/div[2]/div[2]/p'))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="main"]/div/div/div[1]/div[1]/button'))).click()

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

    # Генерируем уникальные данные для контрагента
    unique_company_name = generate_unique_company_name()
    unique_phone_number = generate_unique_phone_number()
    unique_email = generate_unique_email()
    unique_full_name = generate_unique_full_name()

    # Заполняем данные контрагента
    with allure.step("Заполняем данные контрагента"):
        wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Введите ИНН']"))).send_keys(
            inn_value)
    # Инн
    # Проверяем, активна ли кнопка "Добавить"
    add_button = wait.until(
    EC.presence_of_element_located((By.XPATH, "//button[@type='submit' and text()='Добавить']")))
    # Если кнопка активна, тест должен упасть
    assert not add_button.is_enabled(), " Ошибка! Кнопка 'Добавить' активна при пустых данных!"
    print(" Все ок! Кнопка 'Добавить' неактивна.")
    #Название
    driver.find_element(By.XPATH, "//input[@placeholder='Введите название']").send_keys(unique_company_name)

    # Проверяем, активна ли кнопка "Добавить"
    add_button = wait.until(
        EC.presence_of_element_located((By.XPATH, "//button[@type='submit' and text()='Добавить']")))
    # Если кнопка активна, тест должен упасть
    assert not add_button.is_enabled(), " Ошибка! Кнопка 'Добавить' активна при пустых данных,Название!"
    print(" Все ок! Кнопка 'Добавить' неактивна.")
    #Фио
    driver.find_element(By.XPATH, "//input[@placeholder='Введите ФИО']").send_keys(unique_full_name)

    # Проверяем, активна ли кнопка "Добавить"
    add_button = wait.until(
        EC.presence_of_element_located((By.XPATH, "//button[@type='submit' and text()='Добавить']")))
    # Если кнопка активна, тест должен упасть
    assert not add_button.is_enabled(), " Ошибка! Кнопка 'Добавить' активна при пустых данных Фио!"
    print(" Все ок! Кнопка 'Добавить' неактивна.")
    #email
    driver.find_element(By.XPATH, "//input[@placeholder='Введите Email']").send_keys(unique_email)

    # Проверяем, активна ли кнопка "Добавить"
    add_button = wait.until(
        EC.presence_of_element_located((By.XPATH, "//button[@type='submit' and text()='Добавить']")))
    # Если кнопка активна, тест должен упасть
    assert not add_button.is_enabled(), " Ошибка! Кнопка 'Добавить' активна при пустых данных, email!"
    print(" Все ок! Кнопка 'Добавить' неактивна.")
    #телефон
    driver.find_element(By.XPATH, "//input[@placeholder='Введите номер телефона']").send_keys(unique_phone_number)

    # Проверяем, активна ли кнопка "Добавить"
    add_button = wait.until(
        EC.presence_of_element_located((By.XPATH, "//button[@type='submit' and text()='Добавить']")))
    # Если кнопка активна, тест должен упасть

    #производитель
    driver.find_element(By.XPATH, "//span[text()='Является производителем']").click()

    # Выбираем статус
    status_input = driver.find_element(By.XPATH, "//input[@placeholder='Выберите статус']")
    status_input.click()
    wait.until(EC.element_to_be_clickable((By.XPATH, "//li[2]"))).click()

    # Нажимаем "Добавить"
    driver.find_element(By.XPATH, "//button[@type='submit' and text()='Добавить']").click()

   #производители
    button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Производители')]")))
    button.click()
    time.sleep(1)
    attach_screenshot(driver, "Контрагент добавлен")
# Ожидание троеточия и кликаем по нему

    try:
        buttons = driver.find_elements(By.XPATH, "//button[contains(@class, 'MuiIconButton-root')]")
        buttons[-1].click()
    except IndexError:
        pytest.fail("Не найдено кнопки 'троеточие'")

    # Ожидание и клик по кнопке "Редактировать"
    edit_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//li[contains(@class, 'MuiMenuItem-root') and text()='Редактировать']"))
    )
    edit_button.click()


    # Редактируем
    # Редактируем описание
    with allure.step("Редактирование"):

      description_input = wait.until(
        EC.presence_of_element_located((By.XPATH, "//textarea[@placeholder='Введите описание']"))
    )
    description_input.send_keys(Keys.CONTROL + "a")
    description_input.send_keys(Keys.BACKSPACE)
    description_input.send_keys("Все отлично")


    # Выбираем статус
    status_dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Выберите статус']")))
    status_dropdown.click()
    wait.until(EC.element_to_be_clickable((By.XPATH, "//li[contains(text(), 'Благонадежный')]"))).click()

    # Редактируем ФИО
    contact_name_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Введите ФИО']")))
    contact_name_input.send_keys(Keys.CONTROL + "a")
    contact_name_input.send_keys(Keys.BACKSPACE)
    # Даем UI обновиться

    # Проверяем, активна ли кнопка "Изменить"
    change_button = wait.until(EC.presence_of_element_located((By.XPATH, "//button[text()='Изменить']")))
    # Если кнопка активна, тест должен упасть
    assert not change_button.is_enabled(), " Ошибка! Кнопка активна при пустом Фио!"
    print(" Все ок! Кнопка неактивна.")
    contact_name_input.send_keys("Автотестов Автотест Автотестович")

    # Редактируем Email
    email_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Введите Email']")))
    email_input.send_keys(Keys.CONTROL + "a")
    email_input.send_keys(Keys.BACKSPACE)
    # Даем UI обновиться

    # Проверяем, активна ли кнопка "Изменить"
    change_button = wait.until(EC.presence_of_element_located((By.XPATH, "//button[text()='Изменить']")))
    # Если кнопка активна, тест должен упасть
    assert not change_button.is_enabled(), " Ошибка! Кнопка активна при пустом email!"
    print(" Все ок! Кнопка неактивна.")
    email_input.send_keys("excelent@gmail.com")

    # Редактируем номер телефона
    phone_input = wait.until(
        EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Введите номер телефона']"))
    )
    phone_input.send_keys(Keys.CONTROL + "a")
    phone_input.send_keys(Keys.BACKSPACE)
    # Даем UI обновиться
    time.sleep(1)
    # Проверяем, активна ли кнопка "Изменить"
    change_button = wait.until(EC.presence_of_element_located((By.XPATH, "//button[text()='Изменить']")))
    # Если кнопка активна, тест должен упасть
    assert not change_button.is_enabled(), " Ошибка! Кнопка активна при пустом номере!"
    print(" Все ок! Кнопка неактивна.")
    phone_input.send_keys("88005553535")

    # Редактируем должность
    position_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Введите должность']")))
    position_input.send_keys(Keys.CONTROL + "a")
    position_input.send_keys(Keys.BACKSPACE)
    position_input.send_keys("Автотест")

    # Редактирование Название
    name_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Введите название']")))
    name_input.click()
    name_input.send_keys(Keys.CONTROL + "a")
    name_input.send_keys(Keys.BACKSPACE)
    # Даем UI обновиться

    # Проверяем, активна ли кнопка "Изменить"
    change_button = wait.until(EC.presence_of_element_located((By.XPATH, "//button[text()='Изменить']")))
    # Если кнопка активна, тест должен упасть
    assert not change_button.is_enabled(), " Ошибка! Кнопка активна при пустом названии!"
    print(" Все ок! Кнопка неактивна.")

    name_input.send_keys("Идеальный автотест")

    # Кликаем по кнопке "Изменить"
    change_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Изменить']")))
    change_button.click()
    time.sleep(2)
    attach_screenshot(driver, "Контрагент отредактирован")
    # Удаляем
    with allure.step("Удаление"):
        try:
            buttons = driver.find_elements(By.XPATH, "//button[contains(@class, 'MuiIconButton-root')]")
            buttons[-1].click()
        except IndexError:
            pytest.fail("Не найдено кнопки 'троеточие'")

    delete_button = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//li[contains(@class, 'MuiMenuItem-root') and text()='Удалить']")))
    delete_button.click()
    time.sleep(1)
    attach_screenshot(driver, "Контрагент удален")