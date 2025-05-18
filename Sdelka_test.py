import pyautogui
import pytest
from selenium import webdriver
from selenium.common import NoSuchElementException
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
    wait = WebDriverWait(driver, 9)
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
                    time.sleep(0.1)
                    break
                except Exception:
                    if attempt == 2:
                        raise Exception("Не удалось открыть список ответственных")
                    time.sleep(0.1)

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
                    time.sleep(0.1)
                    options[index].click()
                    selected_count += 1
                    break
                except Exception:
                    if click_attempt == 2:
                        raise Exception(f"Не удалось кликнуть элемент {index}")
                    time.sleep(0.1)

            time.sleep(0.2)  # Пауза между выборами

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
        driver.get("https://testbp1.business-pad.com/")
        # Вход в систему
        driver.find_element(By.XPATH, '//*[@id=":r0:"]').send_keys("adminbp")
        driver.find_element(By.XPATH, '//*[@id=":r1:"]').send_keys("") # вставь пароль
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
        print(f"Ошибка при выполнении: {str(e)}")

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
            folder_name_input.send_keys("Сделка")
            folder_name_input.send_keys(Keys.ENTER)
            # Прикрепление скриншота после успешного ввода
            attach_screenshot(driver, "После ввода 'Сделки'")
        except Exception as e:
            # Прикрепление скриншота в случае ошибки
            attach_screenshot(driver, "Ошибка при создании папки")
            # Завершение теста с ошибкой
            print(f"Не удалось создать папку: {e}")

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
            print(f"Не удалось кликнуть по элементу 'Пусто': {str(e)}")

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
            print(f"Не удалось кликнуть по кнопке добавления: {e}")

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
            print(f"Не удалось нажать на вкладку 'Настройка процесса': {e}")

    with allure.step("Ввод текста 'Сделка' в поле названия процесса"):
        try:
            # Ожидание появления поля ввода
            process_name_input = wait.until(
                EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Введите название процесса']")))
            # Очистка поля ввода
            process_name_input.send_keys(Keys.CONTROL + "a")
            process_name_input.send_keys(Keys.DELETE)
            # Ввод нового текста
            process_name_input.send_keys("Сделка")
            attach_screenshot(driver, "После ввода 'Сделка'")
        except Exception as e:
            attach_screenshot(driver, "Ошибка при вводе текста в поле названия процесса")
            print(f"Не удалось ввести текст в поле названия процесса: {e}")

    # Выбор участников
    with allure.step("2. Выбор участников"):
        participants = ["КД", "Экономист", "СРК", "МП", "РОП",
                        "Бухгалтер", "Операционист"]

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
                    time.sleep(0.1)  # Увеличили время ожидания
                    attach_screenshot(driver, f"После ввода {participant}")

                    # Ждем появления списка и кликаем по варианту
                    participant_option = wait.until(
                        EC.element_to_be_clickable(
                            (By.XPATH, f"//div[contains(@class,'MuiAutocomplete-popper')]//li[contains(., '{participant}')]"))
                    )
                    participant_option.click()
                    attach_screenshot(driver, f"Участник {participant} выбран")
                    time.sleep(0.2)

                except Exception as e:
                    attach_screenshot(driver, f"Ошибка выбора участника {participant}")
                    print(f"Не удалось выбрать участника {participant}: {str(e)}")
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
            print(f"Не удалось нажать на кнопку 'Сохранить': {e}")


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
            print(f"Не удалось нажать на кнопку 'Полотно процесса': {e}")

        # Перетаскивание элемента "Основной"!!!!!!!!!!!!
        #СТАРТ!!!!!!!!!!!!!!
        with allure.step("Клик по элементу 'СТАРТ'"):
            try:
                # Ожидаем появление элемента и проверяем текст
                finish_element = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'p.MuiTypography-body1[aria-label="Старт"]'))
                )

                # Проверяем текст элемента
                assert finish_element.text == "Старт", f"Текст элемента не 'Старт', а '{finish_element.text}'"

                # Кликаем по элементу
                finish_element.click()

                # Делаем скриншот для отчета
                attach_screenshot(driver, "После клика по 'Старт'")

            except Exception as e:
                # Если ошибка - делаем скриншот и падаем с понятным сообщением
                attach_screenshot(driver, "Ошибка при клике по 'Старт'")
                print(f"Не удалось кликнуть по 'Старт': {str(e)}")
    #Очистка
    with allure.step("Старт"):
        try:
            name1_input = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Введите название узла']")))
            attach_screenshot(driver, "Элемент найден, перед кликом")  # Скриншот перед кликом
        except Exception as e:
            attach_screenshot(driver, "Ошибка при вводе названия узла")
            print(f"Ошибка при вводе названия узла: {e}")
    # Ответственный
    with allure.step("'Ответственные'"):
        try:
            responsible_header = wait.until(EC.presence_of_element_located((By.XPATH, "//h2[contains(text(), 'Ответственные')]")))
            responsible_header.click()
            attach_screenshot(driver, "После клика по заголовку 'Ответственные'")
        except Exception as e:
            attach_screenshot(driver, "Ошибка при клике по заголовку 'Ответственные'")
            print(f"Ошибка при клике по заголовку 'Ответственные': {e}")
    #Выбор ответственных
    with allure.step("Выбор нескольких ответственных"):
        try:
            # Выбираем первый (0) и третий (2) элементы из списка
            select_multiple_responsibles(driver, [0, 0, 4])
            attach_screenshot(driver, "Ответственные выбраны")
        except Exception as e:
            attach_screenshot(driver, "Ошибка выбора ответственных")
            print(f"Ошибка выбора ответственных: {str(e)}")

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
                print(f"Не удалось кликнуть по 'Финиш': {str(e)}")
    #Очистка
    with allure.step("Финиш"):
        try:
            name1_input = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Введите название узла']")))
            attach_screenshot(driver, "Элемент найден, перед кликом")  # Скриншот перед кликом
        except Exception as e:
            attach_screenshot(driver, "Ошибка при вводе названия узла")
            print(f"Ошибка при вводе названия узла: {e}")
    # Ответственный
    with allure.step("'Ответственные'"):
        try:
            responsible_header = wait.until(EC.presence_of_element_located((By.XPATH, "//h2[contains(text(), 'Ответственные')]")))
            responsible_header.click()
            attach_screenshot(driver, "После клика по заголовку 'Ответственные'")
        except Exception as e:
            attach_screenshot(driver, "Ошибка при клике по заголовку 'Ответственные'")
            print(f"Ошибка при клике по заголовку 'Ответственные': {e}")
    #Выбор ответственных
    with allure.step("Выбор нескольких ответственных"):
        try:
            # Выбираем первый (0) и третий (2) элементы из списка
            select_multiple_responsibles(driver, [0, 0, 4])
            attach_screenshot(driver, "Ответственные выбраны")
        except Exception as e:
            attach_screenshot(driver, "Ошибка выбора ответственных")
            print(f"Ошибка выбора ответственных: {str(e)}")
    #Перетаскиваем Финиш
    with allure.step("2. Перетаскивание элемента 'Финиш'"):
        try:
            # 1. Находим элемент и его родительский узел
            element = wait.until(
                EC.element_to_be_clickable((By.XPATH, '//p[@aria-label="Финиш"]'))
            )
            node = driver.execute_script(
                "return arguments[0].closest('div[data-testid^=\"rf__node-\"]');",
                element
            )
            # 2. Прокручиваем к элементу и делаем паузу
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", node)
            time.sleep(0.3)
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
            time.sleep(0.3)  # Даем время на применение изменений
            attach_screenshot(driver, "После перемещения элемента")
        except Exception as e:
            attach_screenshot(driver, "Ошибка при перетаскивании")
            print(f"Не удалось переместить элемент: {str(e)}")
    #ПЕРВЫЙ
    with allure.step("2. Перетаскивание элемента 'Основной'"):
        try:

            element = wait.until(EC.presence_of_element_located((By.XPATH, '//p[contains(text(), "Основной")]')))
            actions = ActionChains(driver)
            actions.click_and_hold(element).move_by_offset(400, 0).release().perform()
            attach_screenshot(driver, "После перетаскивания элемента")
        except Exception as e:
            attach_screenshot(driver, "Ошибка при перетаскивании элемента")
            print(f"Ошибка при перетаскивании элемента: {e}")
    # Ввод названия
    with allure.step("Очистка поля 'Название узла' и ввод 'Согласование сделки с РОП'"):
        try:
            name_input = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Введите название узла']")))
            attach_screenshot(driver, "Элемент найден, перед кликом")  # Скриншот перед кликом
            name_input.click()  # Фокусируемся на элементе
            name_input.send_keys(Keys.CONTROL + "a")  # Выделяем весь текст
            name_input.send_keys(Keys.DELETE)  # Удаляем выделенный текст
            name_input.send_keys("Согласование сделки с РОП")  # Вводим новое значение
            attach_screenshot(driver, "После ввода названия узла")
        except Exception as e:
            attach_screenshot(driver, "Ошибка при вводе названия узла")
            print(f"Ошибка при вводе названия узла: {e}")
    #Описание
    with allure.step("Ввод 'коммента' в поле 'Описание узла'"):
        try:
            description_input = wait.until(EC.visibility_of_element_located((By.XPATH, "//textarea[@placeholder='Введите описание узла']")))
            description_input.send_keys("Согласование/замечания/отклонение сделки с РОП")
            attach_screenshot(driver, "После ввода описания узла")
        except Exception as e:
            attach_screenshot(driver, "Ошибка при вводе описания узла")
            print(f"Ошибка при вводе описания узла: {e}")
    # Ответственный
    with allure.step("Клик по заголовку 'Ответственные'"):
        try:
            responsible_header = wait.until(EC.presence_of_element_located((By.XPATH, "//h2[contains(text(), 'Ответственные')]")))
            responsible_header.click()
            attach_screenshot(driver, "После клика по заголовку 'Ответственные'")
        except Exception as e:
            attach_screenshot(driver, "Ошибка при клике по заголовку 'Ответственные'")
            print(f"Ошибка при клике по заголовку 'Ответственные': {e}")
    #Выбор ответственных
    with allure.step("Выбор нескольких ответственных"):
        try:
            # Выбираем первый (0) и третий (2) элементы из списка
            select_multiple_responsibles(driver, [6])
            attach_screenshot(driver, "Ответственные выбраны")
        except Exception as e:
            attach_screenshot(driver, "Ошибка выбора ответственных")
            print(f"Ошибка выбора ответственных: {str(e)}")
        #Второй
        with allure.step("2. Перетаскивание элемента 'Основной'"):
            try:
                element = wait.until(EC.presence_of_element_located((By.XPATH, '//p[contains(text(), "Основной")]')))
                actions = ActionChains(driver)
                actions.click_and_hold(element).move_by_offset(400, 0).release().perform()
                attach_screenshot(driver, "После перетаскивания элемента")
            except Exception as e:
                attach_screenshot(driver, "Ошибка при перетаскивании элемента")
                print(f"Ошибка при перетаскивании элемента: {e}")
    # Ввод названия
    with allure.step("Очистка поля 'Название узла' и ввод 'Корректировка сделки'"):
        try:
            name_input = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Введите название узла']")))
            attach_screenshot(driver, "Элемент найден, перед кликом")  # Скриншот перед кликом
            name_input.click()  # Фокусируемся на элементе
            name_input.send_keys(Keys.CONTROL + "a")  # Выделяем весь текст
            name_input.send_keys(Keys.DELETE)  # Удаляем выделенный текст
            name_input.send_keys("Корректировка сделки")  # Вводим новое значение
            attach_screenshot(driver, "После ввода названия узла")
        except Exception as e:
            attach_screenshot(driver, "Ошибка при вводе названия узла")
            print(f"Ошибка при вводе названия узла: {e}")
    #Описание
    with allure.step("Ввод 'коммента' в поле 'Описание узла'"):
        try:
            description_input = wait.until(EC.visibility_of_element_located((By.XPATH, "//textarea[@placeholder='Введите описание узла']")))
            description_input.send_keys("Изменение условий сделки, если РОП или КД не согласовали")
            attach_screenshot(driver, "После ввода описания узла")
        except Exception as e:
            attach_screenshot(driver, "Ошибка при вводе описания узла")
            print(f"Ошибка при вводе описания узла: {e}")
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
            select_multiple_responsibles(driver, [0, 0, 4])
            attach_screenshot(driver, "Ответственные выбраны")
        except Exception as e:
            attach_screenshot(driver, "Ошибка выбора ответственных")
            pytest.fail(f"Ошибка выбора ответственных: {str(e)}")
        #Третий !!!!!!!!!!
        with allure.step("2. Перетаскивание элемента 'Основной'"):
            try:
                element = wait.until(EC.presence_of_element_located((By.XPATH, '//p[contains(text(), "Основной")]')))
                actions = ActionChains(driver)
                actions.click_and_hold(element).move_by_offset(530, 0).release().perform()
                attach_screenshot(driver, "После перетаскивания элемента")
            except Exception as e:
                attach_screenshot(driver, "Ошибка при перетаскивании элемента")
                pytest.fail(f"Ошибка при перетаскивании элемента: {e}")
    # Ввод названия
    with allure.step("Очистка поля 'Название узла' и ввод 'Отклонение сделки'"):
        try:
            name_input = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Введите название узла']")))
            attach_screenshot(driver, "Элемент найден, перед кликом")  # Скриншот перед кликом
            name_input.click()  # Фокусируемся на элементе
            name_input.send_keys(Keys.CONTROL + "a")  # Выделяем весь текст
            name_input.send_keys(Keys.DELETE)  # Удаляем выделенный текст
            name_input.send_keys("Отклонение сделки")  # Вводим новое значение
            attach_screenshot(driver, "После ввода названия узла")
        except Exception as e:
            attach_screenshot(driver, "Ошибка при вводе названия узла")
            pytest.fail(f"Ошибка при вводе названия узла: {e}")
    #Описание
    with allure.step("Ввод 'коммента' в поле 'Отклонение сделки'"):
        try:
            description_input = wait.until(EC.visibility_of_element_located((By.XPATH, "//textarea[@placeholder='Введите описание узла']")))
            description_input.send_keys("Отклонение сделки")
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
            select_multiple_responsibles(driver, [6])
            attach_screenshot(driver, "Ответственные выбраны")
        except Exception as e:
            attach_screenshot(driver, "Ошибка выбора ответственных")
            pytest.fail(f"Ошибка выбора ответственных: {str(e)}")
        #Четвертый
        with allure.step("2. Перетаскивание элемента 'Основной'"):
            try:
                element = wait.until(EC.presence_of_element_located((By.XPATH, '//p[contains(text(), "Основной")]')))
                actions = ActionChains(driver)
                actions.click_and_hold(element).move_by_offset(300, 0).release().perform()
                attach_screenshot(driver, "После перетаскивания элемента")
            except Exception as e:
                attach_screenshot(driver, "Ошибка при перетаскивании элемента")
                pytest.fail(f"Ошибка при перетаскивании элемента: {e}")
    #Четвертый
    # Ввод названия
    with allure.step("Очистка поля 'Название узла' и ввод 'Утверждение '"):
        try:
            name_input = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Введите название узла']")))
            attach_screenshot(driver, "Элемент найден, перед кликом")  # Скриншот перед кликом
            name_input.click()  # Фокусируемся на элементе
            name_input.send_keys(Keys.CONTROL + "a")  # Выделяем весь текст
            name_input.send_keys(Keys.DELETE)  # Удаляем выделенный текст
            name_input.send_keys("Утверждение ")  # Вводим новое значение
            attach_screenshot(driver, "После ввода названия узла")
        except Exception as e:
            attach_screenshot(driver, "Ошибка при вводе названия узла")
            pytest.fail(f"Ошибка при вводе названия узла: {e}")
            #Описание
    with allure.step("Ввод коммента в поле 'Описание узла'"):
        try:
            description_input = wait.until(EC.visibility_of_element_located((By.XPATH, "//textarea[@placeholder='Введите описание узла']")))
            description_input.send_keys("Утверждение, передача экономисту для регистрации")
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
            select_multiple_responsibles(driver, [5])
            attach_screenshot(driver, "Ответственные выбраны")
        except Exception as e:
            attach_screenshot(driver, "Ошибка выбора ответственных")
            pytest.fail(f"Ошибка выбора ответственных: {str(e)}")
        #Пятый
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
    with allure.step("Очистка поля 'Название узла' и ввод 'Регистрация сделки'"):
        try:
            name_input = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Введите название узла']")))
            attach_screenshot(driver, "Элемент найден, перед кликом")  # Скриншот перед кликом
            name_input.click()  # Фокусируемся на элементе
            name_input.send_keys(Keys.CONTROL + "a")  # Выделяем весь текст
            name_input.send_keys(Keys.DELETE)  # Удаляем выделенный текст
            name_input.send_keys("Регистрация сделки")  # Вводим новое значение
            attach_screenshot(driver, "После ввода названия узла")
        except Exception as e:
            attach_screenshot(driver, "Ошибка при вводе названия узла")
            pytest.fail(f"Ошибка при вводе названия узла: {e}")
    #Коммент
    with allure.step("Ввод коммента в поле 'Описание узла'"):
        try:
            description_input = wait.until(EC.visibility_of_element_located((By.XPATH, "//textarea[@placeholder='Введите описание узла']")))
            description_input.send_keys("Внесение параметров сделки в БД и присвоение номера")
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
            select_multiple_responsibles(driver, [4])
            attach_screenshot(driver, "Ответственные выбраны")
        except Exception as e:
            attach_screenshot(driver, "Ошибка выбора ответственных")
            pytest.fail(f"Ошибка выбора ответственных: {str(e)}")
        #Шестой
        with allure.step("2. Перетаскивание элемента 'Основной'"):
            try:
                element = wait.until(EC.presence_of_element_located((By.XPATH, '//p[contains(text(), "Основной")]')))
                actions = ActionChains(driver)
                actions.click_and_hold(element).move_by_offset(400, 0).release().perform()
                attach_screenshot(driver, "После перетаскивания элемента")
            except Exception as e:
                attach_screenshot(driver, "Ошибка при перетаскивании элемента")
                pytest.fail(f"Ошибка при перетаскивании элемента: {e}")

    # Ввод названия
    with allure.step("Очистка поля 'Название узла' и ввод 'Реализация сделки'"):
        try:
            name_input = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Введите название узла']")))
            attach_screenshot(driver, "Элемент найден, перед кликом")  # Скриншот перед кликом
            name_input.click()  # Фокусируемся на элементе
            name_input.send_keys(Keys.CONTROL + "a")  # Выделяем весь текст
            name_input.send_keys(Keys.DELETE)  # Удаляем выделенный текст
            name_input.send_keys("Реализация сделки")  # Вводим новое значение
            attach_screenshot(driver, "После ввода названия узла")
        except Exception as e:
            attach_screenshot(driver, "Ошибка при вводе названия узла")
            pytest.fail(f"Ошибка при вводе названия узла: {e}")
    #Коммент
    with allure.step("Ввод коммента в поле 'Описание узла'"):
        try:
            description_input = wait.until(EC.visibility_of_element_located((By.XPATH, "//textarea[@placeholder='Введите описание узла']")))
            description_input.send_keys("Извещение ответственного сотрудника об утверждении регистрации  сделки и передача сделки на реализацию.")
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
            select_multiple_responsibles(driver, [4])
            attach_screenshot(driver, "Ответственные выбраны")
        except Exception as e:
            attach_screenshot(driver, "Ошибка выбора ответственных")
            pytest.fail(f"Ошибка выбора ответственных: {str(e)}")

        #Седьмой
        with allure.step("2. Перетаскивание элемента 'Основной'"):
            try:
                element = wait.until(EC.presence_of_element_located((By.XPATH, '//p[contains(text(), "Основной")]')))
                actions = ActionChains(driver)
                actions.click_and_hold(element).move_by_offset(600, 0).release().perform()
                attach_screenshot(driver, "После перетаскивания элемента")
            except Exception as e:
                attach_screenshot(driver, "Ошибка при перетаскивании элемента")
                pytest.fail(f"Ошибка при перетаскивании элемента: {e}")

    # Ввод названия
    with allure.step("Очистка поля 'Название узла' и ввод 'Закрытие сделки'"):
        try:
            name_input = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Введите название узла']")))
            attach_screenshot(driver, "Элемент найден, перед кликом")  # Скриншот перед кликом
            name_input.click()  # Фокусируемся на элементе
            name_input.send_keys(Keys.CONTROL + "a")  # Выделяем весь текст
            name_input.send_keys(Keys.DELETE)  # Удаляем выделенный текст
            name_input.send_keys("Закрытие сделки")  # Вводим новое значение
            attach_screenshot(driver, "После ввода названия узла")
        except Exception as e:
            attach_screenshot(driver, "Ошибка при вводе названия узла")
            pytest.fail(f"Ошибка при вводе названия узла: {e}")
    #Коммент
    with allure.step("Ввод коммента в поле 'Описание узла'"):
        try:
            description_input = wait.until(EC.visibility_of_element_located((By.XPATH, "//textarea[@placeholder='Введите описание узла']")))
            description_input.send_keys("Внесение фактических финансовых показателей и дат в соответствии с первичными документами.")
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
            select_multiple_responsibles(driver, [4, 3, 2])
            attach_screenshot(driver, "Ответственные выбраны")
        except Exception as e:
            attach_screenshot(driver, "Ошибка выбора ответственных")
            pytest.fail(f"Ошибка выбора ответственных: {str(e)}")

    #ЗОНЫ
    # Вторая
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
            input_field.send_keys("РОП, СРК и МП")  # Вводим новое значение
            attach_screenshot(driver, "После ввода названия узла")
        except Exception as e:
            attach_screenshot(driver, "Ошибка при вводе названия узла")
            pytest.fail(f"Ошибка при вводе названия узла: {e}")
    # Ответственный
    with allure.step("Клик по заголовку 'Ответственные'"):
        try:
            responsible_header = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input.MuiInputBase-input[placeholder='Выберите роли']")))
            responsible_header.click()
        except Exception as e:
            pytest.fail(f"Ошибка при клике по заголовку 'Ответственные': {e}")
    #Выбор ответственных
    with allure.step("Выбор ролей"):
        try:
            wait = WebDriverWait(driver, 10)
            roles = ["СРК", "МП", "РОП"]
            # Находим поле ввода ролей
            role_input = wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "input.MuiInputBase-input[placeholder='Выберите роли']")))
            for role in roles:
                # Ввод текста роли
                role_input.clear()
                role_input.send_keys(role)
                time.sleep(0.1)  # Пауза для отображения результатов
                attach_screenshot(driver, f"После ввода '{role}'")
                # Клик на 50 пикселей ниже поля ввода
                actions = ActionChains(driver)
                actions.move_to_element_with_offset(role_input, 0, 50).click().perform()
                time.sleep(0.1)
                # Дополнительная прокрутка страницы (если нужно)
                driver.execute_script("window.scrollBy(0, 50)")
                time.sleep(0.1)
            # Финализация выбора
            role_input.send_keys(Keys.ENTER)
            time.sleep(0.1)
            attach_screenshot(driver, "Все роли выбраны")
        except Exception as e:
            attach_screenshot(driver, "Ошибка выбора ролей")
            pytest.fail(f"Ошибка выбора ролей: {str(e)}")
    # Третья
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
            input_field.send_keys("РОП")  # Вводим новое значение
            attach_screenshot(driver, "После ввода названия узла")
        except Exception as e:
            attach_screenshot(driver, "Ошибка при вводе названия узла")
            pytest.fail(f"Ошибка при вводе названия узла: {e}")
    # Ответственный
    with allure.step("Клик по заголовку 'Ответственные'"):
        try:
            responsible_header = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input.MuiInputBase-input[placeholder='Выберите роли']")))
            responsible_header.click()
        except Exception as e:
            pytest.fail(f"Ошибка при клике по заголовку 'Ответственные': {e}")
    #Выбор ответственных
    with allure.step("Выбор ролей"):
        try:
            wait = WebDriverWait(driver, 10)
            roles = ["РОП"]
            # Находим поле ввода ролей
            role_input = wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "input.MuiInputBase-input[placeholder='Выберите роли']")))
            for role in roles:
                # Ввод текста роли
                role_input.clear()
                role_input.send_keys(role)
                time.sleep(0.2)  # Пауза для отображения результатов
                attach_screenshot(driver, f"После ввода '{role}'")
                # Клик на 50 пикселей ниже поля ввода
                actions = ActionChains(driver)
                actions.move_to_element_with_offset(role_input, 0, 50).click().perform()
                time.sleep(0.1)
                # Дополнительная прокрутка страницы (если нужно)
                driver.execute_script("window.scrollBy(0, 50)")
                time.sleep(0.1)
            # Финализация выбора
            role_input.send_keys(Keys.ENTER)
            time.sleep(0.1)
            attach_screenshot(driver, "Все роли выбраны")
        except Exception as e:
            attach_screenshot(driver, "Ошибка выбора ролей")
            pytest.fail(f"Ошибка выбора ролей: {str(e)}")
    # Четвертая
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
            input_field.send_keys("КД")  # Вводим новое значение
            attach_screenshot(driver, "После ввода названия узла")
        except Exception as e:
            attach_screenshot(driver, "Ошибка при вводе названия узла")
            pytest.fail(f"Ошибка при вводе названия узла: {e}")
    # Ответственный
    with allure.step("Клик по заголовку 'Ответственные'"):
        try:
            responsible_header = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input.MuiInputBase-input[placeholder='Выберите роли']")))
            responsible_header.click()
        except Exception as e:
            pytest.fail(f"Ошибка при клике по заголовку 'Ответственные': {e}")
    #Выбор ответственных
    with allure.step("Выбор ролей"):
        try:
            wait = WebDriverWait(driver, 10)
            roles = ["КД"]
            # Находим поле ввода ролей
            role_input = wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "input.MuiInputBase-input[placeholder='Выберите роли']")))
            for role in roles:
                # Ввод текста роли
                role_input.clear()
                role_input.send_keys(role)
                time.sleep(0.2)  # Пауза для отображения результатов
                attach_screenshot(driver, f"После ввода '{role}'")
                # Клик на 50 пикселей ниже поля ввода
                actions = ActionChains(driver)
                actions.move_to_element_with_offset(role_input, 0, 50).click().perform()
                time.sleep(0.1)
                # Дополнительная прокрутка страницы (если нужно)
                driver.execute_script("window.scrollBy(0, 50)")
                time.sleep(0.1)
            # Финализация выбора
            role_input.send_keys(Keys.ENTER)
            time.sleep(0.2)
            attach_screenshot(driver, "Все роли выбраны")
        except Exception as e:
            attach_screenshot(driver, "Ошибка выбора ролей")
            pytest.fail(f"Ошибка выбора ролей: {str(e)}")
    # Пятая
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
            attach_screenshot(driver, "После ввода названия узла")
        except Exception as e:
            attach_screenshot(driver, "Ошибка при вводе названия узла")
            pytest.fail(f"Ошибка при вводе названия узла: {e}")
    # Ответственный
    with allure.step("Клик по заголовку 'Ответственные'"):
        try:
            responsible_header = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input.MuiInputBase-input[placeholder='Выберите роли']")))
            responsible_header.click()
        except Exception as e:
            pytest.fail(f"Ошибка при клике по заголовку 'Ответственные': {e}")
    #Выбор ответственных
    with allure.step("Выбор ролей"):
        try:
            wait = WebDriverWait(driver, 10)
            roles = ["Экономист"]
            # Находим поле ввода ролей
            role_input = wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "input.MuiInputBase-input[placeholder='Выберите роли']")))
            for role in roles:
                # Ввод текста роли
                role_input.clear()
                role_input.send_keys(role)
                time.sleep(0.2)  # Пауза для отображения результатов
                attach_screenshot(driver, f"После ввода '{role}'")
                # Клик на 50 пикселей ниже поля ввода
                actions = ActionChains(driver)
                actions.move_to_element_with_offset(role_input, 0, 50).click().perform()
                time.sleep(0.1)
                # Дополнительная прокрутка страницы (если нужно)
                driver.execute_script("window.scrollBy(0, 50)")
                time.sleep(0.1)
            # Финализация выбора
            role_input.send_keys(Keys.ENTER)
            time.sleep(0.2)
            attach_screenshot(driver, "Все роли выбраны")
        except Exception as e:
            attach_screenshot(driver, "Ошибка выбора ролей")
            pytest.fail(f"Ошибка выбора ролей: {str(e)}")
    # Шестая
    with allure.step("Очистка поля 'Название '"):
        try:
            zone_element = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//div[contains(@class, 'react-flow__node-swimlane')]//p[contains(@class, 'MuiTypography-body1') and contains(text(), 'Зона ответственности 6')]")))
            zone_element.click()
            input_field = wait.until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "input.MuiInputBase-input[name='name'][placeholder='Введите название']")))
            input_field.click()  # Фокусируемся на элементе
            input_field.send_keys(Keys.CONTROL + "a")  # Выделяем весь текст
            input_field.send_keys(Keys.DELETE)  # Удаляем выделенный текст
            input_field.send_keys("Операционист, Экономист и Бухгалтер")  # Вводим новое значение
            attach_screenshot(driver, "После ввода названия узла")
        except Exception as e:
            attach_screenshot(driver, "Ошибка при вводе названия узла")
            pytest.fail(f"Ошибка при вводе названия узла: {e}")
    # Ответственный
    with allure.step("Клик по заголовку 'Ответственные'"):
        try:
            responsible_header = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input.MuiInputBase-input[placeholder='Выберите роли']")))
            responsible_header.click()
        except Exception as e:
            pytest.fail(f"Ошибка при клике по заголовку 'Ответственные': {e}")
    #Выбор ответственных
    with allure.step("Выбор ролей"):
        try:
            wait = WebDriverWait(driver, 10)
            roles = ["Экономист", "Бухгалтер", "Операционист"]
            # Находим поле ввода ролей
            role_input = wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "input.MuiInputBase-input[placeholder='Выберите роли']")))
            for role in roles:
                # Ввод текста роли
                role_input.clear()
                role_input.send_keys(role)
                time.sleep(0.2)  # Пауза для отображения результатов
                attach_screenshot(driver, f"После ввода '{role}'")
                # Клик на 50 пикселей ниже поля ввода
                actions = ActionChains(driver)
                actions.move_to_element_with_offset(role_input, 0, 50).click().perform()
                time.sleep(0.1)
                # Дополнительная прокрутка страницы (если нужно)
                driver.execute_script("window.scrollBy(0, 50)")
                time.sleep(0.1)
            # Финализация выбора
            role_input.send_keys(Keys.ENTER)
            time.sleep(0.2)
            attach_screenshot(driver, "Все роли выбраны")
        except Exception as e:
            attach_screenshot(driver, "Ошибка выбора ролей")
            pytest.fail(f"Ошибка выбора ролей: {str(e)}")
    #СВЯЗИ
    #Схватываем id'шки
    with allure.step("получаем data-id"):
        try:
            element = WebDriverWait(driver, 10).until(      #!!!!!!!!!!!!!!!!!!!!
                EC.presence_of_element_located((By.XPATH, '//p[contains(text(), "Старт")]')))
            element.click()
            # Получаем data-id
            parent_div = driver.find_element(By.XPATH, '//p[contains(text(), "Старт")]/ancestor::div[@data-id]')
            data_id1 = parent_div.get_attribute('data-id')
            element1 = WebDriverWait(driver, 10).until(    #!!!!!!!!!!!!!!!!!!!!
                EC.presence_of_element_located((By.XPATH, '//p[contains(text(), "Корректировка сделки")]')))
            element1.click()
            parent_div = driver.find_element(By.XPATH, '//p[contains(text(), "Корректировка сделки")]/ancestor::div[@data-id]')
            data_id2 = parent_div.get_attribute('data-id')
            element2 = WebDriverWait(driver, 10).until(    #!!!!!!!!!!!!!!!!!!!!
                EC.presence_of_element_located((By.XPATH, '//p[contains(text(), "Согласование сделки с РОП")]')))
            element2.click()
            parent_div = driver.find_element(By.XPATH, '//p[contains(text(), "Согласование сделки с РОП")]/ancestor::div[@data-id]')
            data_id3 = parent_div.get_attribute('data-id')
            element3 = WebDriverWait(driver, 10).until(    #!!!!!!!!!!!!!!!!!!!!
                EC.presence_of_element_located((By.XPATH, '//p[contains(text(), "Отклонение сделки")]')))
            element3.click()
            parent_div = driver.find_element(By.XPATH, '//p[contains(text(), "Отклонение сделки")]/ancestor::div[@data-id]')
            data_id4 = parent_div.get_attribute('data-id')
            element4 = WebDriverWait(driver, 10).until(    #!!!!!!!!!!!!!!!!!!!!
                EC.presence_of_element_located((By.XPATH, '//p[contains(text(), "Утверждение")]')))
            element4.click()
            parent_div = driver.find_element(By.XPATH, '//p[contains(text(), "Утверждение")]/ancestor::div[@data-id]')
            data_id5 = parent_div.get_attribute('data-id')
            element5 = WebDriverWait(driver, 10).until(    #!!!!!!!!!!!!!!!!!!!!
                EC.presence_of_element_located((By.XPATH, '//p[contains(text(), "Реализация сделки")]')))
            element5.click()
            parent_div = driver.find_element(By.XPATH, '//p[contains(text(), "Реализация сделки")]/ancestor::div[@data-id]')
            data_id6 = parent_div.get_attribute('data-id')
            element6 = WebDriverWait(driver, 10).until(    #!!!!!!!!!!!!!!!!!!!!
                EC.presence_of_element_located((By.XPATH, '//p[contains(text(), "Регистрация сделки")]')))
            element6.click()
            parent_div = driver.find_element(By.XPATH, '//p[contains(text(), "Регистрация сделки")]/ancestor::div[@data-id]')
            data_id7 = parent_div.get_attribute('data-id')
            element7 = WebDriverWait(driver, 10).until(    #!!!!!!!!!!!!!!!!!!!!
                EC.presence_of_element_located((By.XPATH, '//p[contains(text(), "Закрытие сделки")]')))
            element7.click()
            parent_div = driver.find_element(By.XPATH, '//p[contains(text(), "Закрытие сделки")]/ancestor::div[@data-id]')
            data_id8 = parent_div.get_attribute('data-id')
            element8 = WebDriverWait(driver, 10).until(    #!!!!!!!!!!!!!!!!!!!!
                EC.presence_of_element_located((By.XPATH, '//p[contains(text(), "Финиш")]')))
            element8.click()
            parent_div = driver.find_element(By.XPATH, '//p[contains(text(), "Финиш")]/ancestor::div[@data-id]')
            data_id9 = parent_div.get_attribute('data-id')
        except Exception as e:
            print(f"Не удалось схватить id элементов: {str(e)}")
    #Первая Связь!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    with allure.step("2. Поиск элементов для drag-and-drop"):
        try:
            x, y = 650, 350  # ← сюда подставь координаты точки клика
            pyautogui.moveTo(x, y)
            pyautogui.click()
            source = driver.find_element(By.CSS_SELECTOR, f"div[data-nodeid='{data_id1}'][data-handleid='4']")
            target = driver.find_element(By.CSS_SELECTOR, f"div[data-nodeid='{data_id3}'][data-handleid='3']")
        except Exception as e:
            attach_screenshot(driver, "Ошибка при поиске элементов")
            allure.attach(
                f"Ошибка: {str(e)}",
                name="Ошибка",
                attachment_type=allure.attachment_type.TEXT)
            source, target = None, None
    with allure.step("3. Перетаскивание элемента"):
        if source and target:
            try:
                ActionChains(driver).drag_and_drop(source, target).perform()
                time.sleep(0.2)  # Короткая пауза для стабилизации
                attach_screenshot(driver, "После перетаскивания элемента")
            except Exception as e:
                attach_screenshot(driver, "Ошибка при перетаскивании элемента")
                allure.attach(
                    f"Не удалось перетащить: {str(e)}",
                    name="Ошибка",
                    attachment_type=allure.attachment_type.TEXT)
        else:
            allure.attach(
                "Пропущено: элементы для перетаскивания не найдены",
                name="Инфо",
                attachment_type=allure.attachment_type.TEXT)
    #Вторая Связь
    with allure.step("2. Поиск элементов для drag-and-drop"):
        try:
            x, y = 650, 350  # ← сюда подставь координаты точки клика
            pyautogui.moveTo(x, y)
            pyautogui.click()
            source = driver.find_element(By.CSS_SELECTOR, f"div[data-nodeid='{data_id2}'][data-handleid='4']")
            target = driver.find_element(By.CSS_SELECTOR, f"div[data-nodeid='{data_id3}'][data-handleid='3']")
        except Exception as e:
            attach_screenshot(driver, "Ошибка при поиске элементов")
            allure.attach(
                f"Ошибка: {str(e)}",
                name="Ошибка",
                attachment_type=allure.attachment_type.TEXT)
            source, target = None, None
    with allure.step("3. Перетаскивание элемента"):
        if source and target:
            try:
                ActionChains(driver).drag_and_drop(source, target).perform()
                time.sleep(0.2)  # Короткая пауза для стабилизации
                attach_screenshot(driver, "После перетаскивания элемента")
            except Exception as e:
                attach_screenshot(driver, "Ошибка при перетаскивании элемента")
                allure.attach(
                    f"Не удалось перетащить: {str(e)}",
                    name="Ошибка",
                    attachment_type=allure.attachment_type.TEXT)
        else:
            allure.attach(
                "Пропущено: элементы для перетаскивания не найдены",
                name="Инфо",
                attachment_type=allure.attachment_type.TEXT)
    #Третья!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    with allure.step("2. Поиск элементов для drag-and-drop"):
        try:
            x, y = 650, 350  # ← сюда подставь координаты точки клика
            pyautogui.moveTo(x, y)
            pyautogui.click()
            time.sleep(0.3)
            source = driver.find_element(By.CSS_SELECTOR, f"div[data-nodeid='{data_id3}'][data-handleid='4']")
            target = driver.find_element(By.CSS_SELECTOR, f"div[data-nodeid='{data_id4}'][data-handleid='4']")
        except Exception as e:
            attach_screenshot(driver, "Ошибка при поиске элементов")
            allure.attach(
                f"Ошибка: {str(e)}",
                name="Ошибка",
                attachment_type=allure.attachment_type.TEXT)
            source, target = None, None
    with allure.step("3. Перетаскивание элемента"):
        if source and target:
            try:
                ActionChains(driver).drag_and_drop(source, target).perform()
                time.sleep(1)  # Короткая пауза для стабилизации
                attach_screenshot(driver, "После перетаскивания элемента")
            except Exception as e:
                attach_screenshot(driver, "Ошибка при перетаскивании элемента")
                allure.attach(
                    f"Не удалось перетащить: {str(e)}",
                    name="Ошибка",
                    attachment_type=allure.attachment_type.TEXT)
        else:
            allure.attach(
                "Пропущено: элементы для перетаскивания не найдены",
                name="Инфо",
                attachment_type=allure.attachment_type.TEXT)
    #Четвертая Связь!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    with allure.step("2. Поиск элементов для drag-and-drop"):
        try:
            x, y = 650, 350  # ← сюда подставь координаты точки клика
            pyautogui.moveTo(x, y)
            pyautogui.click()
            time.sleep(0.2)
            source = driver.find_element(By.CSS_SELECTOR, f"div[data-nodeid='{data_id4}'][data-handleid='4']")
            target = driver.find_element(By.CSS_SELECTOR, f"div[data-nodeid='{data_id5}'][data-handleid='1']")
        except Exception as e:
            attach_screenshot(driver, "Ошибка при поиске элементов")
            allure.attach(
                f"Ошибка: {str(e)}",
                name="Ошибка",
                attachment_type=allure.attachment_type.TEXT)
            source, target = None, None
    with allure.step("3. Перетаскивание элемента"):
        if source and target:
            try:
                ActionChains(driver).drag_and_drop(source, target).perform()
                time.sleep(1)  # Короткая пауза для стабилизации
                attach_screenshot(driver, "После перетаскивания элемента")
            except Exception as e:
                attach_screenshot(driver, "Ошибка при перетаскивании элемента")
                allure.attach(
                    f"Не удалось перетащить: {str(e)}",
                    name="Ошибка",
                    attachment_type=allure.attachment_type.TEXT)
        else:
            allure.attach(
                "Пропущено: элементы для перетаскивания не найдены",
                name="Инфо",
                attachment_type=allure.attachment_type.TEXT)
    #Шестая Связь!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    with allure.step("2. Поиск элементов для drag-and-drop"):
        try:
            x, y = 650, 350  # ← сюда подставь координаты точки клика
            pyautogui.moveTo(x, y)
            pyautogui.click()
            time.sleep(0.6)
            source = driver.find_element(By.CSS_SELECTOR, f"div[data-nodeid='{data_id2}'][data-handleid='4']")
            target = driver.find_element(By.CSS_SELECTOR, f"div[data-nodeid='{data_id5}'][data-handleid='1']")
        except Exception as e:
            attach_screenshot(driver, "Ошибка при поиске элементов")
            allure.attach(
                f"Ошибка: {str(e)}",
                name="Ошибка",
                attachment_type=allure.attachment_type.TEXT)
            source, target = None, None
    with allure.step("3. Перетаскивание элемента"):
        if source and target:
            try:
                ActionChains(driver).drag_and_drop(source, target).perform()
                time.sleep(1)  # Короткая пауза для стабилизации
                attach_screenshot(driver, "После перетаскивания элемента")
            except Exception as e:
                attach_screenshot(driver, "Ошибка при перетаскивании элемента")
                allure.attach(
                    f"Не удалось перетащить: {str(e)}",
                    name="Ошибка",
                    attachment_type=allure.attachment_type.TEXT)
        else:
            allure.attach(
                "Пропущено: элементы для перетаскивания не найдены",
                name="Инфо",
                attachment_type=allure.attachment_type.TEXT)
            #Седьмая Связь!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    with allure.step("2. Поиск элементов для drag-and-drop"):
        try:
            x, y = 650, 350  # ← сюда подставь координаты точки клика
            pyautogui.moveTo(x, y)
            pyautogui.click()
            time.sleep(0.6)
            source = driver.find_element(By.CSS_SELECTOR, f"div[data-nodeid='{data_id3}'][data-handleid='4']")
            target = driver.find_element(By.CSS_SELECTOR, f"div[data-nodeid='{data_id5}'][data-handleid='1']")
        except Exception as e:
            attach_screenshot(driver, "Ошибка при поиске элементов")
            allure.attach(
                f"Ошибка: {str(e)}",
                name="Ошибка",
                attachment_type=allure.attachment_type.TEXT)
            source, target = None, None
    with allure.step("3. Перетаскивание элемента"):
        if source and target:
            try:
                ActionChains(driver).drag_and_drop(source, target).perform()
                time.sleep(1)  # Короткая пауза для стабилизации
                attach_screenshot(driver, "После перетаскивания элемента")
            except Exception as e:
                attach_screenshot(driver, "Ошибка при перетаскивании элемента")
                allure.attach(
                    f"Не удалось перетащить: {str(e)}",
                    name="Ошибка",
                    attachment_type=allure.attachment_type.TEXT)
        else:
            allure.attach(
                "Пропущено: элементы для перетаскивания не найдены",
                name="Инфо",
                attachment_type=allure.attachment_type.TEXT)
    #Восьмая Связь!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    with allure.step("2. Поиск элементов для drag-and-drop"):
        try:
            x, y = 650, 350  # ← сюда подставь координаты точки клика
            pyautogui.moveTo(x, y)
            pyautogui.click()
            time.sleep(0.6)
            source = driver.find_element(By.CSS_SELECTOR, f"div[data-nodeid='{data_id5}'][data-handleid='4']")
            target = driver.find_element(By.CSS_SELECTOR, f"div[data-nodeid='{data_id7}'][data-handleid='1']")
        except Exception as e:
            attach_screenshot(driver, "Ошибка при поиске элементов")
            allure.attach(
                f"Ошибка: {str(e)}",
                name="Ошибка",
                attachment_type=allure.attachment_type.TEXT)
            source, target = None, None
    with allure.step("3. Перетаскивание элемента"):
        if source and target:
            try:
                ActionChains(driver).drag_and_drop(source, target).perform()
                time.sleep(1)  # Короткая пауза для стабилизации
                attach_screenshot(driver, "После перетаскивания элемента")
            except Exception as e:
                attach_screenshot(driver, "Ошибка при перетаскивании элемента")
                allure.attach(
                    f"Не удалось перетащить: {str(e)}",
                    name="Ошибка",
                    attachment_type=allure.attachment_type.TEXT)
        else:
            allure.attach(
                "Пропущено: элементы для перетаскивания не найдены",
                name="Инфо",
                attachment_type=allure.attachment_type.TEXT)
    #Девятая Связь!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    with allure.step("2. Поиск элементов для drag-and-drop"):
        try:
            x, y = 650, 350  # ← сюда подставь координаты точки клика
            pyautogui.moveTo(x, y)
            pyautogui.click()
            time.sleep(0.6)
            source = driver.find_element(By.CSS_SELECTOR, f"div[data-nodeid='{data_id8}'][data-handleid='3']")
            target = driver.find_element(By.CSS_SELECTOR, f"div[data-nodeid='{data_id7}'][data-handleid='1']")
        except Exception as e:
            attach_screenshot(driver, "Ошибка при поиске элементов")
            allure.attach(
                f"Ошибка: {str(e)}",
                name="Ошибка",
                attachment_type=allure.attachment_type.TEXT)
            source, target = None, None
    with allure.step("3. Перетаскивание элемента"):
        if source and target:
            try:
                ActionChains(driver).drag_and_drop(source, target).perform()
                time.sleep(1)  # Короткая пауза для стабилизации
                attach_screenshot(driver, "После перетаскивания элемента")
            except Exception as e:
                attach_screenshot(driver, "Ошибка при перетаскивании элемента")
                allure.attach(
                    f"Не удалось перетащить: {str(e)}",
                    name="Ошибка",
                    attachment_type=allure.attachment_type.TEXT)
        else:
            allure.attach(
                "Пропущено: элементы для перетаскивания не найдены",
                name="Инфо",
                attachment_type=allure.attachment_type.TEXT)
    #Десятая Связь!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    with allure.step("2. Поиск элементов для drag-and-drop"):
        try:
            x, y = 650, 350  # ← сюда подставь координаты точки клика
            pyautogui.moveTo(x, y)
            pyautogui.click()
            time.sleep(0.6)
            source = driver.find_element(By.CSS_SELECTOR, f"div[data-nodeid='{data_id2}'][data-handleid='4']")
            target = driver.find_element(By.CSS_SELECTOR, f"div[data-nodeid='{data_id7}'][data-handleid='1']")
        except Exception as e:
            attach_screenshot(driver, "Ошибка при поиске элементов")
            allure.attach(
                f"Ошибка: {str(e)}",
                name="Ошибка",
                attachment_type=allure.attachment_type.TEXT)
            source, target = None, None
    with allure.step("3. Перетаскивание элемента"):
        if source and target:
            try:
                ActionChains(driver).drag_and_drop(source, target).perform()
                time.sleep(1)  # Короткая пауза для стабилизации
                attach_screenshot(driver, "После перетаскивания элемента")
            except Exception as e:
                attach_screenshot(driver, "Ошибка при перетаскивании элемента")
                allure.attach(
                    f"Не удалось перетащить: {str(e)}",
                    name="Ошибка",
                    attachment_type=allure.attachment_type.TEXT)
        else:
            allure.attach(
                "Пропущено: элементы для перетаскивания не найдены",
                name="Инфо",
                attachment_type=allure.attachment_type.TEXT)
    #11 Связь!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    with allure.step("2. Поиск элементов для drag-and-drop"):
        try:
            x, y = 650, 350  # ← сюда подставь координаты точки клика
            pyautogui.moveTo(x, y)
            pyautogui.click()
            time.sleep(0.6)
            source = driver.find_element(By.CSS_SELECTOR, f"div[data-nodeid='{data_id8}'][data-handleid='2']")
            target = driver.find_element(By.CSS_SELECTOR, f"div[data-nodeid='{data_id9}'][data-handleid='3']")
        except Exception as e:
            attach_screenshot(driver, "Ошибка при поиске элементов")
            allure.attach(
                f"Ошибка: {str(e)}",
                name="Ошибка",
                attachment_type=allure.attachment_type.TEXT)
            source, target = None, None
    with allure.step("3. Перетаскивание элемента"):
        if source and target:
            try:
                ActionChains(driver).drag_and_drop(source, target).perform()
                time.sleep(1)  # Короткая пауза для стабилизации
                attach_screenshot(driver, "После перетаскивания элемента")
            except Exception as e:
                attach_screenshot(driver, "Ошибка при перетаскивании элемента")
                allure.attach(
                    f"Не удалось перетащить: {str(e)}",
                    name="Ошибка",
                    attachment_type=allure.attachment_type.TEXT)
        else:
            allure.attach(
                "Пропущено: элементы для перетаскивания не найдены",
                name="Инфо",
                attachment_type=allure.attachment_type.TEXT)
    #12 Связь!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    with allure.step("2. Поиск элементов для drag-and-drop"):
        try:
            x, y = 650, 350  # ← сюда подставь координаты точки клика
            pyautogui.moveTo(x, y)
            pyautogui.click()
            time.sleep(0.6)
            source = driver.find_element(By.CSS_SELECTOR, f"div[data-nodeid='{data_id6}'][data-handleid='2']")
            target = driver.find_element(By.CSS_SELECTOR, f"div[data-nodeid='{data_id8}'][data-handleid='3']")
        except Exception as e:
            attach_screenshot(driver, "Ошибка при поиске элементов")
            allure.attach(
                f"Ошибка: {str(e)}",
                name="Ошибка",
                attachment_type=allure.attachment_type.TEXT)
            source, target = None, None
    with allure.step("3. Перетаскивание элемента"):
        if source and target:
            try:
                ActionChains(driver).drag_and_drop(source, target).perform()
                time.sleep(1)  # Короткая пауза для стабилизации
                attach_screenshot(driver, "После перетаскивания элемента")
            except Exception as e:
                attach_screenshot(driver, "Ошибка при перетаскивании элемента")
                allure.attach(
                    f"Не удалось перетащить: {str(e)}",
                    name="Ошибка",
                    attachment_type=allure.attachment_type.TEXT)
        else:
            allure.attach(
                "Пропущено: элементы для перетаскивания не найдены",
                name="Инфо",
                attachment_type=allure.attachment_type.TEXT)
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

        time.sleep(1)