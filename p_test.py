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
        driver.get("https://team.business-pad.com/")
        # Вход в систему
        driver.find_element(By.XPATH, '//*[@id=":r0:"]').send_keys("K.Bekir")
        driver.find_element(By.XPATH, '//*[@id=":r1:"]').send_keys("Team.Bekir")
        driver.find_element(By.XPATH, '//*[@id="root"]/div/main/div/div/div/div[2]/div/form/div/div[4]').click()
        attach_screenshot(driver, "После логина")
        driver.get("https://team.business-pad.com/settings")


        with allure.step("Клик по 'Список бизнес-процессов'"):
            # Ожидаем и кликаем по тексту
            button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "div.MuiGrid-container.css-r9stk3"))
            )
            assert "Список бизнес-процессов" in button.text, "Текст кнопки не совпадает"
            button.click()

            attach_screenshot(driver, "После клика по списку БП")

#Финалочка

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
        """
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






