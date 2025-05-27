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
        driver.get("https://dev.business-pad.com/")
        # Вход в систему
        driver.find_element(By.XPATH, '//*[@id=":r0:"]').send_keys("adminbp")
        driver.find_element(By.XPATH, '//*[@id=":r1:"]').send_keys("12") # вставь пароль
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


    # Создаем папку автотест
    with allure.step("Нажатие на кнопку 'Создать папку' и ввод текста 'Автотест'"):
        try:
            # Ожидание появления кнопки и клик
            create_folder_button = wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//h2[contains(text(), "Создать папку")]')  # Ищем элемент по тексту
            ))
            create_folder_button.click()
            # Ожидание появления поля для ввода названия папки

            folder_name_input = wait.until(EC.visibility_of_element_located(
                (By.XPATH, '//div[contains(@class, "MuiInputBase-root") and .//legend[contains(., "Создать папку")]]//input')))
            folder_name_input.send_keys("Автотест")
            folder_name_input.send_keys(Keys.ENTER)
            # Прикрепление скриншота после успешного ввода
            attach_screenshot(driver, "После ввода 'Автотест'")
        except Exception as e:
            # Прикрепление скриншота в случае ошибки
            attach_screenshot(driver, "Ошибка при создании папки")
            # Завершение теста с ошибкой
            pytest.fail(f"Не удалось создать папку: {e}")

        with allure.step("Клик по элементу 'Автотест'"):
            try:
                # Ожидание появления элемента
                element = wait.until(EC.element_to_be_clickable(
                    (By.XPATH, '//*[@id="main"]/div[1]/div/div[2]/div[3]/div[3]/div/div[2]/div/div/div/div[1]/div[1]/h6')
                ))
                # Прокрутка страницы до элемента
                driver.execute_script("arguments[0].scrollIntoView(true);", element)
                # Пауза для стабилизации элемента

                actions = ActionChains(driver)
                actions.move_to_element(element).click().perform()
                # Прикрепление скриншота после успешного клика
                attach_screenshot(driver, "После клика по 'Автотест'")
            except Exception as e:
                # Прикрепление скриншота в случае ошибки
                attach_screenshot(driver, "Ошибка при клике по 'Автотест'")
                # Завершение теста с ошибкой
                pytest.fail(f"Не удалось кликнуть по элементу 'Автотест': {e}")
                #Кнопка добавить
        with allure.step("Клик по кнопке с иконкой добавления"):
            try:
                # Ожидание появления кнопки
                button = wait.until(EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "button.MuiButtonBase-root.MuiButton-containedSecondary")
                ))
                # Прокрутка страницы до кнопки
                driver.execute_script("arguments[0].scrollIntoView(true);", button)
                # Пауза для стабилизации

                # Клик по кнопке
                actions = ActionChains(driver)
                actions.move_to_element(button).click().perform()
                # Прикрепление скриншота после успешного клика
                attach_screenshot(driver, "После клика по кнопке добавления")
            except Exception as e:
                # Прикрепление скриншота в случае ошибки
                attach_screenshot(driver, "Ошибка при клике по кнопке добавления")
                # Завершение теста с ошибкой
                pytest.fail(f"Не удалось кликнуть по кнопке добавления: {e}")

                attach_screenshot(driver, "Полотно")
            #Редактирование
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

            with allure.step("Ввод текста 'Автотест Бизнес Процесс' в поле названия процесса"):
                try:
                    # Ожидание появления поля ввода
                    process_name_input = wait.until(
                        EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Введите название процесса']"))
                    )


                    # Очистка поля ввода с помощью комбинации клавиш
                    process_name_input.send_keys(Keys.CONTROL + "a")  # Выделить весь текст
                    process_name_input.send_keys(Keys.DELETE)  # Удалить выделенный текст

                    # Ввод нового текста
                    process_name_input.send_keys("Автотест Бизнес Процесс")
                    attach_screenshot(driver, "После ввода 'Автотест Бизнес Процесс'")
                except Exception as e:
                    attach_screenshot(driver, "Ошибка при вводе текста в поле названия процесса")
                    pytest.fail(f"Не удалось ввести текст в поле названия процесса: {e}")
                # Участник $$$$$$$$$$$$$
            with allure.step("Нажатие на Участников"):
                try:
                    # Ожидание появления кнопки с иконкой стрелки вниз
                    select_participants_input = wait.until(
                        EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Выберите участников']"))
                    )
                    # Клик по кнопке
                    select_participants_input.click()
                    attach_screenshot(driver, "После нажатия на Участников")
                except Exception as e:
                    attach_screenshot(driver, "Ошибка при нажатии на Участников")
                    pytest.fail(f"Не удалось нажать на Участников: {e}")

            with allure.step("Ввод текста 'тестировщик' в выпадающее меню"):
                try:

                    search_input = driver.find_element(By.XPATH, "//input[@placeholder='Выберите участников']")
                    search_input.send_keys("тестировщик")
                    attach_screenshot(driver, "После ввода 'тестировщик'")
                except Exception as e:
                    attach_screenshot(driver, "Ошибка при вводе текста 'тестировщик'")
                    pytest.fail(f"Не удалось ввести текст 'тестировщик': {e}")

            with allure.step("Нажатие на элемент 'тестировщик' в выпадающем меню"):
                try:
                    # Ожидание появления элемента "тестировщик"
                    dropdown_item = wait.until(
                        EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Выберите участников']")))
                    # Используем ActionChains для клика на 50 пикселей ниже центра элемента
                    actions = ActionChains(driver)
                    actions.move_to_element_with_offset(dropdown_item, 0, 40).click().perform()

                    attach_screenshot(driver, "После выбора элемента 'тестировщик'")
                    #Сохранить!!!!!!!!!
                    with allure.step("Нажатие на кнопку 'Сохранить'"):
                        try:
                            # Ожидание появления кнопки "Сохранить"
                            save_button = wait.until(
                                EC.presence_of_element_located((By.XPATH, "/html/body/div/div/main/div[5]/div/div[1]/button"))
                            )
                            # Клик по кнопке "Сохранить" через JavaScript
                            driver.execute_script("arguments[0].click();", save_button)
                            attach_screenshot(driver, "После нажатия на кнопку 'Сохранить'")
                        except Exception as e:
                            attach_screenshot(driver, "Ошибка при нажатии на кнопку 'Сохранить'")
                            pytest.fail(f"Не удалось нажать на кнопку 'Сохранить': {e}")


                    # Клик по элементу "Длительность":::::::::::::::::::
                    with allure.step("Клик по элементу 'Длительность'"):
                        duration_element = wait.until(
                            EC.element_to_be_clickable((By.XPATH,
                                                        "//h6[contains(@class, 'MuiTypography-h6') and contains(text(), 'Длительность')]"))
                        )
                        duration_element.click()
                        attach_screenshot(driver, "После клика на 'Длительность'")

                    # Клик по переключателю
                    with allure.step("Клик по переключателю"):
                        switch_element = wait.until(
                            EC.element_to_be_clickable(
                                (By.CSS_SELECTOR, "span.MuiSwitch-root"))
                        )
                        # Кликаем через ActionChains для большей надежности
                        ActionChains(driver).move_to_element(switch_element).click().perform()
                        attach_screenshot(driver, "После клика на переключатель")

                except Exception as e:
                    attach_screenshot(driver, "Ошибка при выполнении действий")
                    pytest.fail(f"Не удалось выполнить действия: {e}")

                    # Сохранить
            with allure.step("Нажатие на кнопку 'Сохранить'"):
                try:
                    # Ожидание появления кнопки "Сохранить"
                    save_button = wait.until(
                        EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Сохранить')]"))
                    )
                    # Клик по кнопке "Сохранить" через JavaScript
                    driver.execute_script("arguments[0].click();", save_button)
                    attach_screenshot(driver, "После нажатия на кнопку 'Сохранить'")
                except Exception as e:
                    attach_screenshot(driver, "Ошибка при нажатии на кнопку 'Сохранить'")
                    pytest.fail(f"Не удалось нажать на кнопку 'Сохранить': {e}")
                    # Обратно на полотно

            with allure.step("Нажатие на кнопку 'Полотно процесса'"):
                try:
                    # Ожидание появления кнопки "Полотно процесса"
                    canvas_button = wait.until(
                        EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Полотно процесса')]"))
                    )
                    # Клик по кнопке "Полотно процесса" через JavaScript
                    driver.execute_script("arguments[0].click();", canvas_button)
                    attach_screenshot(driver, "После нажатия на кнопку 'Полотно процесса'")
                except Exception as e:
                    attach_screenshot(driver, "Ошибка при нажатии на кнопку 'Полотно процесса'")
                    pytest.fail(f"Не удалось нажать на кнопку 'Полотно процесса': {e}")

  # ПОЛОТНО!!!!!!!!!!!!!!!!!!!!!!!!!!

    # Найти перетаскиваемый элемент
    with allure.step("Поиск перетаскиваемого элемента"):
        try:
            draggable = driver.find_element(By.CSS_SELECTOR, ".MuiGrid-container[draggable='true']")
        except Exception as e:
            pytest.fail(f"Не удалось найти перетаскиваемый элемент: {e}")

    with allure.step("Поиск области, куда нужно перетащить элемент"):
        try:
            drop_zone = driver.find_element(By.CSS_SELECTOR, ".react-flow__viewport")
        except Exception as e:
            pytest.fail(f"Не удалось найти область для перетаскивания: {e}")

    with allure.step("Выполнение drag & drop"):
        try:
            actions = ActionChains(driver)
            actions.click_and_hold(draggable).move_to_element(drop_zone).release().perform()

        except Exception as e:
            pytest.fail(f"Ошибка при выполнении drag & drop: {e}")

    with allure.step("Проверка появления элемента в нужном месте"):
        try:
            assert "swimlane" in drop_zone.get_attribute("innerHTML"), "Элемент не появился"
        except AssertionError as e:
            pytest.fail(f"Проверка не пройдена: {e}")
#Название
    with allure.step("Очистка поля 'Название узла' и ввод 'Этап Автотеста'"):
        try:
            name_input = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Введите название узла']")))
            attach_screenshot(driver, "Элемент найден, перед кликом")  # Скриншот перед кликом
            name_input.click()  # Фокусируемся на элементе
            name_input.send_keys(Keys.CONTROL + "a")  # Выделяем весь текст
            name_input.send_keys(Keys.DELETE)  # Удаляем выделенный текст
            name_input.send_keys("Этап Автотеста")  # Вводим новое значение
            attach_screenshot(driver, "После ввода названия узла")
        except Exception as e:
            attach_screenshot(driver, "Ошибка при вводе названия узла")
            pytest.fail(f"Ошибка при вводе названия узла: {e}")
#Описание
    with allure.step("Ввод 'Автотест описание' в поле 'Описание узла'"):
        try:
            description_input = wait.until(EC.visibility_of_element_located((By.XPATH, "//textarea[@placeholder='Введите описание узла']")))
            description_input.send_keys("Автотест описание")
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

    with allure.step("Клик по полю 'Выберите ответственных'"):
        try:
            responsible_input = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Выберите ответственных']")))
            responsible_input.click()
            attach_screenshot(driver, "После клика по полю 'Выберите ответственных'")
        except Exception as e:
            attach_screenshot(driver, "Ошибка при клике по полю 'Выберите ответственных'")
            pytest.fail(f"Ошибка при клике по полю 'Выберите ответственных': {e}")

        #Выбор тестировщика!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    try:
        with allure.step("Клик по элементу autocomplete-popper и нажатие Enter"):
            # Ожидание появления элемента
            autocomplete_popper = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//div[contains(@class, 'MuiAutocomplete-popper') and contains(@class, 'MuiPopper-root')]")))
            attach_screenshot(driver, "Элемент найден, перед кликом")  # Скриншот перед кликом
            print(f"DEBUG: Найден элемент autocomplete-popper, {autocomplete_popper}")

            # Клик по элементу
            autocomplete_popper.click()
            attach_screenshot(driver, "После клика по элементу")

            # Нажатие клавиши Enter
            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ENTER)
            attach_screenshot(driver, "После нажатия Enter")
    except Exception as e:
        attach_screenshot(driver, "Ошибка при клике по элементу или нажатии Enter")
        pytest.fail(f"Ошибка при клике по элементу или нажатии Enter: {e}")

        attach_screenshot(driver, "Отображение на полотне")
        # Удаление

    try:
        with allure.step("Клик по конкретным трем точкам"):
            print("Ищу все кнопки с тремя точками...")
            time.sleep(2)
            all_buttons = wait.until(EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "button.MuiIconButton-root")

            ))

            # Фильтруем только видимые кнопки
            visible_buttons = [
                btn for btn in all_buttons
                if btn.value_of_css_property('opacity') == '1'
                   and btn.value_of_css_property('visibility') != 'hidden'
            ]

            if not visible_buttons:
                raise Exception("Не найдено видимых кнопок с тремя точками")

            target_index = 8  # Измените при необходимости 34 67
            button = visible_buttons[target_index] if len(visible_buttons) > target_index else visible_buttons[-1]

            # Кликаем по нужной кнопке
            ActionChains(driver) \
                .move_to_element(button) \
                .pause(0.3) \
                .click() \
                .perform()
            attach_screenshot(driver, "После клика по выбранным трем точкам")

            print("Клик по трем точкам выполнен, жду появления меню...")


    except Exception as e:
        attach_screenshot(driver, "Ошибка при клике")
        pytest.fail(f"Ошибка при клике по трем точкам: {str(e)}")

        # Ждем появления меню после клика
    try:
        with allure.step("Ожидание появления меню с опцией 'Удалить'"):
            delete_option = wait.until(EC.presence_of_element_located(
                (By.XPATH, "/html/body/div[2]/div[3]/ul/li[2]")
            ))
            print("Меню найдено, продолжаю тест.")
    except Exception as e:
        attach_screenshot(driver, "Меню не появилось после клика")
        pytest.fail(f"Меню с кнопкой 'Удалить' не появилось: {str(e)}")

        # Кликаем по пункту "Удалить"
    try:
        with allure.step("Клик по пункту 'Удалить'"):
            ActionChains(driver) \
                .move_to_element_with_offset(delete_option, 10, 5) \
                .pause(0.3) \
                .click() \
                .perform()

            attach_screenshot(driver, "После клика на Удалить")
            print("Клик по 'Удалить' выполнен.")
    except Exception as e:
        attach_screenshot(driver, "Ошибка при клике на Удалить")
        pytest.fail(f"Ошибка при клике на Удалить: {str(e)}")

        # Подтверждение удаления
    try:
        with allure.step("Подтверждение удаления (Enter)"):
            ActionChains(driver).send_keys(Keys.ENTER).perform()
            print("Enter на подтверждение удаления отправлен.")
    except Exception as e:
        attach_screenshot(driver, "Ошибка при подтверждении удаления")
        pytest.fail(f"Ошибка при подтверждении удаления: {str(e)}")
    try:
        with allure.step("Клик по кнопке 'Подтвердить'"):
            # Ожидаем появления и кликабельности кнопки
            confirm_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Подтвердить')]")))

            # Кликаем через ActionChains для надежности
            ActionChains(driver).move_to_element(confirm_button).pause(0.3).click().perform()

            attach_screenshot(driver, "После клика на кнопку 'Подтвердить'")

    except Exception as e:
        attach_screenshot(driver, "Ошибка при клике на 'Подтвердить'")
        pytest.fail(f"Ошибка при клике на кнопку 'Подтвердить': {str(e)}")

# Удаление папки
    with allure.step("Клик по ссылке 'Настройки'"):
        try:
            # Ожидаем, пока элемент станет кликабельным
            settings_link = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//a[contains(@class, 'css-t7enrq') and @href='/settings']")
            ))
            attach_screenshot(driver, "Перед кликом по Настройкам")

            # Кликаем через Selenium
            settings_link.click()
            print("Клик по ссылке 'Настройки' выполнен.")

            attach_screenshot(driver, "После клика по Настройкам")

        except Exception as e:
            attach_screenshot(driver, "Ошибка при клике на Настройки")
            print(f"Ошибка: {e}")
    #!!!!!!!!!!!!!!!!!!!!!!!!
            with allure.step("Клик по 'Список бизнес-процессов'"):
                # Ожидаем и кликаем по тексту
                button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "div.MuiGrid-container.css-r9stk3"))
                )
                assert "Список бизнес-процессов" in button.text, "Текст кнопки не совпадает"
                button.click()

                attach_screenshot(driver, "После клика по списку БП")

            # Финалочка
            """"
            try:
                with allure.step("Клик по конкретным трем точкам"):
                    time.sleep(3)
                    # 1. Находим ВСЕ элементы с тремя точками
                    all_buttons = wait.until(EC.presence_of_all_elements_located(
                        (By.CSS_SELECTOR, "button.MuiIconButton-root")
                    ))

                    visible_buttons = [
                        btn for btn in all_buttons
                        if btn.value_of_css_property('opacity') == '1'
                           and btn.value_of_css_property('visibility') != 'hidden'
                    ]
                    if not visible_buttons:
                        raise Exception("Не найдено видимых кнопок с тремя точками")

                    target_index = 5  # Измените индекс на нужный при говняке 7
                    if len(visible_buttons) > target_index:
                        button = visible_buttons[target_index]
                    else:
                        button = visible_buttons[-1]
                    ActionChains(driver) \
                        .move_to_element(button) \
                        .pause(0.3) \
                        .click() \
                        .perform()
                    attach_screenshot(driver, "После клика по выбранным трем точкам")
            except Exception as e:
                attach_screenshot(driver, "Ошибка при клике")
                pytest.fail(f"Ошибка при клике по трем точкам: {str(e)}")
            # !!!!!!!!!!!!!!!!
            # Удаляем
            
            more_vert_button = wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button[tabindex='0'] svg[data-testid='MoreVertIcon']")
            ))
            ActionChains(driver).move_to_element(more_vert_button).pause(0.2).click()
            # 2. **Ждем, когда реально появится меню!**
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "ul[role='menu']")))
            print("Меню появилось!")
            # 3. **Ожидаем видимость и кликаем по пункту 'Удалить'**
            delete_option = wait.until(EC.visibility_of_element_located(
                (By.XPATH, "//li[contains(text(), 'Удалить')]")
            ))
            ActionChains(driver).move_to_element(delete_option).pause(0.3).click().perform()
    """
#Финалочка





