from selenium.webdriver.common.by import By

from infra.ui.base_page import BasePage

class Menu(BasePage):
    NUTRITIONAL_TARGET_NAVIGATION = (By.XPATH, "//a[@type='button']/span[text()='Nutrition Targets']")
    MENU = (By.XPATH, "//button[@title='Open Menu']")
    DIET_NUTRITION_NAVIGATION = (By.XPATH, "//button[text() = 'Diet & Nutrition']")
    MEAL_AND_SCHEDUAL_BUTTON = (By.XPATH, "//*[@id='app']/div[1]/div/nav/div/div[3]/ul[3]/li[2]/button")
    MEAL_SETTINGS = (By.XPATH, "//*[@id='app']/div[1]/div/nav/div/div[3]/ul[3]/li[2]/ul/li[1]/a")
    PLANNER = (By.XPATH,"//*[@id='app']/div[1]/div/nav/div/div[3]/ul[1]/li[1]/a")

    def __init__(self, driver):
        self._driver = driver
        self.init_menue()

    def init_menue(self):
        self.menu = self.wait_for_element_in_page_by_xpath(self.MENU[1])

    def click_menu(self):
        self.menu.click()

    def go_to_diet_and_nutrition(self):
        self.wait_for_element_in_page_by_xpath(self.DIET_NUTRITION_NAVIGATION[1]).click()

    def go_to_nutritional_target_page(self):
        self.wait_for_element_in_page_by_xpath(self.NUTRITIONAL_TARGET_NAVIGATION[1]).click()

    def go_to_meal_and_schedule(self):
        self.wait_for_element_in_page_by_xpath(self.MEAL_AND_SCHEDUAL_BUTTON[1]).click()

    def go_to_meal_settings(self):
        self.wait_for_element_in_page_by_xpath(self.MEAL_SETTINGS[1]).click()

    def go_to_planner_page(self):
        self.wait_for_element_in_page_by_xpath(self.PLANNER[1]).click()
