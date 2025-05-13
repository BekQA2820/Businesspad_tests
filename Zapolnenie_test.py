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
            driver.find_element(By.XPATH, '//*[@id=":r1:"]').send_keys("TUqHXP79irZd")
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
    # Шаг 3: Выбор финансовых операций
    with allure.step("Выбор финансовых операций"):
        try:
            bp_list = wait.until(
                EC.element_to_be_clickable((By.XPATH,
                                            '//*[@id="main"]/div/div/div[2]/div[2]/div[2]/div/div/div/div[2]/div[2]/p')))
            ActionChains(driver).move_to_element(bp_list).double_click().perform()
            attach_screenshot(driver, "После выбора финансовых операций")
        except Exception as e:
            pytest.fail(f"Ошибка выбора финансовых операций: {str(e)}")
    # Шаг 4: Заполнение единиц
    participants = [ "шт", "кг", "г", "л","т", "Услуга", "пп", "услуга","комп"]
    input_xpath = '//*[@id="main"]/div[2]/form/div/div/div[2]/div[1]/div[2]/div[1]/div/div[1]/div/div/div[1]/div/div'
    for participant in participants:
        try:
            # 1. Ожидаем и находим поле ввода
            time.sleep(0.2)
            input_field = wait.until(
                EC.presence_of_element_located((By.XPATH, input_xpath)))
            # 2. Проверяем, что элемент видимый и доступный для ввода
            if not input_field.is_displayed() or not input_field.is_enabled():
                print(f"Поле ввода недоступно для единицы {participant}")
                continue
            # 3. Прокручиваем к элементу (если нужно)
            driver.execute_script("arguments[0].scrollIntoView(true);", input_field)
            # 4. Кликаем и вводим через ActionChains (более надежный способ)
            actions = ActionChains(driver)
            actions.move_to_element(input_field).click().pause(0.2)
            actions.send_keys(participant).pause(0.1)
            actions.send_keys(Keys.ENTER).perform()
            print(f"Успешно добавлен единиц: {participant}")
        except Exception as e:
            print(f"Пропуск единицы {participant} из-за ошибки: {str(e)}")
            continue
        attach_screenshot(driver, "После заполнения всех единиц")
    #ВАЛЮТЫ!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    participants = [ "RUB", "EUR", "USD", "KZT","CNY", "JPY", "AED"]
    input_xpath = '//*[@id="main"]/div[2]/form/div/div/div[2]/div[1]/div[2]/div[2]/div/div[1]/div/div/div[1]/div/div'
    for participant in participants:
        try:
            # 1. Ожидаем и находим поле ввода
            time.sleep(0.2)
            input_field = wait.until(
                EC.presence_of_element_located((By.XPATH, input_xpath)))
            # 2. Проверяем, что элемент видимый и доступный для ввода
            if not input_field.is_displayed() or not input_field.is_enabled():
                print(f"Поле ввода недоступно для валюты {participant}")
                continue
            # 3. Прокручиваем к элементу (если нужно)
            driver.execute_script("arguments[0].scrollIntoView(true);", input_field)
            # 4. Кликаем и вводим через ActionChains (более надежный способ)
            actions = ActionChains(driver)
            actions.move_to_element(input_field).click().pause(0.5)
            actions.send_keys(participant).pause(0.3)
            actions.send_keys(Keys.ENTER).perform()
            print(f"Успешно добавлена валюта: {participant}")
        except Exception as e:
            print(f"Пропуск валюты {participant} из-за ошибки: {str(e)}")
            continue
        attach_screenshot(driver, "После заполнения всех валют")
    #Финансовые операции
    participants = [ "Покупка товара/услуги", "Продажа товара/услуги","Таможенная пошлина",
                     "БР","Транспорт до границы", "Процент по кредиту","НДС+Таможенный сбор", "Транспорт после границы",
                     "Репатриация","Ненормативные расходы", "Заем", "Услуги таможенного брокера","Прочие до налогов", "Комиссия за конвертацию валюты",
                     "Комиссии банк(1%)"]
    input_xpath = '//*[@id="main"]/div[2]/form/div/div/div[2]/div[1]/div[2]/div[3]/div/div[1]/div/div/div[1]'
    for participant in participants:
        try:
            # 1. Ожидаем и находим поле ввода
            time.sleep(0.2)
            input_field = wait.until(
                EC.presence_of_element_located((By.XPATH, input_xpath)))
            # 2. Проверяем, что элемент видимый и доступный для ввода
            if not input_field.is_displayed() or not input_field.is_enabled():
                print(f"Поле ввода недоступно для единицы {participant}")
                continue
            # 3. Прокручиваем к элементу (если нужно)
            driver.execute_script("arguments[0].scrollIntoView(true);", input_field)
            # 4. Кликаем и вводим через ActionChains (более надежный способ)
            actions = ActionChains(driver)
            actions.move_to_element(input_field).click().pause(0.5)
            actions.send_keys(participant).pause(0.3)
            actions.send_keys(Keys.ENTER).perform()
            print(f"Успешно добавлен Финансовые операций: {participant}")
        except Exception as e:
            print(f"Пропуск Финансовой операции {participant} из-за ошибки: {str(e)}")
            continue
        attach_screenshot(driver, "После заполнения всех операций")
    #Вычитаемые финансовые операции
    participants = [ "Комиссия 1", "Комиссия 2","Комиссия 3", "Комиссия 4","Комиссия 5", "Комиссия 6","Комиссия 7", "Комиссия 8", "Комиссия 10",
                     "Прочие после налогов", "Прочие до налогов"]
    input_xpath = '//*[@id="main"]/div[2]/form/div/div/div[2]/div[1]/div[2]/div[4]/div/div[1]/div/div/div[1]/div/div'
    for participant in participants:
        try:
            # 1. Ожидаем и находим поле ввода
            time.sleep(0.2)
            input_field = wait.until(
                EC.presence_of_element_located((By.XPATH, input_xpath)))
            # 2. Проверяем, что элемент видимый и доступный для ввода
            if not input_field.is_displayed() or not input_field.is_enabled():
                print(f"Поле ввода недоступно для валюты {participant}")
                continue
            # 3. Прокручиваем к элементу (если нужно)
            driver.execute_script("arguments[0].scrollIntoView(true);", input_field)
            # 4. Кликаем и вводим через ActionChains
            actions = ActionChains(driver)
            actions.move_to_element(input_field).click().pause(0.2)
            actions.send_keys(participant).pause(0.2)
            actions.send_keys(Keys.ENTER).perform()
            print(f"Успешно добавлена выч.фин: {participant}")
        except Exception as e:
            print(f"Пропуск выч.фин {participant} из-за ошибки: {str(e)}")
            continue
        attach_screenshot(driver, "После заполнения всех выч.фин")
    #Налог!!!!!!!!!!!!
    # Шаг 4: Заполнение процентов
    participants = ["0", "5","7","10","15", "20"]
    input_xpath = '//*[@id="main"]/div[2]/form/div/div/div[2]/div[1]/div[2]/div[5]/div/div[1]/div/div/div[1]'
    for participant in participants:
        try:
            # 1. Ожидаем и находим поле ввода
            time.sleep(0.1)
            input_field = wait.until(
                EC.presence_of_element_located((By.XPATH, input_xpath)))
            # 2. Проверяем, что элемент видимый и доступный для ввода
            if not input_field.is_displayed() or not input_field.is_enabled():
                print(f"Поле ввода недоступно для процента {participant}")
                continue
            # 3. Прокручиваем к элементу (если нужно)
            driver.execute_script("arguments[0].scrollIntoView(true);", input_field)
            # 4. Кликаем и вводим через ActionChains (более надежный способ)
            actions = ActionChains(driver)
            actions.move_to_element(input_field).click().pause(0.2)
            actions.send_keys(participant).pause(0.1)
            actions.send_keys(Keys.ENTER).perform()
            print(f"Успешно добавлен процент: {participant}")
        except Exception as e:
            print(f"Пропуск процента {participant} из-за ошибки: {str(e)}")
            continue
        attach_screenshot(driver, "После заполнения всех процентов")
    # Шаг 4: Заполнение Статусов
    participants = ["заявление к оплате", "утверждено в оплату", "утверждено в реестре", "утверждено в оплату ДирКем"
        ,"утверждено в оплату ДЭ" , "утверждено в оплату КД",
                    "утверждено в реестре/утверждено в оплату",
                    "утверждено в реестре/утверждено в оплату ДирКем",
                    "заявление к оплате/оплата по сигналу" , "заявление в оплату/оплата по сигналу",
                    "заявление в реестре/оплата по сигналу" , "утверждено в оплату ДирКем/оплата по сигналу",
                    "утверждено в оплату ДЭ/оплата по сигналу", "утверждено в реестре/утверждено в оплату/оплата по сигналу",
                    "утверждено в реестре/утверждено в оплату ДирКем/оплата по сигналу",
                    "утверждено в реестре/утверждено в оплату ДЭ/оплата по сигналу",
                    "заявлено к оплате/оплата по наиболее выгодному курсу до" ,
                    "утверждено в оплату/оплата по наиболее выгодному курсу до",
                    "утверждено в реестре/оплата по наиболее выгодному курсу до" ,
                    "утверждено в реестре/утверждено в оплату/оплата по наиболее выгодному курсу до",
                    "утверждено в реестре/утверждено в оплату ДЭ/оплата по наиболее выгодному курсу до",
                    "утверждено в реестре/утверждено в оплату ДирКем/оплата по наиболее выгодному курсу до",
                    "заявлено к оплате/требуется согласование КД и ДЭ", "утверждено в оплату ДирКем/ требуется согласование КД и ДЭ",
                    "утверждено в реестре/требуется согласование КД и ДЭ" ,
                    "утверждено в реестре/утверждено в оплату ДирКем/требуется согласование КД и ДЭ",
                    "Черновик" , "план", "заявлено к оплате, перерасход", "утверждено в оплату,перерасход",
                    "утверждено в реестре, перерасход", "утверждено в реестре, утверждено ДирКем, перерасход",
                    "утверждено в реестре, утверждено ДирКем,оплата по наиболее выгодному курсу до, перерасход", "факт"]
    input_xpath = '//*[@id="main"]/div[2]/form/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/div[1]/div/div'
    for participant in participants:
        try:
            # 1. Ожидаем и находим поле ввода
            time.sleep(0.1)
            input_field = wait.until(
                EC.presence_of_element_located((By.XPATH, input_xpath)))
            # 2. Проверяем, что элемент видимый и доступный для ввода
            if not input_field.is_displayed() or not input_field.is_enabled():
                print(f"Поле ввода недоступно для статуса {participant}")
                continue
            # 3. Прокручиваем к элементу (если нужно)
            driver.execute_script("window.scrollBy(0, -100);")  # Прокрутка вверх
            time.sleep(0.1)
            input_field.click()
            # 4. Кликаем и вводим через ActionChains (более надежный способ)
            actions = ActionChains(driver)
            actions.move_to_element(input_field).click().pause(1)
            actions.send_keys(participant).pause(0.2)
            actions.send_keys(Keys.ENTER).perform()
            print(f"Успешно добавлен статус: {participant}")
        except Exception as e:
            print(f"Пропуск статуса {participant} из-за ошибки: {str(e)}")
            continue
        attach_screenshot(driver, "После заполнения всех статусов")
    #Выходим
    with allure.step("Выход"):
        exit_attempts = [
            ('Основная кнопка выхода', '//*[@id="main"]/div[2]/button'),  # XPath основной кнопки
            ('Крестик (CloseIcon)', '[data-testid="CloseIcon"]'),          # CSS крестика
            ('Кнопка "Отмена"', '//button[contains(text(), "Отмена")]'),   # XPath кнопки с текстом
            ('Иконка закрытия', '.modal-close-button'),                    # CSS класса иконки
        ]
    for attempt_name, locator in exit_attempts:
        try:
            element = wait.until(EC.element_to_be_clickable((By.XPATH, locator) if locator.startswith('//')
                                                            else (By.CSS_SELECTOR, locator)))
            ActionChains(driver).move_to_element(element).click().perform()
            break  # Если клик успешен — выходим из цикла
        except Exception:
            continue  # Пробуем следующий вариант
        else:
         print("Не удалось выйти: ни одна из кнопок не найдена")
    # Документы
    with allure.step("Выбор Документов"):
        try:
            bp_list = wait.until(
                EC.element_to_be_clickable((By.XPATH,
                                            '//*[@id="main"]/div/div/div[2]/div[3]/div[2]/div/div/div/div[5]/div[2]')))
            ActionChains(driver).move_to_element(bp_list).double_click().perform()
            attach_screenshot(driver, "После выбора документов")
        except Exception as e:
            print(f"Ошибка выбора документов: {str(e)}")
    participants = ["Устав", "Свидетельство регистрации","Свидетельство ИНН","Решение (протокол) о назначении руководителя","Выписка из ЕГРЮЛ",
                    "Карточка основных сведений контрагента" ,"Бухгалтерская отчетность", "Бизнес-справка","Лицензия на торговую деятельность",
                    "Свидетельство VAT" , "Доверенность уполномоченного лица","Договор аренды", "Паспорт Генерального директора"]
    input_xpath = '//*[@id="main"]/div[2]/form/div/div/div[2]/div/div[2]/div/div/div[1]/div/div/div[1]/div/div/fieldset'
    for participant in participants:
        try:
            # 1. Ожидаем и находим поле ввода
            time.sleep(0.1)
            input_field = wait.until(
                EC.presence_of_element_located((By.XPATH, input_xpath)))
            # 2. Проверяем, что элемент видимый и доступный для ввода
            if not input_field.is_displayed() or not input_field.is_enabled():
                print(f"Поле ввода недоступно для документов {participant}")
                continue
            # 3. Прокручиваем к элементу (если нужно)
            driver.execute_script("arguments[0].scrollIntoView(true);", input_field)
            # 4. Кликаем и вводим через ActionChains (более надежный способ)
            actions = ActionChains(driver)
            actions.move_to_element(input_field).click().pause(0.5)
            actions.send_keys(participant).pause(0.3)
            actions.send_keys(Keys.ENTER).perform()
            print(f"Успешно добавлен документ: {participant}")
        except Exception as e:
            print(f"Пропуск документа {participant} из-за ошибки: {str(e)}")
            continue
        attach_screenshot(driver, "После заполнения всех документов")
        #Выходим
    with allure.step("Выход"):
        elements = [
            ('Основная кнопка', By.CSS_SELECTOR, 'button[anchor="right"]'),
            ('Крестик', By.CSS_SELECTOR, '[data-testid="CloseIcon"]'),
            ('Иконка закрытия', By.CLASS_NAME, 'MuiIconButton-root'),
            ('SVG закрытия', By.CSS_SELECTOR, 'svg[viewBox="0 0 24 24"]')
        ]

    click_methods = [
        lambda el: el.click(),
        lambda el: ActionChains(driver).click(el).perform(),
        lambda el: driver.execute_script("arguments[0].click();", el),
        lambda el: ActionChains(driver).double_click(el).perform()
    ]

    success = False
    for name, by, locator in elements:
        try:
            el = WebDriverWait(driver, 5).until(EC.presence_of_element_located((by, locator)))
            for method in click_methods:
                try:
                    method(el)
                    success = True
                    break
                except:
                    continue
            if success:
                break
        except:
            continue

    if not success:
        pytest.fail("Не удалось выйти: все варианты не сработали")

    # Явное продолжение теста
    WebDriverWait(driver, 5).until(EC.invisibility_of_element_located((by, locator)))
    #Процент по кредиту
    with allure.step("Кредит"):
        try:
            settings_icon = wait.until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="main"]/div/div/div[2]/div[2]/div[2]/div/div/div/div[5]/div[2]')))
            ActionChains(driver).move_to_element(settings_icon).click().perform()
            plus_icon = wait.until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="main"]/div[1]/div/div[1]/div[2]/div[2]/button')))
            ActionChains(driver).move_to_element(plus_icon).click().perform()
        except Exception as e:
            print(f"Ошибка при работе с датой: {str(e)}")
        #ПЕРВЫЙ
    with allure.step("ДАТА"):
        try:
            # Клик по кнопке календаря (если нужно открыть попап)
            calendar_button = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'td.css-ua8zne button[aria-label="Choose date"]'))
            )
            ActionChains(driver).move_to_element(calendar_button).click().perform()

            # Ожидание и ввод даты в поле input
            date_input = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'td.css-ua8zne input[type="tel"]'))
            )
            date_input.clear()  # Очистка поля (если нужно)
            date_input.send_keys("01012022")
            #Процент
            calendar_button = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'td.css-ua8zne input[name="percentValue"]'))
            )
            ActionChains(driver).move_to_element(calendar_button).click().perform()
            # Ожидание и ввод даты в поле input
            date_input = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'td.css-ua8zne input[name="percentValue"]'))
            )
            date_input.clear()  # Очистка поля (если нужно)
            date_input.send_keys("10")
            save_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Сохранить")]')))
            save_button.click()
        except Exception as e:
            print(f"Ошибка при работе с датой: {str(e)}")
    #Второй
    with allure.step("ДАТА"):
        try:
            # Клик по кнопке календаря (если нужно открыть попап)
            plus_icon = wait.until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="main"]/div[1]/div/div[1]/div[2]/div[2]/button')))
            ActionChains(driver).move_to_element(plus_icon).click().perform()
            calendar_button = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'td.css-ua8zne button[aria-label="Choose date"]'))
            )
            ActionChains(driver).move_to_element(calendar_button).click().perform()

            # Ожидание и ввод даты в поле input
            date_input = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'td.css-ua8zne input[type="tel"]'))
            )
            date_input.clear()  # Очистка поля (если нужно)
            date_input.send_keys("01012023")
            #Процент
            calendar_button = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'td.css-ua8zne input[name="percentValue"]'))
            )
            ActionChains(driver).move_to_element(calendar_button).click().perform()
            # Ожидание и ввод даты в поле input
            date_input = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'td.css-ua8zne input[name="percentValue"]'))
            )
            date_input.clear()  # Очистка поля (если нужно)
            date_input.send_keys("15")
            save_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Сохранить")]')))
            save_button.click()
        except Exception as e:
            print(f"Ошибка при работе с датой: {str(e)}")
    #Третий
    with allure.step("ДАТА"):
        try:
            # Клик по кнопке календаря (если нужно открыть попап)
            plus_icon = wait.until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="main"]/div[1]/div/div[1]/div[2]/div[2]/button')))
            ActionChains(driver).move_to_element(plus_icon).click().perform()
            calendar_button = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'td.css-ua8zne button[aria-label="Choose date"]'))
            )
            ActionChains(driver).move_to_element(calendar_button).click().perform()

            # Ожидание и ввод даты в поле input
            date_input = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'td.css-ua8zne input[type="tel"]'))
            )
            date_input.clear()  # Очистка поля (если нужно)
            date_input.send_keys("01012024")
            #Процент
            calendar_button = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'td.css-ua8zne input[name="percentValue"]'))
            )
            ActionChains(driver).move_to_element(calendar_button).click().perform()
            # Ожидание и ввод даты в поле input
            date_input = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'td.css-ua8zne input[name="percentValue"]'))
            )
            date_input.clear()  # Очистка поля (если нужно)
            date_input.send_keys("21")
            save_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Сохранить")]')))
            save_button.click()
        except Exception as e:
            print(f"Ошибка при работе с датой: {str(e)}")
    #Четвертый
    with allure.step("ДАТА"):
        try:
            # Клик по кнопке календаря (если нужно открыть попап)
            plus_icon = wait.until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="main"]/div[1]/div/div[1]/div[2]/div[2]/button')))
            ActionChains(driver).move_to_element(plus_icon).click().perform()
            calendar_button = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'td.css-ua8zne button[aria-label="Choose date"]'))
            )
            ActionChains(driver).move_to_element(calendar_button).click().perform()

            # Ожидание и ввод даты в поле input
            date_input = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'td.css-ua8zne input[type="tel"]'))
            )
            date_input.clear()  # Очистка поля (если нужно)
            date_input.send_keys("01102024")
            #Процент
            calendar_button = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'td.css-ua8zne input[name="percentValue"]'))
            )
            ActionChains(driver).move_to_element(calendar_button).click().perform()
            # Ожидание и ввод даты в поле input
            date_input = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'td.css-ua8zne input[name="percentValue"]'))
            )
            date_input.clear()  # Очистка поля (если нужно)
            date_input.send_keys("24")
            save_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Сохранить")]')))
            save_button.click()
        except Exception as e:
            print(f"Ошибка при работе с датой: {str(e)}")
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
            name_input.send_keys("Bekirr9912")
            fam_input = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[name="lastName"]'))
            )
            ActionChains(driver).move_to_element(fam_input).double_click().perform()
            fam_input.send_keys("Kumehovw55")
            log_input = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[name="username"]'))
            )
            ActionChains(driver).move_to_element(log_input).double_click().perform()
            log_input.send_keys("admi2890432")
            pas_input = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[name="password"]'))
            )
            ActionChains(driver).move_to_element(pas_input).double_click().perform()
            pas_input.send_keys("xdpIW2225393")
            podr_input = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[name="department"]'))
            )
            ActionChains(driver).move_to_element(podr_input).double_click().perform()
            podr_input.send_keys("qa1345")
            position_input = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[name="position"]'))
            )
            ActionChains(driver).move_to_element(position_input).double_click().perform()
            position_input.send_keys("test13459")
            email_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="email"]'))
            )
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", email_input)
            email_input.click()
            email_input.send_keys("tef99dfg3@gmail.com")
            phone_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="phone"]'))
            )
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", phone_input)
            phone_input.click()
            phone_input.send_keys("88997589935")
            save_but = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//button[contains(text(), "Сохранить")]'))
            )
            save_but.click()
        except Exception as e:
            print(f"Ошибка при работе с датой: {str(e)}")
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
            role_input = WebDriverWait(driver, 15).until(
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
    # Добавляем роль 2
    with allure.step("добавляем роль"):
        try:
            role_field = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="main"]/div[3]/form/div[1]/div/div/div/div[1]/div')))
            role_field.click()
            add_button = WebDriverWait(driver, 25).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.MuiButton-contained.css-lmp1wz')))
            add_button.click()
        except Exception as e:
            pytest.fail(f"Ошибка : {str(e)}")
        # Юрист
    with allure.step("Ввод названия роли"):
        try:
            time.sleep(2)
            role_input = WebDriverWait(driver, 25).until(
                EC.visibility_of_element_located((By.NAME, "name")))
            role_input.click()
            role_input.clear()
            role_input.send_keys("Юрист")
            driver.find_element(By.XPATH, '//button[contains(text(), "Редактирование")]').click() #ПЕРВОЕ РЕДАКТИРОВАНИЕ
            driver.find_element(By.XPATH, '//span[contains(text(), "Редактирование основной информации экземпляров БП")]/preceding-sibling::span/input').click() #Первый чекбокс
            driver.find_element(By.XPATH, '//span[text()="Редактирование сущностей экземпляров БП"]/preceding-sibling::span//input').click() #Второй чекбокс
            driver.find_element(By.XPATH, '//span[text()="Смена этапов экземпляров БП"]/preceding-sibling::span').click() #Третий чекбокс
            driver.find_element(By.XPATH, '//span[contains(@class, "MuiTypography-body1") and contains(text(), "Редактирование участников")]/preceding-sibling::span[contains(@class, "MuiCheckbox-root")]').click() #Четвертый чекбокс
            driver.find_element(By.XPATH, '//*[@id="main"]/div[4]/form/div[1]/div/div[2]/div[3]/div[2]/div/button[3]').click() # ВТОРОЕ РЕДАКТИРОВАНИЕ
            driver.find_element(By.XPATH, '//span[text()="Редактирование основной информации задач"]/preceding-sibling::span').click() #Первый чекбокс
            driver.find_element(By.XPATH, '//span[contains(text(), "Редактирование сущностей задач")]/..').click() #Второй чекбокс
            #Скрол и клик по нижним чекбоксам!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            element = driver.find_element(By.XPATH, '//span[text()="Редактирование тегов в экземплярах БП и задачах"]/preceding-sibling::span')
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
    # Добавляем роль 3
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
        # ДирКем
    with allure.step("Ввод названия роли"):
        try:
            time.sleep(2)
            role_input = WebDriverWait(driver, 25).until(
                EC.visibility_of_element_located((By.NAME, "name")))
            role_input.click()
            role_input.clear()
            role_input.send_keys("ДирКем")
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
            element = driver.find_element(By.XPATH, '//span[contains(text(), "Вычисляемое")]/../span[1]')
            driver.execute_script("arguments[0].scrollIntoView();", element)
            element.click()
            #"Сохранить"
            save_button = driver.find_element(By.XPATH, '//*[@id="main"]/div[4]/form/div[2]/div/div')
            driver.execute_script("arguments[0].scrollIntoView();", save_button)
            save_button.click()
        except Exception as e:
            pytest.fail(f"Ошибка при вводе названия роли: {str(e)}. Скриншот: role_input_error.png")
    # Добавляем роль 4
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
        # РОП
    with allure.step("Ввод названия роли"):
        try:
            time.sleep(2)
            role_input = WebDriverWait(driver, 25).until(
                EC.visibility_of_element_located((By.NAME, "name")))
            role_input.click()
            role_input.clear()
            role_input.send_keys("РОП")
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
            element = driver.find_element(By.XPATH, '//span[contains(text(), "Вычисляемое")]/../span[1]')
            driver.execute_script("arguments[0].scrollIntoView();", element)
            element.click()
            #"Сохранить"
            save_button = driver.find_element(By.XPATH, '//*[@id="main"]/div[4]/form/div[2]/div/div')
            driver.execute_script("arguments[0].scrollIntoView();", save_button)
            save_button.click()
        except Exception as e:
            pytest.fail(f"Ошибка при вводе названия роли: {str(e)}. Скриншот: role_input_error.png")
    # Добавляем роль 5
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
        # Бизнес-аналитик
    with allure.step("Ввод названия роли"):
        try:
            time.sleep(2)
            role_input = WebDriverWait(driver, 25).until(
                EC.visibility_of_element_located((By.NAME, "name")))
            role_input.click()
            role_input.clear()
            role_input.send_keys("Бизнес-аналитик")
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
            element = driver.find_element(By.XPATH, '//span[contains(text(), "Вычисляемое")]/../span[1]')
            driver.execute_script("arguments[0].scrollIntoView();", element)
            element.click()
            #"Сохранить"
            save_button = driver.find_element(By.XPATH, '//*[@id="main"]/div[4]/form/div[2]/div/div')
            driver.execute_script("arguments[0].scrollIntoView();", save_button)
            save_button.click()
        except Exception as e:
            pytest.fail(f"Ошибка при вводе названия роли: {str(e)}. Скриншот: role_input_error.png")
    # Добавляем роль 6
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
        # Бухгалтер
    with allure.step("Ввод названия роли"):
        try:
            time.sleep(2)
            role_input = WebDriverWait(driver, 25).until(
                EC.visibility_of_element_located((By.NAME, "name")))
            role_input.click()
            role_input.clear()
            role_input.send_keys("Бухгалтер")
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
            element = driver.find_element(By.XPATH, '//span[contains(text(), "Вычисляемое")]/../span[1]')
            driver.execute_script("arguments[0].scrollIntoView();", element)
            element.click()
            element = driver.find_element(By.XPATH, "//span[contains(text(), 'Движение средств')]/../span[1]")
            driver.execute_script("arguments[0].scrollIntoView();", element)
            element.click()
            #"Сохранить"
            save_button = driver.find_element(By.XPATH, '//*[@id="main"]/div[4]/form/div[2]/div/div')
            driver.execute_script("arguments[0].scrollIntoView();", save_button)
            save_button.click()
        except Exception as e:
            pytest.fail(f"Ошибка при вводе названия роли: {str(e)}. Скриншот: role_input_error.png")
    # Добавляем роль 7
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
        # ГБ
    with allure.step("Ввод названия роли"):
        try:
            time.sleep(2)
            role_input = WebDriverWait(driver, 25).until(
                EC.visibility_of_element_located((By.NAME, "name")))
            role_input.click()
            role_input.clear()
            role_input.send_keys("ГБ")
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
            element = driver.find_element(By.XPATH, '//span[contains(text(), "Вычисляемое")]/../span[1]')
            driver.execute_script("arguments[0].scrollIntoView();", element)
            element.click()
            element = driver.find_element(By.XPATH, "//span[contains(text(), 'Движение средств')]/../span[1]")
            driver.execute_script("arguments[0].scrollIntoView();", element)
            element.click()
            #"Сохранить"
            save_button = driver.find_element(By.XPATH, '//*[@id="main"]/div[4]/form/div[2]/div/div')
            driver.execute_script("arguments[0].scrollIntoView();", save_button)
            save_button.click()
        except Exception as e:
            pytest.fail(f"Ошибка при вводе названия роли: {str(e)}. Скриншот: role_input_error.png")
    # Добавляем роль 8
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
        # ФИН
    with allure.step("Ввод названия роли"):
        try:
            time.sleep(2)
            role_input = WebDriverWait(driver, 25).until(
                EC.visibility_of_element_located((By.NAME, "name")))
            role_input.click()
            role_input.clear()
            role_input.send_keys("ФИН")
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
            element = driver.find_element(By.XPATH, '//span[contains(text(), "Вычисляемое")]/../span[1]')
            driver.execute_script("arguments[0].scrollIntoView();", element)
            element.click()
            element = driver.find_element(By.XPATH, "//span[contains(text(), 'Движение средств')]/../span[1]")
            driver.execute_script("arguments[0].scrollIntoView();", element)
            element.click()
            #"Сохранить"
            save_button = driver.find_element(By.XPATH, '//*[@id="main"]/div[4]/form/div[2]/div/div')
            driver.execute_script("arguments[0].scrollIntoView();", save_button)
            save_button.click()
        except Exception as e:
            pytest.fail(f"Ошибка при вводе названия роли: {str(e)}. Скриншот: role_input_error.png")
    # Добавляем роль 9
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
        # Операционист
    with allure.step("Ввод названия роли"):
        try:
            time.sleep(2)
            role_input = WebDriverWait(driver, 25).until(
                EC.visibility_of_element_located((By.NAME, "name")))
            role_input.click()
            role_input.clear()
            role_input.send_keys("Операционист")
            driver.find_element(By.XPATH, '//button[contains(text(), "Редактирование")]').click() #ПЕРВОЕ РЕДАКТИРОВАНИЕ
            driver.find_element(By.XPATH, '//span[contains(text(), "Редактирование основной информации экземпляров БП")]/preceding-sibling::span/input').click() #Первый чекбокс
            driver.find_element(By.XPATH, '//span[text()="Редактирование сущностей экземпляров БП"]/preceding-sibling::span//input').click() #Второй чекбокс
            driver.find_element(By.XPATH, '//span[text()="Смена этапов экземпляров БП"]/preceding-sibling::span').click() #Третий чекбокс
            driver.find_element(By.XPATH, '//*[@id="main"]/div[4]/form/div[1]/div/div[2]/div[3]/div[2]/div/button[3]').click() # ВТОРОЕ РЕДАКТИРОВАНИЕ
            driver.find_element(By.XPATH, '//span[text()="Редактирование основной информации задач"]/preceding-sibling::span').click() #Первый чекбокс
            driver.find_element(By.XPATH, '//span[contains(text(), "Редактирование сущностей задач")]/..').click() #Второй чекбокс
            driver.find_element(By.XPATH, '//*[@id="main"]/div[4]/form/div[1]/div/div[2]/div[4]/div[2]/div/button[2]').click() #ТРЕТИЙ ПРОСМОТР
            #Скрол и клик по нижним чекбоксам!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            element = driver.find_element(By.XPATH, '//span[text()="Редактирование тегов в экземплярах БП и задачах"]/preceding-sibling::span')
            driver.execute_script("arguments[0].scrollIntoView();", element)
            element.click()
            element = driver.find_element(By.XPATH, '//span[contains(text(), "Вычисляемое")]/../span[1]')
            driver.execute_script("arguments[0].scrollIntoView();", element)
            element.click()
            element = driver.find_element(By.XPATH, "//span[contains(text(), 'Движение средств')]/../span[1]")
            driver.execute_script("arguments[0].scrollIntoView();", element)
            element.click()
            #"Сохранить"
            save_button = driver.find_element(By.XPATH, '//*[@id="main"]/div[4]/form/div[2]/div/div')
            driver.execute_script("arguments[0].scrollIntoView();", save_button)
            save_button.click()
        except Exception as e:
            pytest.fail(f"Ошибка при вводе названия роли: {str(e)}. Скриншот: role_input_error.png")
    # Добавляем роль 10
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
        # ГД
    with allure.step("Ввод названия роли"):
        try:
            time.sleep(2)
            role_input = WebDriverWait(driver, 25).until(
                EC.visibility_of_element_located((By.NAME, "name")))
            role_input.click()
            role_input.clear()
            role_input.send_keys("ГД")
            driver.find_element(By.XPATH, '//button[contains(text(), "Редактирование")]').click() #ПЕРВОЕ РЕДАКТИРОВАНИЕ
            driver.find_element(By.XPATH, '//span[contains(text(), "Редактирование основной информации экземпляров БП")]/preceding-sibling::span/input').click() #Первый чекбокс
            driver.find_element(By.XPATH, '//span[text()="Редактирование сущностей экземпляров БП"]/preceding-sibling::span//input').click() #Второй чекбокс
            driver.find_element(By.XPATH, '//span[text()="Смена этапов экземпляров БП"]/preceding-sibling::span').click() #Третий чекбокс
            driver.find_element(By.XPATH, '//*[@id="main"]/div[4]/form/div[1]/div/div[2]/div[3]/div[2]/div/button[3]').click() # ВТОРОЕ РЕДАКТИРОВАНИЕ
            driver.find_element(By.XPATH, '//span[text()="Редактирование основной информации задач"]/preceding-sibling::span').click() #Первый чекбокс
            driver.find_element(By.XPATH, '//span[contains(text(), "Редактирование сущностей задач")]/..').click() #Второй чекбокс
            driver.find_element(By.XPATH, '//*[@id="main"]/div[4]/form/div[1]/div/div[2]/div[4]/div[2]/div/button[3]').click() #ТРЕТЬЕ РЕДАКТИРОВАНИЕ
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
            element = driver.find_element(By.XPATH, '//span[text()="Управление кадрами"]/..')
            driver.execute_script("arguments[0].scrollIntoView();", element)
            element.click()
            element = driver.find_element(By.XPATH, '//span[text()="Редактирование прав бизнес-ролей"]/preceding-sibling::span')
            driver.execute_script("arguments[0].scrollIntoView();", element)
            element.click()
            #"Сохранить"
            save_button = driver.find_element(By.XPATH, '//*[@id="main"]/div[4]/form/div[2]/div/div')
            driver.execute_script("arguments[0].scrollIntoView();", save_button)
            save_button.click()
        except Exception as e:
            pytest.fail(f"Ошибка при вводе названия роли: {str(e)}. Скриншот: role_input_error.png")
    # Добавляем роль 11
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
        # КД
    with allure.step("Ввод названия роли"):
        try:
            time.sleep(2)
            role_input = WebDriverWait(driver, 25).until(
                EC.visibility_of_element_located((By.NAME, "name")))
            role_input.click()
            role_input.clear()
            role_input.send_keys("КД")
            driver.find_element(By.XPATH, '//button[contains(text(), "Редактирование")]').click() #ПЕРВОЕ РЕДАКТИРОВАНИЕ
            driver.find_element(By.XPATH, '//span[contains(text(), "Редактирование основной информации экземпляров БП")]/preceding-sibling::span/input').click() #Первый чекбокс
            driver.find_element(By.XPATH, '//span[text()="Редактирование сущностей экземпляров БП"]/preceding-sibling::span//input').click() #Второй чекбокс
            driver.find_element(By.XPATH, '//span[text()="Смена этапов экземпляров БП"]/preceding-sibling::span').click() #Третий чекбокс
            driver.find_element(By.XPATH, '//*[@id="main"]/div[4]/form/div[1]/div/div[2]/div[3]/div[2]/div/button[3]').click() # ВТОРОЕ РЕДАКТИРОВАНИЕ
            driver.find_element(By.XPATH, '//span[text()="Редактирование основной информации задач"]/preceding-sibling::span').click() #Первый чекбокс
            driver.find_element(By.XPATH, '//span[contains(text(), "Редактирование сущностей задач")]/..').click() #Второй чекбокс
            driver.find_element(By.XPATH, '//*[@id="main"]/div[4]/form/div[1]/div/div[2]/div[4]/div[2]/div/button[3]').click() #ТРЕТЬЕ РЕДАКТИРОВАНИЕ
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
            element = driver.find_element(By.XPATH, '//span[text()="Управление кадрами"]/..')
            driver.execute_script("arguments[0].scrollIntoView();", element)
            element.click()
            element = driver.find_element(By.XPATH, '//span[text()="Редактирование прав бизнес-ролей"]/preceding-sibling::span')
            driver.execute_script("arguments[0].scrollIntoView();", element)
            element.click()
            #"Сохранить"
            save_button = driver.find_element(By.XPATH, '//*[@id="main"]/div[4]/form/div[2]/div/div')
            driver.execute_script("arguments[0].scrollIntoView();", save_button)
            save_button.click()
        except Exception as e:
            pytest.fail(f"Ошибка при вводе названия роли: {str(e)}. Скриншот: role_input_error.png")
    # Добавляем роль 12
    with allure.step("добавляем роль"):
        try:
            role_field = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="main"]/div[3]/form/div[1]/div/div/div/div[1]/div')))
            role_field.click()
            add_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.MuiButton-contained.css-lmp1wz')))
            add_button.click()
        except Exception as e:
            pytest.fail(f"Ошибка : {str(e)}")
        # ДЭ
    with allure.step("Ввод названия роли"):
        try:
            time.sleep(2)
            role_input = WebDriverWait(driver, 25).until(
                EC.visibility_of_element_located((By.NAME, "name")))
            role_input.click()
            role_input.clear()
            role_input.send_keys("ДЭ")
            driver.find_element(By.XPATH, '//button[contains(text(), "Редактирование")]').click() #ПЕРВОЕ РЕДАКТИРОВАНИЕ
            driver.find_element(By.XPATH, '//span[contains(text(), "Редактирование основной информации экземпляров БП")]/preceding-sibling::span/input').click() #Первый чекбокс
            driver.find_element(By.XPATH, '//span[text()="Редактирование сущностей экземпляров БП"]/preceding-sibling::span//input').click() #Второй чекбокс
            driver.find_element(By.XPATH, '//span[text()="Смена этапов экземпляров БП"]/preceding-sibling::span').click() #Третий чекбокс
            driver.find_element(By.XPATH, '//*[@id="main"]/div[4]/form/div[1]/div/div[2]/div[3]/div[2]/div/button[3]').click() # ВТОРОЕ РЕДАКТИРОВАНИЕ
            driver.find_element(By.XPATH, '//span[text()="Редактирование основной информации задач"]/preceding-sibling::span').click() #Первый чекбокс
            driver.find_element(By.XPATH, '//span[contains(text(), "Редактирование сущностей задач")]/..').click() #Второй чекбокс
            driver.find_element(By.XPATH, '//*[@id="main"]/div[4]/form/div[1]/div/div[2]/div[4]/div[2]/div/button[3]').click() #ТРЕТЬЕ РЕДАКТИРОВАНИЕ
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
    # Добавляем роль 13
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
        # СРК
    with allure.step("Ввод названия роли"):
        try:
            role_input = WebDriverWait(driver, 15).until(
                EC.visibility_of_element_located((By.NAME, "name")))
            role_input.click()
            role_input.clear()
            role_input.send_keys("СРК")
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
            element = driver.find_element(By.XPATH, '//span[contains(text(), "Вычисляемое")]/../span[1]')
            driver.execute_script("arguments[0].scrollIntoView();", element)
            element.click()
            #"Сохранить"
            save_button = driver.find_element(By.XPATH, '//*[@id="main"]/div[4]/form/div[2]/div/div')
            driver.execute_script("arguments[0].scrollIntoView();", save_button)
            save_button.click()
        except Exception as e:
            pytest.fail(f"Ошибка при вводе названия роли: {str(e)}. Скриншот: role_input_error.png")
    # Добавляем роль 14
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
        # МП
    with allure.step("Ввод названия роли"):
        try:
            role_input = WebDriverWait(driver, 15).until(
                EC.visibility_of_element_located((By.NAME, "name")))
            role_input.click()
            role_input.clear()
            role_input.send_keys("МП")
            driver.find_element(By.XPATH, '//button[contains(text(), "Редактирование")]').click() #ПЕРВОЕ РЕДАКТИРОВАНИЕ
            driver.find_element(By.XPATH, '//span[contains(text(), "Редактирование основной информации экземпляров БП")]/preceding-sibling::span/input').click() #Первый чекбокс
            driver.find_element(By.XPATH, '//span[text()="Редактирование сущностей экземпляров БП"]/preceding-sibling::span//input').click() #Второй чекбокс
            driver.find_element(By.XPATH, '//span[text()="Смена этапов экземпляров БП"]/preceding-sibling::span').click() #Третий чекбокс
            driver.find_element(By.XPATH, '//span[contains(@class, "MuiTypography-body1") and contains(text(), "Редактирование участников")]/preceding-sibling::span[contains(@class, "MuiCheckbox-root")]').click() #Четвертый чекбокс
            driver.find_element(By.XPATH, '//*[@id="main"]/div[4]/form/div[1]/div/div[2]/div[3]/div[2]/div/button[3]').click() # ВТОРОЕ РЕДАКТИРОВАНИЕ
            driver.find_element(By.XPATH, '//span[text()="Редактирование основной информации задач"]/preceding-sibling::span').click() #Первый чекбокс
            driver.find_element(By.XPATH, '//span[contains(text(), "Редактирование сущностей задач")]/..').click() #Второй чекбокс
            #Скрол и клик по нижним чекбоксам!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            element = driver.find_element(By.XPATH, '//span[text()="Редактирование тегов в экземплярах БП и задачах"]/preceding-sibling::span')
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
    # Добавляем роль 15
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
        # Мп
    with allure.step("Ввод названия роли"):
        try:
            role_input = WebDriverWait(driver, 15).until(
                EC.visibility_of_element_located((By.NAME, "name")))
            role_input.click()
            role_input.clear()
            role_input.send_keys("Мп")
            driver.find_element(By.XPATH, '//button[contains(text(), "Редактирование")]').click() #ПЕРВОЕ РЕДАКТИРОВАНИЕ
            driver.find_element(By.XPATH, '//span[contains(text(), "Редактирование основной информации экземпляров БП")]/preceding-sibling::span/input').click() #Первый чекбокс
            driver.find_element(By.XPATH, '//span[text()="Редактирование сущностей экземпляров БП"]/preceding-sibling::span//input').click() #Второй чекбокс
            driver.find_element(By.XPATH, '//span[text()="Смена этапов экземпляров БП"]/preceding-sibling::span').click() #Третий чекбокс
            driver.find_element(By.XPATH, '//span[contains(@class, "MuiTypography-body1") and contains(text(), "Редактирование участников")]/preceding-sibling::span[contains(@class, "MuiCheckbox-root")]').click() #Четвертый чекбокс
            driver.find_element(By.XPATH, '//*[@id="main"]/div[4]/form/div[1]/div/div[2]/div[3]/div[2]/div/button[3]').click() # ВТОРОЕ РЕДАКТИРОВАНИЕ
            driver.find_element(By.XPATH, '//span[text()="Редактирование основной информации задач"]/preceding-sibling::span').click() #Первый чекбокс
            driver.find_element(By.XPATH, '//span[contains(text(), "Редактирование сущностей задач")]/..').click() #Второй чекбокс
            driver.find_element(By.XPATH, '//*[@id="main"]/div[4]/form/div[1]/div/div[2]/div[4]/div[2]/div/button[3]').click() #ТРЕТЬЕ РЕДАКТИРОВАНИЕ
            #Скрол и клик по нижним чекбоксам!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            element = driver.find_element(By.XPATH, '//span[text()="Редактирование тегов в экземплярах БП и задачах"]/preceding-sibling::span')
            driver.execute_script("arguments[0].scrollIntoView();", element)
            element.click()
            #"Сохранить"
            save_button = driver.find_element(By.XPATH, '//*[@id="main"]/div[4]/form/div[2]/div/div')
            driver.execute_script("arguments[0].scrollIntoView();", save_button)
            save_button.click()
        except Exception as e:
            pytest.fail(f"Ошибка при вводе названия роли: {str(e)}. Скриншот: role_input_error.png")
    # Добавляем роль 16
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
        # АДМ
    with allure.step("Ввод названия роли"):
        try:
            role_input = WebDriverWait(driver, 15).until(
                EC.visibility_of_element_located((By.NAME, "name")))
            role_input.click()
            role_input.clear()
            role_input.send_keys("АДМ")
            driver.find_element(By.XPATH, '//button[contains(text(), "Редактирование")]').click() #ПЕРВОЕ РЕДАКТИРОВАНИЕ
            driver.find_element(By.XPATH, '//span[contains(text(), "Редактирование основной информации экземпляров БП")]/preceding-sibling::span/input').click() #Первый чекбокс
            driver.find_element(By.XPATH, '//span[text()="Редактирование сущностей экземпляров БП"]/preceding-sibling::span//input').click() #Второй чекбокс
            driver.find_element(By.XPATH, '//span[text()="Смена этапов экземпляров БП"]/preceding-sibling::span').click() #Третий чекбокс
            driver.find_element(By.XPATH, '//span[contains(@class, "MuiTypography-body1") and contains(text(), "Редактирование участников")]/preceding-sibling::span[contains(@class, "MuiCheckbox-root")]').click() #Четвертый чекбокс
            driver.find_element(By.XPATH, '//*[@id="main"]/div[4]/form/div[1]/div/div[2]/div[3]/div[2]/div/button[3]').click() # ВТОРОЕ РЕДАКТИРОВАНИЕ
            driver.find_element(By.XPATH, '//span[text()="Редактирование основной информации задач"]/preceding-sibling::span').click() #Первый чекбокс
            driver.find_element(By.XPATH, '//span[contains(text(), "Редактирование сущностей задач")]/..').click() #Второй чекбокс
            driver.find_element(By.XPATH, '//*[@id="main"]/div[4]/form/div[1]/div/div[2]/div[4]/div[2]/div/button[3]').click() #ТРЕТЬЕ РЕДАКТИРОВАНИЕ
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
            element = driver.find_element(By.XPATH, '//span[text()="Управление кадрами"]/..')
            driver.execute_script("arguments[0].scrollIntoView();", element)
            element.click()
            element = driver.find_element(By.XPATH, '//span[text()="Редактирование прав бизнес-ролей"]/preceding-sibling::span')
            driver.execute_script("arguments[0].scrollIntoView();", element)
            element.click()
            #"Сохранить"
            save_button = driver.find_element(By.XPATH, '//*[@id="main"]/div[4]/form/div[2]/div/div')
            driver.execute_script("arguments[0].scrollIntoView();", save_button)
            save_button.click()
        except Exception as e:
            pytest.fail(f"Ошибка при вводе названия роли: {str(e)}. Скриншот: role_input_error.png")
    time.sleep(5)