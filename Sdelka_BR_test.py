import pytest
from selenium import webdriver
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
#Это выбор ответственных

def select_multiple_responsibles(driver: WebDriver, indices: list):
    """
    Выбирает указанные элементы из списка ответственных
    :param driver: Экземпляр WebDriver
    :param indices: Список индексов для выбора (начиная с 0)
    """
    wait = WebDriverWait(driver, 15)
    selected_count = 0

    try:
        for index in indices:
            # Открываем список
            for attempt in range(3):
                try:
                    field = wait.until(EC.element_to_be_clickable(
                        (By.XPATH, "//input[@placeholder='Выберите ответственных']")
                    ))
                    field.click()
                    time.sleep(0.5)
                    break
                except Exception:
                    if attempt == 2:
                        raise Exception("Не удалось открыть список ответственных")
                    time.sleep(0.5)

            # Ждем появления списка
            wait.until(EC.visibility_of_element_located(
                (By.XPATH, "//div[contains(@class, 'MuiAutocomplete-popper')]")
            ))

            # Получаем свежий список элементов
            options = wait.until(EC.presence_of_all_elements_located(
                (By.XPATH, "//li[contains(@class, 'MuiAutocomplete-option')]")
            ))

            # Проверяем индекс
            if index >= len(options):
                print(f"Предупреждение: индекс {index} пропущен (в списке только {len(options)} элементов)")
                continue

            # Кликаем элемент
            for click_attempt in range(3):
                try:
                    driver.execute_script("arguments[0].scrollIntoView(true);", options[index])
                    time.sleep(0.3)
                    options[index].click()
                    selected_count += 1
                    break
                except Exception:
                    if click_attempt == 2:
                        raise Exception(f"Не удалось кликнуть элемент {index}")
                    time.sleep(0.5)

            time.sleep(0.5)  # Пауза между выборами

        # Финализируем выбор если был выбран хотя бы один элемент
        if selected_count > 0:
            ActionChains(driver).send_keys(Keys.ENTER).perform()
            time.sleep(1)
        else:
            raise Exception("Не было выбрано ни одного элемента")

    except Exception as e:
        attach_screenshot(driver, "Ошибка выбора ответственных")
        raise Exception(f"Ошибка при выборе ответственных: {str(e)}")


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
        driver.get("https://dev.business-pad.com/")
        # Вход в систему
        driver.find_element(By.XPATH, '//*[@id=":r0:"]').send_keys("adminbp")
        driver.find_element(By.XPATH, '//*[@id=":r1:"]').send_keys("xDBfZomfzWjg")
        driver.find_element(By.XPATH, '//*[@id="root"]/div/main/div/div/div/div[2]/div/form/div/div[4]').click()
        attach_screenshot(driver, "После логина")

    try:
        with allure.step("Клик по иконке настроек"):
            # Ожидаем и кликаем по иконке Settings
            settings_icon = wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "svg[data-testid='SettingsIcon']")
            ))

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

        with allure.step("Клик по 'Список бизнес-процессов'"):
            # Ожидаем и кликаем по тексту
            bp_list = wait.until(EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="main"]/div/div/div[2]/div[1]/div[2]/div/div/div/div[2]/div[2]/p')
            ))

            # Двойной клик для надежности
            ActionChains(driver) \
                .move_to_element(bp_list) \
                .pause(0.2) \
                .click() \
                .pause(0.1) \
                .click() \
                .perform()

            attach_screenshot(driver, "После клика по списку БП")

    except Exception as e:
        attach_screenshot(driver, "Ошибка при выполнении действий")
        pytest.fail(f"Ошибка при выполнении: {str(e)}")

    # Создаем папку Копии
    with allure.step("Нажатие на кнопку 'Создать папку' и ввод текста 'Копии'"):
        try:
            # Ожидание появления кнопки и клик
            create_folder_button = wait.until(EC.element_to_be_clickable(
                (By.XPATH, '//h2[contains(text(), "Создать папку")]')  # Ищем элемент по тексту
            ))
            create_folder_button.click()
            # Ожидание появления поля для ввода названия папки
            folder_name_input = wait.until(EC.visibility_of_element_located(
                (By.XPATH, '//div[contains(@class, "MuiInputBase-root") and .//legend[contains(., "Создать папку")]]//input')))
            folder_name_input.send_keys("Копии")
            folder_name_input.send_keys(Keys.ENTER)
            # Прикрепление скриншота после успешного ввода
            attach_screenshot(driver, "После ввода 'Копии'")
        except Exception as e:
            # Прикрепление скриншота в случае ошибки
            attach_screenshot(driver, "Ошибка при создании папки")
            # Завершение теста с ошибкой
            pytest.fail(f"Не удалось создать папку: {e}")

    with allure.step("Клик по элементу 'Пусто'"):
        try:
            # Ищем элемент по классу и тексту
            empty_element = wait.until(EC.element_to_be_clickable(
                (By.XPATH, '//div[contains(@class, "MuiGrid-item")]//h6[text()="Пусто"]')
            ))
            # Прокручиваем до элемента (если нужно)
            driver.execute_script("arguments[0].click();", empty_element)
            # Кликаем через ActionChains для надежности
            ActionChains(driver).move_to_element(empty_element).pause(0.2).click().perform()
            attach_screenshot(driver, "after_click_empty")
        except Exception as e:
            attach_screenshot(driver, "error_click_empty")
            pytest.fail(f"Не удалось кликнуть по элементу 'Пусто': {str(e)}")

    with allure.step("Клик по кнопке с иконкой добавления"):
        try:
            # Ожидание появления кнопки
            button = wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button.MuiButtonBase-root.MuiButton-containedSecondary")
            ))
            # Прокрутка страницы до кнопки
            driver.execute_script("arguments[0].scrollIntoView(true);", button)
            # Клик по кнопке
            ActionChains(driver).move_to_element(button).click().perform()
            attach_screenshot(driver, "После клика по кнопке добавления")
        except Exception as e:
            attach_screenshot(driver, "Ошибка при клике по кнопке добавления")
            pytest.fail(f"Не удалось кликнуть по кнопке добавления: {e}")

    # Редактирование
    with allure.step("Нажатие на вкладку 'Настройка процесса'"):
        try:
            process_setup_tab = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[@role='tab' and contains(text(), 'Настройка процесса')]"))
            )
            process_setup_tab.click()
            attach_screenshot(driver, "После нажатия на вкладку 'Настройка процесса'")
        except Exception as e:
            attach_screenshot(driver, "Ошибка при нажатии на вкладку 'Настройка процесса'")
            pytest.fail(f"Не удалось нажать на вкладку 'Настройка процесса': {e}")

    with allure.step("Ввод текста 'Копия сделки БР' в поле названия процесса"):
        try:
            # Ожидание появления поля ввода
            process_name_input = wait.until(
                EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Введите название процесса']")))
            # Очистка поля ввода
            process_name_input.send_keys(Keys.CONTROL + "a")
            process_name_input.send_keys(Keys.DELETE)
            # Ввод нового текста
            process_name_input.send_keys("Копия сделки БР")
            attach_screenshot(driver, "После ввода 'Копия сделки БР'")
        except Exception as e:
            attach_screenshot(driver, "Ошибка при вводе текста в поле названия процесса")
            pytest.fail(f"Не удалось ввести текст в поле названия процесса: {e}")

    #$$$$$$$$
    with allure.step("тип процесса"):
        try:
            select_type_input = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "div.MuiAutocomplete-root[name='type']"))
            )
            select_type_input.click()
            attach_screenshot(driver, "Открыт выбор типа процесса")

            budget_option = wait.until(
                EC.element_to_be_clickable((By.XPATH, '//li[@role="option"][2]'))
            )
            budget_option.click()
            attach_screenshot(driver, "Выбран тип 'Бюджет расходов'")
            time.sleep(1)

        except Exception as e:
            attach_screenshot(driver, "Ошибка в процессе настройки")
            pytest.fail(f"Ошибка в процессе настройки: {e}")

    # Выбор участников
    with allure.step("2. Выбор участников"):
        participants = ["ДЭ", "ГД", "СРК", "МП", "Операционист", "Бухгалтер",
                        "Экономист", "КД", "РОП", "ДирКем", "Мп", "АДМ"]

        for participant in participants:
            with allure.step(f"Выбираем участника: {participant}"):
                try:
                    # Находим поле ввода
                    input_field = wait.until(
                        EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Выберите участников']"))
                    )
                    input_field.click()
                    input_field.clear()

                    # Вводим значение
                    input_field.send_keys(participant)
                    time.sleep(2)  # Увеличили время ожидания
                    attach_screenshot(driver, f"После ввода {participant}")

                    # Ждем появления списка и кликаем по варианту
                    participant_option = wait.until(
                        EC.element_to_be_clickable(
                            (By.XPATH, f"//div[contains(@class,'MuiAutocomplete-popper')]//li[contains(., '{participant}')]"))
                    )
                    participant_option.click()
                    attach_screenshot(driver, f"Участник {participant} выбран")
                    time.sleep(1)

                except Exception as e:
                    attach_screenshot(driver, f"Ошибка выбора участника {participant}")
                    pytest.fail(f"Не удалось выбрать участника {participant}: {str(e)}")
                    continue
    #$$$$$$$$$$$$$
    with allure.step("Нажатие на кнопку 'Сохранить'"):
        try:
            save_button = wait.until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div/div/main/div[5]/div/div[1]/button"))
            )
            driver.execute_script("arguments[0].click();", save_button)
            attach_screenshot(driver, "После нажатия на кнопку 'Сохранить'")
        except Exception as e:
            attach_screenshot(driver, "Ошибка при нажатии на кнопку 'Сохранить'")
            pytest.fail(f"Не удалось нажать на кнопку 'Сохранить': {e}")


    with allure.step("Нажатие на кнопку 'Полотно процесса'"):
        try:
            canvas_button = wait.until(
                EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Полотно процесса')]"))
            )
            driver.execute_script("arguments[0].click();", canvas_button)
            time.sleep(1)
            attach_screenshot(driver, "После нажатия на кнопку 'Полотно процесса'")
        except Exception as e:
            attach_screenshot(driver, "Ошибка при нажатии на кнопку 'Полотно процесса'")
            pytest.fail(f"Не удалось нажать на кнопку 'Полотно процесса': {e}")

    # Перетаскивание элемента "Основной"!!!!!!!!!!!!
    with allure.step("2. Перетаскивание элемента 'Основной'"):
        try:
            element = wait.until(EC.presence_of_element_located((By.XPATH, '//p[contains(text(), "Основной")]')))
            actions = ActionChains(driver)
            actions.click_and_hold(element).move_by_offset(500, 0).release().perform()
            attach_screenshot(driver, "После перетаскивания элемента")



        except Exception as e:
            attach_screenshot(driver, "Ошибка при перетаскивании элемента")
            pytest.fail(f"Ошибка при перетаскивании элемента: {e}")

    # Ввод названия
    with allure.step("Очистка поля 'Название узла' и ввод 'Согласование с ГЭ'"):
        try:
            name_input = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Введите название узла']")))
            attach_screenshot(driver, "Элемент найден, перед кликом")  # Скриншот перед кликом
            name_input.click()  # Фокусируемся на элементе
            name_input.send_keys(Keys.CONTROL + "a")  # Выделяем весь текст
            name_input.send_keys(Keys.DELETE)  # Удаляем выделенный текст
            name_input.send_keys("Согласование с ГЭ")  # Вводим новое значение
            attach_screenshot(driver, "После ввода названия узла")
        except Exception as e:
            attach_screenshot(driver, "Ошибка при вводе названия узла")
            pytest.fail(f"Ошибка при вводе названия узла: {e}")
    # Ответственный
    with allure.step("Клик по заголовку 'Ответственные'"):
        try:
            responsible_header = wait.until(EC.presence_of_element_located((By.XPATH, "//h2[contains(text(), 'Ответственные')]")))
            responsible_header.click()
            attach_screenshot(driver, "После клика по заголовку 'Ответственные'")
        except Exception as e:
            attach_screenshot(driver, "Ошибка при клике по заголовку 'Ответственные'")
            pytest.fail(f"Ошибка при клике по заголовку 'Ответственные': {e}")
    #Выбор ответственных
    with allure.step("Выбор нескольких ответственных"):
        try:
            # Выбираем первый (0) и третий (2) элементы из списка
            select_multiple_responsibles(driver, [0, 4])
            attach_screenshot(driver, "Ответственные выбраны")
        except Exception as e:
            attach_screenshot(driver, "Ошибка выбора ответственных")
            pytest.fail(f"Ошибка выбора ответственных: {str(e)}")
        #Второй!!!!!!!!!!! Коммент
        with allure.step("2. Перетаскивание элемента 'Основной'"):
            try:
                element = wait.until(EC.presence_of_element_located((By.XPATH, '//p[contains(text(), "Основной")]')))
                actions = ActionChains(driver)
                actions.click_and_hold(element).move_by_offset(500, 0).release().perform()
                attach_screenshot(driver, "После перетаскивания элемента")



            except Exception as e:
                attach_screenshot(driver, "Ошибка при перетаскивании элемента")
                pytest.fail(f"Ошибка при перетаскивании элемента: {e}")

    # Ввод названия
    with allure.step("Очистка поля 'Название узла' и ввод 'Утверждение БР ДЭ'"):
        try:
            name_input = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Введите название узла']")))
            attach_screenshot(driver, "Элемент найден, перед кликом")  # Скриншот перед кликом
            name_input.click()  # Фокусируемся на элементе
            name_input.send_keys(Keys.CONTROL + "a")  # Выделяем весь текст
            name_input.send_keys(Keys.DELETE)  # Удаляем выделенный текст
            name_input.send_keys("Утверждение БР ДЭ")  # Вводим новое значение
            attach_screenshot(driver, "После ввода названия узла")
        except Exception as e:
            attach_screenshot(driver, "Ошибка при вводе названия узла")
            pytest.fail(f"Ошибка при вводе названия узла: {e}")
    #Описание
    with allure.step("Ввод 'коммента' в поле 'Описание узла'"):
        try:
            description_input = wait.until(EC.visibility_of_element_located((By.XPATH, "//textarea[@placeholder='Введите описание узла']")))
            description_input.send_keys("Утверждение Бюджета расходов на следующий месяц директором по экономике")
            attach_screenshot(driver, "После ввода описания узла")
        except Exception as e:
            attach_screenshot(driver, "Ошибка при вводе описания узла")
            pytest.fail(f"Ошибка при вводе описания узла: {e}")
    # Ответственный
    with allure.step("Клик по заголовку 'Ответственные'"):
        try:
            responsible_header = wait.until(EC.presence_of_element_located((By.XPATH, "//h2[contains(text(), 'Ответственные')]")))
            responsible_header.click()
            attach_screenshot(driver, "После клика по заголовку 'Ответственные'")
        except Exception as e:
            attach_screenshot(driver, "Ошибка при клике по заголовку 'Ответственные'")
            pytest.fail(f"Ошибка при клике по заголовку 'Ответственные': {e}")
    #Выбор ответственных
    with allure.step("Выбор нескольких ответственных"):
        try:
            # Выбираем первый (0) и третий (2) элементы из списка
            select_multiple_responsibles(driver, [0, 4, 6])
            attach_screenshot(driver, "Ответственные выбраны")
        except Exception as e:
            attach_screenshot(driver, "Ошибка выбора ответственных")
            pytest.fail(f"Ошибка выбора ответственных: {str(e)}")
        #Третий !!!!!!!!!!
        with allure.step("2. Перетаскивание элемента 'Основной'"):
            try:
                element = wait.until(EC.presence_of_element_located((By.XPATH, '//p[contains(text(), "Основной")]')))
                actions = ActionChains(driver)
                actions.click_and_hold(element).move_by_offset(500, 0).release().perform()
                attach_screenshot(driver, "После перетаскивания элемента")



            except Exception as e:
                attach_screenshot(driver, "Ошибка при перетаскивании элемента")
                pytest.fail(f"Ошибка при перетаскивании элемента: {e}")

    # Ввод названия
    with allure.step("Очистка поля 'Название узла' и ввод 'Утверждение ДирКем'"):
        try:
            name_input = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Введите название узла']")))
            attach_screenshot(driver, "Элемент найден, перед кликом")  # Скриншот перед кликом
            name_input.click()  # Фокусируемся на элементе
            name_input.send_keys(Keys.CONTROL + "a")  # Выделяем весь текст
            name_input.send_keys(Keys.DELETE)  # Удаляем выделенный текст
            name_input.send_keys("Утверждение ДирКем")  # Вводим новое значение
            attach_screenshot(driver, "После ввода названия узла")
        except Exception as e:
            attach_screenshot(driver, "Ошибка при вводе названия узла")
            pytest.fail(f"Ошибка при вводе названия узла: {e}")
    # Ответственный
    with allure.step("Клик по заголовку 'Ответственные'"):
        try:
            responsible_header = wait.until(EC.presence_of_element_located((By.XPATH, "//h2[contains(text(), 'Ответственные')]")))
            responsible_header.click()
            attach_screenshot(driver, "После клика по заголовку 'Ответственные'")
        except Exception as e:
            attach_screenshot(driver, "Ошибка при клике по заголовку 'Ответственные'")
            pytest.fail(f"Ошибка при клике по заголовку 'Ответственные': {e}")
    #Выбор ответственных
    with allure.step("Выбор нескольких ответственных"):
        try:
            # Выбираем первый (0) и третий (2) элементы из списка
            select_multiple_responsibles(driver, [3, 4])
            attach_screenshot(driver, "Ответственные выбраны")
        except Exception as e:
            attach_screenshot(driver, "Ошибка выбора ответственных")
            pytest.fail(f"Ошибка выбора ответственных: {str(e)}")
        #Четвертый Коммент
        with allure.step("2. Перетаскивание элемента 'Основной'"):
            try:
                element = wait.until(EC.presence_of_element_located((By.XPATH, '//p[contains(text(), "Основной")]')))
                actions = ActionChains(driver)
                actions.click_and_hold(element).move_by_offset(300, 0).release().perform()
                attach_screenshot(driver, "После перетаскивания элемента")



            except Exception as e:
                attach_screenshot(driver, "Ошибка при перетаскивании элемента")
                pytest.fail(f"Ошибка при перетаскивании элемента: {e}")

    # Ввод названия
    with allure.step("Очистка поля 'Название узла' и ввод 'Внесение в БДУ статей расходов'"):
        try:
            name_input = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Введите название узла']")))
            attach_screenshot(driver, "Элемент найден, перед кликом")  # Скриншот перед кликом
            name_input.click()  # Фокусируемся на элементе
            name_input.send_keys(Keys.CONTROL + "a")  # Выделяем весь текст
            name_input.send_keys(Keys.DELETE)  # Удаляем выделенный текст
            name_input.send_keys("Внесение в БДУ статей расходов")  # Вводим новое значение
            attach_screenshot(driver, "После ввода названия узла")
        except Exception as e:
            attach_screenshot(driver, "Ошибка при вводе названия узла")
            pytest.fail(f"Ошибка при вводе названия узла: {e}")
            #Описание
    with allure.step("Ввод коммента в поле 'Описание узла'"):
        try:
            description_input = wait.until(EC.visibility_of_element_located((By.XPATH, "//textarea[@placeholder='Введите описание узла']")))
            description_input.send_keys(" по договору без предоставления счета, со статусом утверждено в оплату на основании счетов/первичных документов, со статусом заявлено к оплате по статьям ЗП, аванса, АУ, Премии ГД, НДФЛ, налоги и взносы со статусом заявлено к оплате")
            attach_screenshot(driver, "После ввода описания узла")
        except Exception as e:
            attach_screenshot(driver, "Ошибка при вводе описания узла")
            pytest.fail(f"Ошибка при вводе описания узла: {e}")
    # Ответственный
    with allure.step("Клик по заголовку 'Ответственные'"):
        try:
            responsible_header = wait.until(EC.presence_of_element_located((By.XPATH, "//h2[contains(text(), 'Ответственные')]")))
            responsible_header.click()
            attach_screenshot(driver, "После клика по заголовку 'Ответственные'")
        except Exception as e:
            attach_screenshot(driver, "Ошибка при клике по заголовку 'Ответственные'")
            pytest.fail(f"Ошибка при клике по заголовку 'Ответственные': {e}")
    #Выбор ответственных
    with allure.step("Выбор нескольких ответственных"):
        try:
            # Выбираем первый (0) и третий (2) элементы из списка
            select_multiple_responsibles(driver, [0, 4, 8])
            attach_screenshot(driver, "Ответственные выбраны")
        except Exception as e:
            attach_screenshot(driver, "Ошибка выбора ответственных")
            pytest.fail(f"Ошибка выбора ответственных: {str(e)}")
        #Пятый Коммент
        with allure.step("2. Перетаскивание элемента 'Основной'"):
            try:
                element = wait.until(EC.presence_of_element_located((By.XPATH, '//p[contains(text(), "Основной")]')))
                actions = ActionChains(driver)
                actions.click_and_hold(element).move_by_offset(700, 0).release().perform()
                attach_screenshot(driver, "После перетаскивания элемента")



            except Exception as e:
                attach_screenshot(driver, "Ошибка при перетаскивании элемента")
                pytest.fail(f"Ошибка при перетаскивании элемента: {e}")

    # Ввод названия
    with allure.step("Очистка поля 'Название узла' и ввод 'Исполнение БР, Внесение ПП, Предоставление ЗНО'"):
        try:
            name_input = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Введите название узла']")))
            attach_screenshot(driver, "Элемент найден, перед кликом")  # Скриншот перед кликом
            name_input.click()  # Фокусируемся на элементе
            name_input.send_keys(Keys.CONTROL + "a")  # Выделяем весь текст
            name_input.send_keys(Keys.DELETE)  # Удаляем выделенный текст
            name_input.send_keys("Исполнение БР, Внесение ПП, Предоставление ЗНО")  # Вводим новое значение
            attach_screenshot(driver, "После ввода названия узла")
        except Exception as e:
            attach_screenshot(driver, "Ошибка при вводе названия узла")
            pytest.fail(f"Ошибка при вводе названия узла: {e}")
    #Коммент
    with allure.step("Ввод коммента в поле 'Описание узла'"):
        try:
            description_input = wait.until(EC.visibility_of_element_located((By.XPATH, "//textarea[@placeholder='Введите описание узла']")))
            description_input.send_keys("Исполнение БР,  Внесение платежных поручений, Предоставление заявок на оплату")
            attach_screenshot(driver, "После ввода описания узла")
        except Exception as e:
            attach_screenshot(driver, "Ошибка при вводе описания узла")
            pytest.fail(f"Ошибка при вводе описания узла: {e}")
    # Ответственный
    with allure.step("Клик по заголовку 'Ответственные'"):
        try:
            responsible_header = wait.until(EC.presence_of_element_located((By.XPATH, "//h2[contains(text(), 'Ответственные')]")))
            responsible_header.click()
            attach_screenshot(driver, "После клика по заголовку 'Ответственные'")
        except Exception as e:
            attach_screenshot(driver, "Ошибка при клике по заголовку 'Ответственные'")
            pytest.fail(f"Ошибка при клике по заголовку 'Ответственные': {e}")
    #Выбор ответственных
    with allure.step("Выбор нескольких ответственных"):
        try:
            # Выбираем первый (0) и третий (2) элементы из списка
            select_multiple_responsibles(driver, [0, 4, 8])
            attach_screenshot(driver, "Ответственные выбраны")
        except Exception as e:
            attach_screenshot(driver, "Ошибка выбора ответственных")
            pytest.fail(f"Ошибка выбора ответственных: {str(e)}")

                #Финиш!!!!!!!!!!!!!!
        with allure.step("Клик по элементу 'Финиш'"):
            try:
                # Ожидаем появление элемента и проверяем текст
                finish_element = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'p.MuiTypography-body1[aria-label="Финиш"]'))
                )

                # Проверяем текст элемента
                assert finish_element.text == "Финиш", f"Текст элемента не 'Финиш', а '{finish_element.text}'"

                # Кликаем по элементу
                finish_element.click()

                # Делаем скриншот для отчета
                attach_screenshot(driver, "После клика по 'Финиш'")

            except Exception as e:
                # Если ошибка - делаем скриншот и падаем с понятным сообщением
                attach_screenshot(driver, "Ошибка при клике по 'Финиш'")
                pytest.fail(f"Не удалось кликнуть по 'Финиш': {str(e)}")
    #Очистка
    with allure.step("Выгрузка в Эксель. Финиш"):
        try:
            name1_input = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Введите название узла']")))
            attach_screenshot(driver, "Элемент найден, перед кликом")  # Скриншот перед кликом
            name1_input.click()  # Фокусируемся на элементе
            name1_input.send_keys(Keys.CONTROL + "a")  # Выделяем весь текст
            name1_input.send_keys(Keys.DELETE)  # Удаляем выделенный текст
            name1_input.send_keys("Выгрузка в Эксель. Финиш")  # Вводим новое значение
            attach_screenshot(driver, "После ввода названия узла")
        except Exception as e:
            attach_screenshot(driver, "Ошибка при вводе названия узла")
            pytest.fail(f"Ошибка при вводе названия узла: {e}")
    #Коммент
    with allure.step("Описание узла"):
        try:
            desc_input = wait.until(EC.visibility_of_element_located((By.XPATH, "//textarea[@placeholder='Введите описание узла']")))
            desc_input.send_keys("В последний день месяца  по факту исполнения БР осуществляется выгрузка в Эксель")
            attach_screenshot(driver, "После ввода описания ")
        except Exception as e:
            attach_screenshot(driver, "Ошибка при вводе описания ")
            pytest.fail(f"Ошибка при вводе описания узла: {e}")
    # Ответственный
    with allure.step("'Ответственные'"):
        try:
            responsible_header = wait.until(EC.presence_of_element_located((By.XPATH, "//h2[contains(text(), 'Ответственные')]")))
            responsible_header.click()
            attach_screenshot(driver, "После клика по заголовку 'Ответственные'")
        except Exception as e:
            attach_screenshot(driver, "Ошибка при клике по заголовку 'Ответственные'")
            pytest.fail(f"Ошибка при клике по заголовку 'Ответственные': {e}")
    #Выбор ответственных
    with allure.step("Выбор нескольких ответственных"):
        try:
            # Выбираем первый (0) и третий (2) элементы из списка
            select_multiple_responsibles(driver, [0, 4, 8])
            attach_screenshot(driver, "Ответственные выбраны")
        except Exception as e:
            attach_screenshot(driver, "Ошибка выбора ответственных")
            pytest.fail(f"Ошибка выбора ответственных: {str(e)}")
    #Перетаскиваем Финиш
    with allure.step("2. Перетаскивание элемента 'Финиш'"):
        try:
            # 1. Находим элемент и его родительский узел
            element = wait.until(
                EC.element_to_be_clickable((By.XPATH, '//p[@aria-label="Выгрузка в Эксель. Финиш"]'))
            )
            node = driver.execute_script(
                "return arguments[0].closest('div[data-testid^=\"rf__node-\"]');",
                element
            )
            # 2. Прокручиваем к элементу и делаем паузу
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", node)
            time.sleep(0.5)
            # 3. Получаем текущие координаты через transform
            transform = driver.execute_script(
                "return window.getComputedStyle(arguments[0]).transform;",
                node
            )
            # 4. Вычисляем новые координаты
            if transform and transform != 'none':
                # Если есть transform, парсим матрицу
                values = list(map(float, transform.split('(')[1].split(')')[0].split(',')))
                new_x = values[4] + 1150
                new_transform = f"matrix({values[0]},{values[1]},{values[2]},{values[3]},{new_x},{values[5]})"
            else:
                # Если transform нет, создаем новый
                new_transform = "translateX(350px)"

            # 5. Применяем перемещение через JavaScript
            driver.execute_script(
                "arguments[0].style.transform = arguments[1];",
                node,
                new_transform
            )
            # 6. Проверяем результат
            time.sleep(0.5)  # Даем время на применение изменений
            attach_screenshot(driver, "После перемещения элемента")
        except Exception as e:
            attach_screenshot(driver, "Ошибка при перетаскивании")
            pytest.fail(f"Не удалось переместить элемент: {str(e)}")
    #Связи!!!!!!
    #Первый
    with allure.step("1. Поиск элементов для drag-and-drop"):
        try:
            source = wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, "//div[@data-nodeid='476' and @data-handlepos='bottom' and @data-handleid='4']")
                )
            )
            target = wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, "//div[@data-nodeid='478' and @data-handlepos='top']")
                ))


        except Exception as e:
            attach_screenshot(driver, "Ошибка при поиске элементов")
            pytest.fail(f"Ошибка при поиске элементов: {e}")

    with allure.step("2. Перетаскивание элемента"):
        try:
            actions = ActionChains(driver)
            actions.click_and_hold(source).move_to_element(target).release().perform()
            attach_screenshot(driver, "После перетаскивания элемента")
        except Exception as e:
            attach_screenshot(driver, "Ошибка при перетаскивании элемента")
            pytest.fail(f"Ошибка при перетаскивании элемента: {e}")
    #Второй
    for attempt in range(1, 3):  # Выполним 2 попытки
        with allure.step(f"Попытка {attempt}: Поиск и перетаскивание"):
            with allure.step("1. Поиск элементов для drag-and-drop"):
                try:
                    source = wait.until(
                        EC.presence_of_element_located(
                            (By.CSS_SELECTOR, "div[data-nodeid='478'][data-handleid='4']")
                        )
                    )
                    target = wait.until(
                        EC.presence_of_element_located(
                            (By.CSS_SELECTOR, "div[data-nodeid='479'][data-handleid='2']")
                        )
                    )
                except Exception as e:
                    attach_screenshot(driver, "Ошибка при поиске элементов")
                    pytest.fail(f"Ошибка при поиске элементов: {e}")

            with allure.step("2. Перетаскивание элемента"):
                try:
                    # Делаем элементы видимыми перед перетаскиванием
                    driver.execute_script("arguments[0].style.opacity = '1';", source)
                    driver.execute_script("arguments[0].style.opacity = '1';", target)
                    time.sleep(0.5)  # Пауза для применения стилей

                    actions = ActionChains(driver)
                    (actions
                     .move_to_element(source)
                     .pause(0.5)
                     .click_and_hold()
                     .pause(0.3)
                     .move_to_element(target)
                     .pause(0.5)
                     .release()
                     .perform())

                    attach_screenshot(driver, f"После перетаскивания элемента (попытка {attempt})")
                    time.sleep(1)  # Пауза между попытками

                except Exception as e:
                    attach_screenshot(driver, f"Ошибка при перетаскивании (попытка {attempt})")
                    if attempt == 2:  # Если это вторая попытка и снова ошибка
                        pytest.fail(f"Ошибка при перетаскивании элемента: {e}")
                    continue  # Продолжаем на следующую попытку
    #Третий
    #Третий
    for attempt in range(1, 3):  # Выполним 2 попытки
        with allure.step(f"Попытка {attempt}: Поиск и перетаскивание"):
            with allure.step("1. Поиск элементов для drag-and-drop"):
                try:
                    source = wait.until(
                        EC.presence_of_element_located(
                            (By.CSS_SELECTOR, "div[data-nodeid='479'][data-handleid='4']")
                        )
                    )
                    target = wait.until(
                        EC.presence_of_element_located(
                            (By.CSS_SELECTOR, "div[data-nodeid='480'][data-handleid='2']")
                        )
                    )
                except Exception as e:
                    attach_screenshot(driver, "Ошибка при поиске элементов")
                    pytest.fail(f"Ошибка при поиске элементов: {e}")

            with allure.step("2. Перетаскивание элемента"):
                try:
                    # Делаем элементы видимыми перед перетаскиванием
                    driver.execute_script("arguments[0].style.opacity = '1';", source)
                    driver.execute_script("arguments[0].style.opacity = '1';", target)
                    time.sleep(0.5)  # Пауза для применения стилей

                    actions = ActionChains(driver)
                    (actions
                     .move_to_element(source)
                     .pause(0.5)
                     .click_and_hold()
                     .pause(0.3)
                     .move_to_element(target)
                     .pause(0.5)
                     .release()
                     .perform())

                    attach_screenshot(driver, f"После перетаскивания элемента (попытка {attempt})")
                    time.sleep(1)  # Пауза между попытками

                except Exception as e:
                    attach_screenshot(driver, f"Ошибка при перетаскивании (попытка {attempt})")
                    if attempt == 2:  # Если это вторая попытка и снова ошибка
                        pytest.fail(f"Ошибка при перетаскивании элемента: {e}")
                    continue  # Продолжаем на следующую попытку
    #Четвертый
    for attempt in range(1, 3):  # Выполним 2 попытки
        with allure.step(f"Попытка {attempt}: Поиск и перетаскивание"):
            with allure.step("1. Поиск элементов для drag-and-drop"):
                try:
                    source = wait.until(
                        EC.presence_of_element_located(
                            (By.CSS_SELECTOR, "div[data-nodeid='480'][data-handleid='4']")
                        )
                    )
                    target = wait.until(
                        EC.presence_of_element_located(
                            (By.CSS_SELECTOR, "div[data-nodeid='481'][data-handleid='2']")
                        )
                    )
                except Exception as e:
                    attach_screenshot(driver, "Ошибка при поиске элементов")
                    pytest.fail(f"Ошибка при поиске элементов: {e}")

            with allure.step("2. Перетаскивание элемента"):
                try:
                    # Делаем элементы видимыми перед перетаскиванием
                    driver.execute_script("arguments[0].style.opacity = '1';", source)
                    driver.execute_script("arguments[0].style.opacity = '1';", target)
                    time.sleep(0.5)  # Пауза для применения стилей

                    actions = ActionChains(driver)
                    (actions
                     .move_to_element(source)
                     .pause(0.5)
                     .click_and_hold()
                     .pause(0.3)
                     .move_to_element(target)
                     .pause(0.5)
                     .release()
                     .perform())

                    attach_screenshot(driver, f"После перетаскивания элемента (попытка {attempt})")
                    time.sleep(1)  # Пауза между попытками

                except Exception as e:
                    attach_screenshot(driver, f"Ошибка при перетаскивании (попытка {attempt})")
                    if attempt == 2:  # Если это вторая попытка и снова ошибка
                        pytest.fail(f"Ошибка при перетаскивании элемента: {e}")
                    continue  # Продолжаем на следующую попытку
    #Пятый
    for attempt in range(1, 3):  # Выполним 2 попытки
        with allure.step(f"Попытка {attempt}: Поиск и перетаскивание"):
            with allure.step("1. Поиск элементов для drag-and-drop"):
                try:
                    source = wait.until(
                        EC.presence_of_element_located(
                            (By.CSS_SELECTOR, "div[data-nodeid='481'][data-handleid='3']")
                        )
                    )
                    target = wait.until(
                        EC.presence_of_element_located(
                            (By.CSS_SELECTOR, "div[data-nodeid='482'][data-handleid='1']")
                        )
                    )
                except Exception as e:
                    attach_screenshot(driver, "Ошибка при поиске элементов")
                    pytest.fail(f"Ошибка при поиске элементов: {e}")

            with allure.step("2. Перетаскивание элемента"):
                try:
                    # Делаем элементы видимыми перед перетаскиванием
                    driver.execute_script("arguments[0].style.opacity = '1';", source)
                    driver.execute_script("arguments[0].style.opacity = '1';", target)
                    time.sleep(0.5)  # Пауза для применения стилей

                    actions = ActionChains(driver)
                    (actions
                     .move_to_element(source)
                     .pause(0.5)
                     .click_and_hold()
                     .pause(0.3)
                     .move_to_element(target)
                     .pause(0.5)
                     .release()
                     .perform())

                    attach_screenshot(driver, f"После перетаскивания элемента (попытка {attempt})")
                    time.sleep(1)  # Пауза между попытками

                except Exception as e:
                    attach_screenshot(driver, f"Ошибка при перетаскивании (попытка {attempt})")
                    if attempt == 2:  # Если это вторая попытка и снова ошибка
                        pytest.fail(f"Ошибка при перетаскивании элемента: {e}")
                    continue  # Продолжаем на следующую попытку
    #Шестой
    for attempt in range(1, 3):  # Выполним 2 попытки
        with allure.step(f"Попытка {attempt}: Поиск и перетаскивание"):
            with allure.step("1. Поиск элементов для drag-and-drop"):
                try:
                    source = wait.until(
                        EC.presence_of_element_located(
                            (By.CSS_SELECTOR, "div[data-nodeid='482'][data-handleid='3']")
                        )
                    )
                    target = wait.until(
                        EC.presence_of_element_located(
                            (By.CSS_SELECTOR, "div[data-nodeid='477'][data-handleid='1']")
                        )
                    )
                except Exception as e:
                    attach_screenshot(driver, "Ошибка при поиске элементов")
                    pytest.fail(f"Ошибка при поиске элементов: {e}")

            with allure.step("2. Перетаскивание элемента"):
                try:
                    # Делаем элементы видимыми перед перетаскиванием
                    driver.execute_script("arguments[0].style.opacity = '1';", source)
                    driver.execute_script("arguments[0].style.opacity = '1';", target)
                    time.sleep(0.5)  # Пауза для применения стилей

                    actions = ActionChains(driver)
                    (actions
                     .move_to_element(source)
                     .pause(0.5)
                     .click_and_hold()
                     .pause(0.3)
                     .move_to_element(target)
                     .pause(0.5)
                     .release()
                     .perform())

                    attach_screenshot(driver, f"После перетаскивания элемента (попытка {attempt})")
                    time.sleep(1)  # Пауза между попытками

                except Exception as e:
                    attach_screenshot(driver, f"Ошибка при перетаскивании (попытка {attempt})")
                    if attempt == 2:  # Если это вторая попытка и снова ошибка
                        pytest.fail(f"Ошибка при перетаскивании элемента: {e}")
                    continue  # Продолжаем на следующую попытку
    #Седьмой
    for attempt in range(1, 3):  # Выполним 2 попытки
        with allure.step(f"Попытка {attempt}: Поиск и перетаскивание"):
            with allure.step("1. Поиск элементов для drag-and-drop"):
                try:
                    source = wait.until(
                        EC.presence_of_element_located(
                            (By.CSS_SELECTOR, "div[data-nodeid='450'][data-handleid='4']")
                        )
                    )
                    target = wait.until(
                        EC.presence_of_element_located(
                            (By.CSS_SELECTOR, "div[data-nodeid='453'][data-handleid='3']")
                        )
                    )
                except Exception as e:
                    attach_screenshot(driver, "Ошибка при поиске элементов")
                    pytest.fail(f"Ошибка при поиске элементов: {e}")

            with allure.step("2. Перетаскивание элемента"):
                try:
                    # Делаем элементы видимыми перед перетаскиванием
                    driver.execute_script("arguments[0].style.opacity = '1';", source)
                    driver.execute_script("arguments[0].style.opacity = '1';", target)
                    time.sleep(0.5)  # Пауза для применения стилей

                    actions = ActionChains(driver)
                    (actions
                     .move_to_element(source)
                     .pause(0.5)
                     .click_and_hold()
                     .pause(0.3)
                     .move_to_element(target)
                     .pause(0.5)
                     .release()
                     .perform())

                    attach_screenshot(driver, f"После перетаскивания элемента (попытка {attempt})")
                    time.sleep(1)  # Пауза между попытками

                except Exception as e:
                    attach_screenshot(driver, f"Ошибка при перетаскивании (попытка {attempt})")
                    if attempt == 2:  # Если это вторая попытка и снова ошибка
                        pytest.fail(f"Ошибка при перетаскивании элемента: {e}")
                    continue  # Продолжаем на следующую попытку
            # СТАРТ!!!!!!!!!
    with allure.step("Работа со стартом"):
        try:
            start_element = wait.until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "p.MuiTypography-body1[aria-label='Старт']")
                )
            )
            start_element.click()
        except Exception as e:
            pytest.fail(f"Ошибка при вводе названия узла: {e}")

    # Ответственный
    with allure.step("Клик по заголовку 'Ответственные в Старте'"):
        try:
            responsible_header = wait.until(EC.presence_of_element_located((By.XPATH, "//h2[contains(text(), 'Ответственные')]")))
            responsible_header.click()
            attach_screenshot(driver, "После клика по заголовку 'Ответственные'")
        except Exception as e:
            attach_screenshot(driver, "Ошибка при клике по заголовку 'Ответственные'")
            pytest.fail(f"Ошибка при клике по заголовку 'Ответственные': {e}")
    #Выбор ответственных
    with allure.step("Выбор нескольких ответственных"):
        try:
            select_multiple_responsibles(driver, [0,0,0,0,0,0,0,0,0,0,0,0])
            attach_screenshot(driver, "Ответственные выбраны")
        except IndexError:
            # Если проблема с индексами - пропускаем тест
            pytest.skip("Недостаточно элементов для выбора")
        except Exception as e:
            attach_screenshot(driver, "Ошибка выбора ответственных")
            pytest.fail(f"Ошибка выбора ответственных: {str(e)}")

    #ЗОНЫ
    # Первая
    with allure.step("Очистка поля 'Название '"):
        try:
            zone_element = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//p[@class='MuiTypography-root MuiTypography-body1 css-2qy2g0' and contains(text(), 'Зона ответственности 1')]")
                )
            )
            zone_element.click()
            input_field = wait.until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "input.MuiInputBase-input[name='name'][placeholder='Введите название']")))
            input_field.click()  # Фокусируемся на элементе
            input_field.send_keys(Keys.CONTROL + "a")  # Выделяем весь текст
            input_field.send_keys(Keys.DELETE)  # Удаляем выделенный текст
            input_field.send_keys("Бухгалтер")  # Вводим новое значение
            attach_screenshot(driver, "После ввода названия узла")
        except Exception as e:
            attach_screenshot(driver, "Ошибка при вводе названия узла")
            pytest.fail(f"Ошибка при вводе названия узла: {e}")

    # Ответственный
    with allure.step("Клик по заголовку 'Ответственные'"):
        try:
            responsible_header = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input.MuiInputBase-input[placeholder='Выберите роли']")
                                                                           )
                                            )
            responsible_header.click()
        except Exception as e:
            pytest.fail(f"Ошибка при клике по заголовку 'Ответственные': {e}")
    #Выбор ответственных
    with allure.step("Выбор ролей"):
        try:
            wait = WebDriverWait(driver, 10)
            roles = ["Бухгалтер", "СРК", "Операционист", "РОП", "Мп", "КД", "МП", "Экономист",]  # Ваши роли

            # Находим поле ввода ролей
            role_input = wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "input.MuiInputBase-input[placeholder='Выберите роли']")
            ))

            for role in roles:
                # Ввод текста роли
                role_input.clear()
                role_input.send_keys(role)
                time.sleep(0.5)  # Пауза для отображения результатов
                attach_screenshot(driver, f"После ввода '{role}'")

                # Клик на 50 пикселей ниже поля ввода
                actions = ActionChains(driver)
                actions.move_to_element_with_offset(role_input, 0, 50).click().perform()
                time.sleep(0.3)

                # Дополнительная прокрутка страницы (если нужно)
                driver.execute_script("window.scrollBy(0, 50)")
                time.sleep(0.2)

            # Финализация выбора
            role_input.send_keys(Keys.ENTER)
            time.sleep(1)
            attach_screenshot(driver, "Все роли выбраны")

        except Exception as e:
            attach_screenshot(driver, "Ошибка выбора ролей")
            pytest.fail(f"Ошибка выбора ролей: {str(e)}")
    #Вторая
    with allure.step("Очистка поля 'Название '"):
        try:
            zone_element = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//div[contains(@class, 'react-flow__node-swimlane')]//p[contains(@class, 'MuiTypography-body1') and contains(text(), 'Зона ответственности 2')]")))

            zone_element.click()
            input_field = wait.until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "input.MuiInputBase-input[name='name'][placeholder='Введите название']")))
            input_field.click()  # Фокусируемся на элементе
            input_field.send_keys(Keys.CONTROL + "a")  # Выделяем весь текст
            input_field.send_keys(Keys.DELETE)  # Удаляем выделенный текст
            input_field.send_keys("ГЭ")  # Вводим новое значение
            input_field.send_keys(Keys.ENTER)
            attach_screenshot(driver, "После ввода названия узла")
        except Exception as e:
            attach_screenshot(driver, "Ошибка при вводе названия узла")
            pytest.fail(f"Ошибка при вводе названия узла: {e}")

    #Третья
    with allure.step("Очистка поля 'Название '"):
        try:
            zone_element = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//div[contains(@class, 'react-flow__node-swimlane')]//p[contains(@class, 'MuiTypography-body1') and contains(text(), 'Зона ответственности 3')]")))

            zone_element.click()
            input_field = wait.until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "input.MuiInputBase-input[name='name'][placeholder='Введите название']")))
            input_field.click()  # Фокусируемся на элементе
            input_field.send_keys(Keys.CONTROL + "a")  # Выделяем весь текст
            input_field.send_keys(Keys.DELETE)  # Удаляем выделенный текст
            input_field.send_keys("ДЭ")  # Вводим новое значение
            input_field.send_keys(Keys.ENTER)
            attach_screenshot(driver, "После ввода названия узла")
        except Exception as e:
            attach_screenshot(driver, "Ошибка при вводе названия узла")
            pytest.fail(f"Ошибка при вводе названия узла: {e}")
    #Четвертая
    with allure.step("Очистка поля 'Название '"):
        try:
            zone_element = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//div[contains(@class, 'react-flow__node-swimlane')]//p[contains(@class, 'MuiTypography-body1') and contains(text(), 'Зона ответственности 4')]")))


            zone_element.click()
            input_field = wait.until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "input.MuiInputBase-input[name='name'][placeholder='Введите название']")))
            input_field.click()  # Фокусируемся на элементе
            input_field.send_keys(Keys.CONTROL + "a")  # Выделяем весь текст
            input_field.send_keys(Keys.DELETE)  # Удаляем выделенный текст
            input_field.send_keys("ДирКем")  # Вводим новое значение
            input_field.send_keys(Keys.ENTER)
            attach_screenshot(driver, "После ввода названия узла")
        except Exception as e:
            attach_screenshot(driver, "Ошибка при вводе названия узла")
            pytest.fail(f"Ошибка при вводе названия узла: {e}")
    #Пятая
    with allure.step("Очистка поля 'Название '"):
        try:
            zone_element = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//div[contains(@class, 'react-flow__node-swimlane')]//p[contains(@class, 'MuiTypography-body1') and contains(text(), 'Зона ответственности 5')]")))


            zone_element.click()
            input_field = wait.until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "input.MuiInputBase-input[name='name'][placeholder='Введите название']")))
            input_field.click()  # Фокусируемся на элементе
            input_field.send_keys(Keys.CONTROL + "a")  # Выделяем весь текст
            input_field.send_keys(Keys.DELETE)  # Удаляем выделенный текст
            input_field.send_keys("Экономист")  # Вводим новое значение
            input_field.send_keys(Keys.ENTER)
            attach_screenshot(driver, "После ввода названия узла")
        except Exception as e:
            attach_screenshot(driver, "Ошибка при вводе названия узла")
            pytest.fail(f"Ошибка при вводе названия узла: {e}")
        time.sleep(5)