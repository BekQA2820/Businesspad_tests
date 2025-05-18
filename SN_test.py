import pyautogui
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
            driver.get("https://testbp1.business-pad.com/")
            # Вход в систему
            driver.find_element(By.XPATH, '//*[@id=":r0:"]').send_keys("adminbp")
            driver.find_element(By.XPATH, '//*[@id=":r1:"]').send_keys("") # вставь пароль
            driver.find_element(By.XPATH, '//*[@id="root"]/div/main/div/div/div/div[2]/div/form/div/div[4]').click()
            time.sleep(2)
            driver.get("https://testbp1.business-pad.com/deal/1530?view=tabs&tab=1")
        except Exception as e:
            print(f"Ошибка авторизации: {str(e)}")

    #Экземпляр::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    #Экземпляр::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    with allure.step("Клик по Процессу"):
        try:
            process_icon = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[1]/div/div[2]/a[3]')))
            process_icon.click()
            sdelka = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//p[contains(@class, 'MuiTypography-root') and contains(text(), 'Сделка')]")))
            sdelka.click()
            plus = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button.MuiButton-containedSecondary")))
            plus.click() #111111111111111111
            input_field = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.NAME, "name")))
            input_field.click()  # Фокусируемся на элементе
            input_field.send_keys("Э55-24 ПНОС CHEMPACK Катализатор гидрирования")
            choose = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/div[1]/div/div[2]/div/div[3]/div[2]/div/div[1]/div/div/div/div/div/div')))
            choose.click()
            time.sleep(1)
            ActionChains(driver).move_to_element(choose).move_by_offset(0, 40).click().perform()
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", choose)
            choose = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/div[1]/div/div[2]/div/div[3]/div[2]/div/div[1]/div/div/div/div/div/div')))
            choose.click()
            ActionChains(driver).move_to_element(choose).move_by_offset(0, 40).click().perform()
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", choose)
            description_field = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "textarea[placeholder='Введите описание']")))
            description_field.click()  # Фокусируемся на элементе
            description_field.send_keys("Каталитическая система гидрирования сероорганических соединений для 21-DC-101 тит. 521")
            number_field = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='Введите номер']")))
            number_field.click()  # Фокусируемся на элементе
            number_field.send_keys("Э55-24")
            money = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="main"]/div[1]/div/div[2]/div/div[4]/div[2]/div/div[1]/div/div/div/div/div/div/button')))
            money.click()
            ActionChains(driver).move_to_element(money).move_by_offset(0, 40).click().perform()
            money.click()
            ActionChains(driver).move_to_element(money).move_by_offset(0, 40).click().perform()
            money.click()
            ActionChains(driver).move_to_element(money).move_by_offset(0, 60).click().perform()
            money.click()
            ActionChains(driver).move_to_element(money).move_by_offset(0, 140).click().perform()
            time.sleep(0.6)
            driver.find_element(By.XPATH, "//button[contains(text(), 'Далее')]").click()
            attach_screenshot(driver, "После клика по Процессам")
        except Exception as e:
            print(f"Ошибка при клике по Процессам: {e}")
        with allure.step("пошло"):
            try:
                #!!!!!!!!
                sdelka = wait.until(EC.presence_of_element_located((By.XPATH, "//h2[text()='Э55-24 ПНОС CHEMPACK Катализатор гидрирования']")))
                sdelka.click()
                open= wait.until(EC.presence_of_element_located((By.XPATH, "//button[text()='Открыть полностью']")))
                open.click()
                button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testid='AddIcon']")))
                button.click()
                #PINGXIANG CHEMPACK IMP&EXP
                company = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Выберите компанию"]')))
                company.click()
                company.send_keys('PINGXIANG CHEMPACK IMP&EXP CO.,Ltd.(нерезидент)')
                ActionChains(driver).move_to_element(company).move_by_offset(0, 40).click().perform()
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", company)
                #КОНТРАГЕНТЫ!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                form = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Выберите формы взаимодействия"]')))
                form.click()
                form.send_keys('Поставщик')
                ActionChains(driver).move_to_element(form).move_by_offset(0, 40).click().perform()
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", form)
                form = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Выберите формы взаимодействия"]')))
                form.click()
                form.send_keys('Производитель')
                ActionChains(driver).move_to_element(form).move_by_offset(0, 40).click().perform()
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", form)
                form = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Выберите формы взаимодействия"]')))
                form.click()
                form.send_keys('Грузоотправитель')
                ActionChains(driver).move_to_element(form).move_by_offset(0, 40).click().perform()
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", form)
                button = driver.find_element(By.CSS_SELECTOR, "button.MuiLoadingButton-root")
                button.click()
                #Васко, ООО
                button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testid='AddIcon']")))
                button.click()
                company = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Выберите компанию"]')))
                company.click()
                company.send_keys('Васко, ООО')
                ActionChains(driver).move_to_element(company).move_by_offset(0, 40).click().perform()
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", company)
                form = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Выберите формы взаимодействия"]')))
                form.click()
                form.send_keys('Брокер')
                ActionChains(driver).move_to_element(form).move_by_offset(0, 40).click().perform()
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", form)
                button = driver.find_element(By.CSS_SELECTOR, "button.MuiLoadingButton-root")
                button.click()
                #ЛУКОЙЛ-Пермнефтеоргсинтез, ООО
                button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testid='AddIcon']")))
                button.click()
                company = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Выберите компанию"]')))
                company.click()
                company.send_keys('ЛУКОЙЛ-Пермнефтеоргсинтез, ООО')
                ActionChains(driver).move_to_element(company).move_by_offset(0, 40).click().perform()
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", company)
                form = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Выберите формы взаимодействия"]')))
                form.click()
                form.send_keys('Покупатель')
                ActionChains(driver).move_to_element(form).move_by_offset(0, 40).click().perform()
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", form)
                form = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Выберите формы взаимодействия"]')))
                form.click()
                form.send_keys('Грузополучатель')
                ActionChains(driver).move_to_element(form).move_by_offset(0, 40).click().perform()
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", form)
                button = driver.find_element(By.CSS_SELECTOR, "button.MuiLoadingButton-root")
                button.click()
            except Exception as e:
                print(f"Ошибка при клике по Процессам: {e}")
        with allure.step("товар"):
            try:
                #!!!!!!!!
                tovaru = wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Товары')]")))
                tovaru.click()
                plus= wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button.css-cdp6mq")))
                plus.click()
                input_field = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='Выберите артикул, наименование']")))
                input_field.click()
                input_field.send_keys('PuriCat ')
                time.sleep(0.8)
                ActionChains(driver).move_to_element(input_field).move_by_offset(0, 40).click().perform()
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", input_field)
                input_field2 = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='Выберите производителя']")))
                input_field2.click()
                ActionChains(driver).move_to_element(input_field2).move_by_offset(0, 40).click().perform()
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", input_field2)
                quantity_field = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='Количество']"))
                )
                quantity_field.click()
                quantity_field.send_keys('9 250')
                date_field = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='dd.mm.yyyy']"))
                )
                date_field.click()
                date_field.send_keys('12.05.2025')
                unit_field = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='Единица']"))
                )
                unit_field.click()
                unit_field.send_keys('кг')
                ActionChains(driver).move_to_element(unit_field).move_by_offset(0, 40).click().perform()
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", unit_field)
                price_field = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='Введите цену']"))
                )
                price_field.click()
                price_field.send_keys('35.6811')
                currency_field = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='Выберите валюту']"))
                )
                currency_field.click()
                currency_field.send_keys('CNY')
                ActionChains(driver).move_to_element(currency_field).move_by_offset(0, 40).click().perform()
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", currency_field)
                counterparty_field = WebDriverWait(driver, 15).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='Выберите контрагента']"))
                )
                counterparty_field.click()
                ActionChains(driver).move_to_element(counterparty_field).move_by_offset(0, 40).click().perform()
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", counterparty_field)
                #!!!!!!!!!!!!!!!!!!!!!!!!!
                chanel_field = WebDriverWait(driver, 15).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'input.MuiInputBase-input[placeholder="Выберите канал оплаты поставщику "]'))
                )
                chanel_field.click()
                ActionChains(driver).move_to_element(chanel_field).move_by_offset(0, 40).click().perform()
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", chanel_field)
                dogovor_field = WebDriverWait(driver, 15).until(
                    EC.element_to_be_clickable((By.XPATH, '//input[@placeholder="Укажите условие оплаты по договору"]'))
                )
                dogovor_field.click()
                ActionChains(driver).move_to_element(dogovor_field).move_by_offset(0, 40).click().perform()
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", dogovor_field)
                gruz_field = WebDriverWait(driver, 15).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'input.MuiAutocomplete-input[placeholder="Выберите грузоотправителя"]'))
                )
                gruz_field.click()
                ActionChains(driver).move_to_element(gruz_field).move_by_offset(0, 40).click().perform()
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", gruz_field)
                checkbox = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((
                        By.XPATH,
                        '//span[contains(text(), "Создать симметричный товар")]/ancestor::label//span[contains(@class, "MuiButtonBase-root")]'
                    )))
                checkbox.click()
                button = driver.find_element(By.XPATH, '//button[contains(., "Добавить")]')
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
                button.click()
                new = wait.until(EC.presence_of_element_located((By.XPATH,'//input[@placeholder="Выберите статью финансовой операции"]')))
                new.click()
                new.send_keys('Таможенная пошлина')
                ActionChains(driver).move_to_element(new).move_by_offset(0, 40).click().perform()
                #!!!!!!!!!!!!!!!!!!!!!!
                save_field = WebDriverWait(driver, 15).until(
                    EC.element_to_be_clickable((By.XPATH, '//button[contains(., "Сохранить")]')))
                save_field.click()
                time.sleep(3)
                input_element = driver.find_element(
                    By.XPATH, '/html/body/div/div/main/div[2]/form/div[1]/div/div[4]/div[2]/div[1]/div/div/input')
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", input_element)
                ActionChains(driver).move_to_element(input_element).click().perform()
                input_element.send_keys(Keys.CONTROL + "a")  # Выделить всё (Win/Linux)
                input_element.send_keys(Keys.DELETE)
                input_element.send_keys('81.8273')
                input_element.send_keys(Keys.ENTER)
                save_field = WebDriverWait(driver, 15).until(
                    EC.element_to_be_clickable((By.XPATH, '//button[contains(., "Сохранить")]')))
                save_field.click()
                driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
            except Exception as e:
                print(f"Ошибка при клике по Процессам: {e}")
        with allure.step("Финансы"):
            try:
                element = wait.until(EC.presence_of_element_located((By.XPATH, "//button[text()='Финансы']")))
                element.click()
                time.sleep(2)
                buttons = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'button.MuiIconButton-root.css-1yxmbwk')))
                buttons[3].click() #12345
                delete_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//li[contains(text(), "Удалить")]')))
                delete_button.click()
                time.sleep(1)
                buttons = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'button.MuiIconButton-root.css-1yxmbwk')))
                buttons[5].click() #12345
                delete_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//li[contains(text(), "Удалить")]')))
                delete_button.click()
                time.sleep(1)
                buttons = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'button.MuiIconButton-root.css-1yxmbwk')))
                buttons[3].click() #12345
                delete_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//li[contains(text(), "Удалить")]')))
                delete_button.click()
            except Exception as e:
                attach_screenshot(driver, "Ошибка при Финансах")
            print(f"Ошибка при ри Финансах: {e}")

        with allure.step("Финансы 1"):
            try:
                time.sleep(0.7)
                button = driver.find_element(By.CSS_SELECTOR, "button.css-cdp6mq")
                button.click()
                #!!!!!!
                time.sleep(1)
                element = driver.find_element(By.CSS_SELECTOR,
                                              'div[name="baseFinancialOperation"] input[placeholder="Выберите статью финансовой операции"]')
                element.click()
                element.send_keys('Покупка товара/услуги')
                ActionChains(driver).move_to_element(element).move_by_offset(0, 40).click().perform()
                input_field = driver.find_element(
                    By.CSS_SELECTOR,
                    'div[name="cashChannel"] input[placeholder="Выберите финансовый канал"]'
                )
                input_field.click()
                ActionChains(driver).move_to_element(input_field).move_by_offset(0, 40).click().perform()
                price_input = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Введите число"]'))
                )
                driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", price_input)
                price_input.send_keys("35.68108")
                time.sleep(0.5)
                price_input1 = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '/html/body/div/div/main/div[2]/div[2]/form/div/div[3]/div[2]/div/div[3]/div/div[1]/div/div/input'))
                )
                driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", price_input1)
                price_input1.send_keys("4625")
                #!~!!!!
                unit_field = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'div[name="measurementUnit"] input'))
                )
                unit_field.send_keys("кг")
                ActionChains(driver).move_to_element(unit_field).move_by_offset(0, 40).click().perform()
                currency_field = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[name="currencyUnit"] input'))
                )
                currency_field.click()
                currency_field.send_keys('CNY')
                ActionChains(driver).move_to_element(currency_field).move_by_offset(0, 40).click().perform()
                switch = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH,
                                                '//label[.//span[text()="Цена с НДС"]]'))
                )
                switch.click()
                tax_field = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[name="tax"] input'))
                )
                tax_field.click()
                tax_field.send_keys('Без')
                ActionChains(driver).move_to_element(tax_field).move_by_offset(0, 40).click().perform()
                status_field = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[name="status"] input'))
                )
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", status_field)
                status_field.send_keys("черновик")
                ActionChains(driver).move_to_element(status_field).move_by_offset(0, 30).click().perform()
                status_field.send_keys(Keys.ENTER)
                product_field = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[name="productUnits"] input'))
                )
                product_field.click()
                ActionChains(driver).move_to_element(product_field).move_by_offset(0, 40).click().perform()
                button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Добавить')]"))
                )
                button.click()
            except Exception as e:
                attach_screenshot(driver, "Ошибка при Финансах")
                print(f"Ошибка при ри Финансах: {e}")
        with allure.step("Продажа товара/услуги"):
            try:

                time.sleep(0.7)
                button = driver.find_element(By.CSS_SELECTOR, "button.css-cdp6mq")
                button.click()
                #!!!!!!
                time.sleep(1)
                element = driver.find_element(By.CSS_SELECTOR,
                                              'div[name="baseFinancialOperation"] input[placeholder="Выберите статью финансовой операции"]')
                element.click()
                element.send_keys('Продажа товара/услуги')
                ActionChains(driver).move_to_element(element).move_by_offset(0, 40).click().perform()
                input_field = driver.find_element(
                    By.CSS_SELECTOR,
                    'div[name="cashChannel"] input[placeholder="Выберите финансовый канал"]'
                )
                input_field.click()
                ActionChains(driver).move_to_element(input_field).move_by_offset(0, 40).click().perform()
                price_input = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Введите число"]'))
                )
                driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", price_input)
                price_input.send_keys("81.8273")
                time.sleep(0.5)
                price_input1 = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '/html/body/div/div/main/div[2]/div[2]/form/div/div[3]/div[2]/div/div[3]/div/div[1]/div/div/input'))
                )
                driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", price_input1)
                price_input1.send_keys("9 250")
                #!~!!!!
                unit_field = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'div[name="measurementUnit"] input'))
                )
                unit_field.send_keys("кг")
                ActionChains(driver).move_to_element(unit_field).move_by_offset(0, 40).click().perform()
                currency_field = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[name="currencyUnit"] input'))
                )
                currency_field.click()
                currency_field.send_keys('CNY')
                ActionChains(driver).move_to_element(currency_field).move_by_offset(0, 40).click().perform()
                switch = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH,
                                                '//label[.//span[text()="Цена с НДС"]]'))
                )
                switch.click()
                tax_field = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[name="tax"] input'))
                )
                tax_field.click()
                tax_field.send_keys('20')
                ActionChains(driver).move_to_element(tax_field).move_by_offset(0, 40).click().perform()
                radio = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//span[contains(@class, "MuiTypography-body1") and text()="Доходная"]/..'))
                )
                radio.click()
                status_field = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[name="status"] input'))
                )
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", status_field)
                status_field.send_keys("черновик")
                ActionChains(driver).move_to_element(status_field).move_by_offset(0, 30).click().perform()
                status_field.send_keys(Keys.ENTER)
                product_field = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[name="productUnits"] input'))
                )
                product_field.click()
                ActionChains(driver).move_to_element(product_field).move_by_offset(0, 40).click().perform()
                button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Добавить')]"))
                )
                button.click()
            except Exception as e:
                attach_screenshot(driver, "Ошибка при Финансах")
            print(f"Ошибка при ри Финансах: {e}")

        with allure.step("НДС+Таможенный сбор"):
            try:

                time.sleep(0.7)
                button = driver.find_element(By.CSS_SELECTOR, "button.css-cdp6mq")
                button.click()
                #!!!!!!
                time.sleep(1)
                element = driver.find_element(By.CSS_SELECTOR,
                                              'div[name="baseFinancialOperation"] input[placeholder="Выберите статью финансовой операции"]')
                element.click()
                element.send_keys('НДС+Таможенный сбор')
                ActionChains(driver).move_to_element(element).move_by_offset(0, 40).click().perform()
                input_field = driver.find_element(
                    By.CSS_SELECTOR,
                    'div[name="cashChannel"] input[placeholder="Выберите финансовый канал"]'
                )
                input_field.click()
                ActionChains(driver).move_to_element(input_field).move_by_offset(0, 40).click().perform()
                price_input = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Введите число"]'))
                )
                driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", price_input)
                price_input.send_keys("76690")
                time.sleep(0.5)
                price_input1 = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '/html/body/div/div/main/div[2]/div[2]/form/div/div[3]/div[2]/div/div[3]/div/div[1]/div/div/input'))
                )
                driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", price_input1)
                price_input1.send_keys("1")
                #!~!!!!
                unit_field = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'div[name="measurementUnit"] input'))
                )
                unit_field.send_keys("услуга")
                ActionChains(driver).move_to_element(unit_field).move_by_offset(0, 40).click().perform()
                currency_field = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[name="currencyUnit"] input'))
                )
                currency_field.click()
                currency_field.send_keys('CNY')
                ActionChains(driver).move_to_element(currency_field).move_by_offset(0, 40).click().perform()
                switch = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH,
                                                '//label[.//span[text()="Цена с НДС"]]'))
                )
                switch.click()
                tax_field = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[name="tax"] input'))
                )
                tax_field.click()
                tax_field.send_keys('без')
                ActionChains(driver).move_to_element(tax_field).move_by_offset(0, 40).click().perform()
                status_field = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[name="status"] input'))
                )
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", status_field)
                status_field.send_keys("черновик")
                ActionChains(driver).move_to_element(status_field).move_by_offset(0, 30).click().perform()
                status_field.send_keys(Keys.ENTER)
                product_field = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[name="productUnits"] input'))
                )
                product_field.click()
                ActionChains(driver).move_to_element(product_field).move_by_offset(0, 40).click().perform()
                button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Добавить')]"))
                )
                button.click()
            except Exception as e:
                attach_screenshot(driver, "Ошибка при Финансах")
                print(f"Ошибка при ри Финансах: {e}")
        with allure.step("Транспорт после границы"):
            try:

                time.sleep(0.7)
                button = driver.find_element(By.CSS_SELECTOR, "button.css-cdp6mq")
                button.click()
                #!!!!!!
                time.sleep(1)
                element = driver.find_element(By.CSS_SELECTOR,
                                              'div[name="baseFinancialOperation"] input[placeholder="Выберите статью финансовой операции"]')
                element.click()
                element.send_keys('Транспорт после границы')
                ActionChains(driver).move_to_element(element).move_by_offset(0, 40).click().perform()
                input_field = driver.find_element(
                    By.CSS_SELECTOR,
                    'div[name="cashChannel"] input[placeholder="Выберите финансовый канал"]'
                )
                input_field.click()
                ActionChains(driver).move_to_element(input_field).move_by_offset(0, 40).click().perform()
                price_input = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Введите число"]'))
                )
                driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", price_input)
                price_input.send_keys("3100")
                time.sleep(0.5)
                price_input1 = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '/html/body/div/div/main/div[2]/div[2]/form/div/div[3]/div[2]/div/div[3]/div/div[1]/div/div/input'))
                )
                driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", price_input1)
                price_input1.send_keys("1")
                #!~!!!!
                unit_field = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'div[name="measurementUnit"] input'))
                )
                unit_field.send_keys("услуга")
                ActionChains(driver).move_to_element(unit_field).move_by_offset(0, 40).click().perform()
                currency_field = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[name="currencyUnit"] input'))
                )
                currency_field.click()
                currency_field.send_keys('EUR')
                ActionChains(driver).move_to_element(currency_field).move_by_offset(0, 40).click().perform()
                switch = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH,
                                                '//label[.//span[text()="Цена с НДС"]]'))
                )
                switch.click()
                tax_field = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[name="tax"] input'))
                )
                tax_field.click()
                tax_field.send_keys('без')
                ActionChains(driver).move_to_element(tax_field).move_by_offset(0, 40).click().perform()
                status_field = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[name="status"] input'))
                )
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", status_field)
                status_field.send_keys("черновик")
                ActionChains(driver).move_to_element(status_field).move_by_offset(0, 30).click().perform()
                status_field.send_keys(Keys.ENTER)
                product_field = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[name="productUnits"] input'))
                )
                product_field.click()
                ActionChains(driver).move_to_element(product_field).move_by_offset(0, 40).click().perform()
                button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Добавить')]"))
                )
                button.click()
            except Exception as e:
                attach_screenshot(driver, "Ошибка при Финансах")
                print(f"Ошибка при ри Финансах: {e}")
        with allure.step("Покупка товара/услуги"):
            try:

                time.sleep(0.7)
                button = driver.find_element(By.CSS_SELECTOR, "button.css-cdp6mq")
                button.click()
                #!!!!!!
                time.sleep(1)
                element = driver.find_element(By.CSS_SELECTOR,
                                              'div[name="baseFinancialOperation"] input[placeholder="Выберите статью финансовой операции"]')
                element.click()
                element.send_keys('Покупка товара/услуги')
                ActionChains(driver).move_to_element(element).move_by_offset(0, 40).click().perform()
                input_field = driver.find_element(
                    By.CSS_SELECTOR,
                    'div[name="cashChannel"] input[placeholder="Выберите финансовый канал"]'
                )
                input_field.click()
                ActionChains(driver).move_to_element(input_field).move_by_offset(0, 40).click().perform()
                price_input = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Введите число"]'))
                )
                driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", price_input)
                price_input.send_keys("35.68108")
                time.sleep(0.5)
                price_input1 = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '/html/body/div/div/main/div[2]/div[2]/form/div/div[3]/div[2]/div/div[3]/div/div[1]/div/div/input'))
                )
                driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", price_input1)
                price_input1.send_keys("4625")
                #!~!!!!
                unit_field = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'div[name="measurementUnit"] input'))
                )
                unit_field.send_keys("кг")
                ActionChains(driver).move_to_element(unit_field).move_by_offset(0, 40).click().perform()
                currency_field = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[name="currencyUnit"] input'))
                )
                currency_field.click()
                currency_field.send_keys('CNY')
                ActionChains(driver).move_to_element(currency_field).move_by_offset(0, 40).click().perform()
                switch = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH,
                                                '//label[.//span[text()="Цена с НДС"]]'))
                )
                switch.click()
                tax_field = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[name="tax"] input'))
                )
                tax_field.click()
                tax_field.send_keys('без')
                ActionChains(driver).move_to_element(tax_field).move_by_offset(0, 40).click().perform()
                status_field = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[name="status"] input'))
                )
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", status_field)
                status_field.send_keys("черновик")
                ActionChains(driver).move_to_element(status_field).move_by_offset(0, 30).click().perform()
                status_field.send_keys(Keys.ENTER)
                product_field = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[name="productUnits"] input'))
                )
                product_field.click()
                ActionChains(driver).move_to_element(product_field).move_by_offset(0, 40).click().perform()
                button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Добавить')]"))
                )
                button.click()
            except Exception as e:
                attach_screenshot(driver, "Ошибка при Финансах")
                print(f"Ошибка при ри Финансах: {e}")
        with allure.step("Финансы БДР"):
            try:
                #БДР
                button = driver.find_element(By.CSS_SELECTOR, "button.css-cdp6mq")
                button.click()
                button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[text()='Движение средств']")))
                button.click()
                element = driver.find_element(By.CSS_SELECTOR, "input[placeholder='Выберите операцию']")
                element.click()
                element.send_keys('Комиссии банк')
                ActionChains(driver).move_to_element(element).move_by_offset(0, 40).click().perform()
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
                field = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "input[value='БДС']"))
                )
                field.click()
                ActionChains(driver).move_to_element(field).move_by_offset(0, 60).click().perform()
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", field)
                field = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='Введите значение']")))
                field.click()
                field.send_keys('120')
                field = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.NAME, "documentNumber")))
                field.send_keys('33')
                field.click()
                date_field = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "input[required][placeholder^='dd']")))
                date_field.click()
                ActionChains(driver).move_to_element(date_field).move_by_offset(0, 40).click().perform()
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", date_field)
                date_field.send_keys('12052025')
                currency_field = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='Выберите валюту']")))
                currency_field.click()
                currency_field.send_keys('CNY')
                ActionChains(driver).move_to_element(currency_field).move_by_offset(0, 50).click().perform()
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", currency_field)
                checkbox = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "span.css-1bppi3i")))
                checkbox.click()
                date_field = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/main/div[2]/div[2]/form/div/div[4]/div[11]/div/div/input")))
                date_field.click()
                date_field.send_keys('12052025')
                button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Добавить')]"))
                )
                button.click()
            except Exception as e:
                attach_screenshot(driver, "Ошибка при Финансах")
                print(f"Ошибка при ри Финансах: {e}")
        with allure.step("Транспорт до границы"):
            try:
                time.sleep(0.7)
                button = driver.find_element(By.CSS_SELECTOR, "button.css-cdp6mq")
                button.click()
                #!!!!!!
                time.sleep(1)
                element = driver.find_element(By.CSS_SELECTOR,
                                              'div[name="baseFinancialOperation"] input[placeholder="Выберите статью финансовой операции"]')
                element.click()
                element.send_keys('Транспорт до границы')
                ActionChains(driver).move_to_element(element).move_by_offset(0, 40).click().perform()
                input_field = driver.find_element(
                    By.CSS_SELECTOR,
                    'div[name="cashChannel"] input[placeholder="Выберите финансовый канал"]'
                )
                input_field.click()
                ActionChains(driver).move_to_element(input_field).move_by_offset(0, 40).click().perform()
                price_input = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Введите число"]'))
                )
                driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", price_input)
                price_input.send_keys("2000")
                time.sleep(0.5)
                price_input1 = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '/html/body/div/div/main/div[2]/div[2]/form/div/div[3]/div[2]/div/div[3]/div/div[1]/div/div/input'))
                )
                driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", price_input1)
                price_input1.send_keys("1")
                #!~!!!!
                unit_field = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'div[name="measurementUnit"] input'))
                )
                unit_field.send_keys("услуга")
                ActionChains(driver).move_to_element(unit_field).move_by_offset(0, 40).click().perform()
                currency_field = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[name="currencyUnit"] input'))
                )
                currency_field.click()
                currency_field.send_keys('EUR')
                ActionChains(driver).move_to_element(currency_field).move_by_offset(0, 40).click().perform()
                switch = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH,
                                                '//label[.//span[text()="Цена с НДС"]]'))
                )
                switch.click()
                tax_field = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[name="tax"] input'))
                )
                tax_field.click()
                tax_field.send_keys('без')
                ActionChains(driver).move_to_element(tax_field).move_by_offset(0, 40).click().perform()
                status_field = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[name="status"] input'))
                )
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", status_field)
                status_field.send_keys("черновик")
                ActionChains(driver).move_to_element(status_field).move_by_offset(0, 30).click().perform()
                status_field.send_keys(Keys.ENTER)
                product_field = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[name="productUnits"] input'))
                )
                product_field.click()
                ActionChains(driver).move_to_element(product_field).move_by_offset(0, 40).click().perform()
                button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Добавить')]"))
                )
                button.click()
            except Exception as e:
                attach_screenshot(driver, "Ошибка при Финансах")
                print(f"Ошибка при ри Финансах: {e}")

        with allure.step("вычисляемое, комиссия 2"):
            try:
                # Ожидание появления кнопки
                tab = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[@role='tab' and contains(., 'Вычисляемое')]")))
                tab.click()
                buttonp = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "button.css-cdp6mq")))
                buttonp.click()
                input_field = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='Выберите статью финансовой операции']")))
                input_field.click()
                input_field.send_keys('Комиссия 2')
                ActionChains(driver).move_to_element(input_field).move_by_offset(0, 40).click().perform()
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", input_field)
                #!!!!!!!!!
                input_field1 = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/main/div[2]/form/div[1]/div/div[3]/div[2]/div/div/input')))
                input_field1.click()
                input_field1.send_keys('Комиссия 2')
                wait = WebDriverWait(driver, 10)
                label = wait.until(EC.presence_of_element_located((By.XPATH, "//label[contains(text(), 'Товар')]")))
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", label)
                label.click()
                time.sleep(0.5)
                input_id = label.get_attribute("for")
                input_field = wait.until(EC.element_to_be_clickable((By.ID, input_id)))
                input_field.send_keys('Puricat')
                time.sleep(0.5)
                ActionChains(driver).move_to_element(input_field).move_by_offset(0, 40).click().perform()
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", input_field)
                input_field = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Выберите финансовые операции']"))
                )
                driver.execute_script("arguments[0].scrollIntoView(true);", input_field)
                driver.execute_script("arguments[0].click();", input_field)
                input_field.send_keys('продажа')
                ActionChains(driver).move_to_element(input_field).move_by_offset(0, 40).click().perform()
                chip = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//span[text()='Сумма с налогом']"))
                )
                chip.click()
                input_field = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/main/div[2]/form/div[1]/div/div[5]/div/div[2]/div/div[3]/div/div/input")))
                input_field.click()
                input_field.send_keys('/1.2*0.5%')
                driver.find_element(By.XPATH, "//button[normalize-space(text())='Сохранить']").click()
            except Exception as e:
                attach_screenshot(driver, "Ошибка при клике по вычисляемое")
                print(f"вычисляемое: {e}")
    with allure.step("Комиссия 3"):
        try:
            buttonp = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.css-cdp6mq")))
            buttonp.click()
            input_field = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='Выберите статью финансовой операции']")))
            input_field.click()
            input_field.send_keys('Комиссия 3')
            ActionChains(driver).move_to_element(input_field).move_by_offset(0, 40).click().perform()
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", input_field)
            #!!!!!!!!!
            input_field1 = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/main/div[2]/form/div[1]/div/div[3]/div[2]/div/div/input')))
            input_field1.click()
            input_field1.send_keys('Комиссия 3')
            wait = WebDriverWait(driver, 10)
            label = wait.until(EC.presence_of_element_located((By.XPATH, "//label[contains(text(), 'Товар')]")))
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", label)
            label.click()
            time.sleep(0.5)
            input_id = label.get_attribute("for")
            input_field = wait.until(EC.element_to_be_clickable((By.ID, input_id)))
            input_field.send_keys('Puricat')
            time.sleep(0.5)
            ActionChains(driver).move_to_element(input_field).move_by_offset(0, 40).click().perform()
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", input_field)
            input_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Выберите финансовые операции']"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", input_field)
            driver.execute_script("arguments[0].click();", input_field)
            input_field.send_keys('продажа')
            ActionChains(driver).move_to_element(input_field).move_by_offset(0, 40).click().perform()
            chip = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//span[text()='Сумма с налогом']"))
            )
            chip.click()
            input_field = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/main/div[2]/form/div[1]/div/div[5]/div/div[2]/div/div[3]/div/div/input")))
            input_field.click()
            input_field.send_keys('/1.2*0.5%')
            driver.find_element(By.XPATH, "//button[normalize-space(text())='Сохранить']").click()
        except Exception as e:
            attach_screenshot(driver, "Ошибка при клике по вычисляемое")
            print(f"вычисляемое: {e}")
    with allure.step("Комиссия 4"):
        try:
            buttonp = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.css-cdp6mq")))
            buttonp.click()
            input_field = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='Выберите статью финансовой операции']")))
            input_field.click()
            input_field.send_keys('Комиссия 4')
            ActionChains(driver).move_to_element(input_field).move_by_offset(0, 40).click().perform()
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", input_field)
            #!!!!!!!!!
            input_field1 = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/main/div[2]/form/div[1]/div/div[3]/div[2]/div/div/input')))
            input_field1.click()
            input_field1.send_keys('Комиссия 4')
            wait = WebDriverWait(driver, 10)
            label = wait.until(EC.presence_of_element_located((By.XPATH, "//label[contains(text(), 'Товар')]")))
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", label)
            label.click()
            time.sleep(0.5)
            input_id = label.get_attribute("for")
            input_field = wait.until(EC.element_to_be_clickable((By.ID, input_id)))
            input_field.send_keys('Puricat')
            time.sleep(0.5)
            ActionChains(driver).move_to_element(input_field).move_by_offset(0, 40).click().perform()
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", input_field)
            input_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Выберите финансовые операции']"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", input_field)
            driver.execute_script("arguments[0].click();", input_field)
            input_field.send_keys('продажа')
            ActionChains(driver).move_to_element(input_field).move_by_offset(0, 40).click().perform()
            chip = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//span[text()='Сумма с налогом']"))
            )
            chip.click()
            input_field = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/main/div[2]/form/div[1]/div/div[5]/div/div[2]/div/div[3]/div/div/input")))
            input_field.click()
            input_field.send_keys('/1.2*0.5%')
            driver.find_element(By.XPATH, "//button[normalize-space(text())='Сохранить']").click()
        except Exception as e:
            attach_screenshot(driver, "Ошибка при клике по вычисляемое")
            print(f"вычисляемое: {e}")
    with allure.step("Комиссия 5"):
        try:
            buttonp = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.css-cdp6mq")))
            buttonp.click()
            input_field = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='Выберите статью финансовой операции']")))
            input_field.click()
            input_field.send_keys('Комиссия 5')
            ActionChains(driver).move_to_element(input_field).move_by_offset(0, 40).click().perform()
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", input_field)
            #!!!!!!!!!
            input_field1 = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/main/div[2]/form/div[1]/div/div[3]/div[2]/div/div/input')))
            input_field1.click()
            input_field1.send_keys('Комиссия 5')
            wait = WebDriverWait(driver, 10)
            label = wait.until(EC.presence_of_element_located((By.XPATH, "//label[contains(text(), 'Товар')]")))
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", label)
            label.click()
            time.sleep(0.5)
            input_id = label.get_attribute("for")
            input_field = wait.until(EC.element_to_be_clickable((By.ID, input_id)))
            input_field.send_keys('Puricat')
            time.sleep(0.5)
            ActionChains(driver).move_to_element(input_field).move_by_offset(0, 40).click().perform()
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", input_field)
            input_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Выберите финансовые операции']"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", input_field)
            driver.execute_script("arguments[0].click();", input_field)
            input_field.send_keys('продажа')
            ActionChains(driver).move_to_element(input_field).move_by_offset(0, 40).click().perform()
            chip = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//span[text()='Сумма с налогом']"))
            )
            chip.click()
            input_field = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/main/div[2]/form/div[1]/div/div[5]/div/div[2]/div/div[3]/div/div/input")))
            input_field.click()
            input_field.send_keys('/1.2*0.5%')
            driver.find_element(By.XPATH, "//button[normalize-space(text())='Сохранить']").click()
        except Exception as e:
            attach_screenshot(driver, "Ошибка при клике по вычисляемое")
            print(f"вычисляемое: {e}")
    with allure.step("Комиссия 6"):
        try:
            buttonp = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.css-cdp6mq")))
            buttonp.click()
            input_field = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='Выберите статью финансовой операции']")))
            input_field.click()
            input_field.send_keys('Комиссия 6')
            ActionChains(driver).move_to_element(input_field).move_by_offset(0, 40).click().perform()
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", input_field)
            #!!!!!!!!!
            input_field1 = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/main/div[2]/form/div[1]/div/div[3]/div[2]/div/div/input')))
            input_field1.click()
            input_field1.send_keys('Комиссия 6')
            wait = WebDriverWait(driver, 10)
            label = wait.until(EC.presence_of_element_located((By.XPATH, "//label[contains(text(), 'Товар')]")))
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", label)
            label.click()
            time.sleep(0.5)
            input_id = label.get_attribute("for")
            input_field = wait.until(EC.element_to_be_clickable((By.ID, input_id)))
            input_field.send_keys('Puricat')
            time.sleep(0.5)
            ActionChains(driver).move_to_element(input_field).move_by_offset(0, 40).click().perform()
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", input_field)
            input_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Выберите финансовые операции']"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", input_field)
            driver.execute_script("arguments[0].click();", input_field)
            input_field.send_keys('продажа')
            ActionChains(driver).move_to_element(input_field).move_by_offset(0, 40).click().perform()
            chip = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//span[text()='Прибыль после налогов']"))
            )
            chip.click()
            input_field = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/main/div[2]/form/div[1]/div/div[5]/div/div[2]/div/div[3]/div/div/input")))
            input_field.click()
            input_field.send_keys('-(')
            input_field1 = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/main/div[2]/form/div[1]/div/div[5]/div/div[2]/div/div/div/div/input")))
            input_field1.click()
            input_field1.send_keys('(')
            chip2 = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/main/div[2]/form/div[1]/div/div[5]/div/div[3]/div[2]/div[2]/div[5]/div/span"))
            )
            chip2.click()
            input_field2 = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/main/div[2]/form/div[1]/div/div[5]/div/div[2]/div/div[5]/div/div/input")))
            input_field2.click()
            input_field2.send_keys('*2%))/3*2')
            driver.find_element(By.XPATH, "//button[normalize-space(text())='Сохранить']").click()
        except Exception as e:
            attach_screenshot(driver, "Ошибка при клике по вычисляемое")
            print(f"вычисляемое: {e}")
    with allure.step("Комиссия 7"):
        try:
            buttonp = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.css-cdp6mq")))
            buttonp.click()
            input_field = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='Выберите статью финансовой операции']")))
            input_field.click()
            input_field.send_keys('Комиссия 7')
            ActionChains(driver).move_to_element(input_field).move_by_offset(0, 40).click().perform()
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", input_field)
            #!!!!!!!!!
            input_field1 = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/main/div[2]/form/div[1]/div/div[3]/div[2]/div/div/input')))
            input_field1.click()
            input_field1.send_keys('Комиссия 7')
            wait = WebDriverWait(driver, 10)
            label = wait.until(EC.presence_of_element_located((By.XPATH, "//label[contains(text(), 'Товар')]")))
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", label)
            label.click()
            time.sleep(0.5)
            input_id = label.get_attribute("for")
            input_field = wait.until(EC.element_to_be_clickable((By.ID, input_id)))
            input_field.send_keys('Puricat')
            time.sleep(0.5)
            ActionChains(driver).move_to_element(input_field).move_by_offset(0, 40).click().perform()
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", input_field)
            input_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Выберите финансовые операции']"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", input_field)
            driver.execute_script("arguments[0].click();", input_field)
            input_field.send_keys('продажа')
            ActionChains(driver).move_to_element(input_field).move_by_offset(0, 40).click().perform()
            chip = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//span[text()='Сумма с налогом']"))
            )
            chip.click()
            input_field = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/main/div[2]/form/div[1]/div/div[5]/div/div[2]/div/div[3]/div/div/input")))
            input_field.click()
            input_field.send_keys('/1.2*0.5%')
            driver.find_element(By.XPATH, "//button[normalize-space(text())='Сохранить']").click()
        except Exception as e:
            attach_screenshot(driver, "Ошибка при клике по вычисляемое")
            print(f"вычисляемое: {e}")
    with allure.step("удаление"):
        try:
            time.sleep(1)
            tab = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@role='tab' and contains(., 'Аналитика')]"))
            )
            tab.click()
            time.sleep(2)
            attach_screenshot(driver, "Аналитика")
            driver.execute_script("window.scrollBy(0, 500);")
            time.sleep(2)
            attach_screenshot(driver, "Аналитика")
            driver.execute_script("window.scrollBy(0, 500);")
            attach_screenshot(driver, "Аналитика")
            settings_link = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//a[.//p[contains(text(), 'Настройки')]]"))
            )
            settings_link.click()
            element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//p[contains(@class, 'MuiTypography-body1') and contains(text(), 'Список бизнес-процессов')]"))
            )
            element.click()
            button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//h2[text()='Сделка']/../../following-sibling::div//button[.//*[local-name()='svg' and @data-testid='MoreVertIcon']]"))
            )
            button.click()
            delete_option = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//li[@role='menuitem'][.//text()='Удалить']"))
            )
            delete_option.click()
        except Exception as e:
            attach_screenshot(driver, "Ошибка при клике по вычисляемое")
            print(f"вычисляемое: {e}")
    with allure.step("проверка валюты"):
        try:
            driver.get("https://cbr.ru/currency_base/daily/")
            time.sleep(2)
            scroll_quarter = "window.scrollTo({ top: document.body.scrollHeight * 0.25, behavior: 'smooth' });"
            driver.execute_script(scroll_quarter)
            print('Валюты с сайта мосбиржи не совпадают с экземпляром 1,0.4,1 и мосбиржа 0.55, 0,0068, 1,11')
        except Exception as e:
            print(f"Ошибка валюты, конец: {str(e)}")

    time.sleep(15)
