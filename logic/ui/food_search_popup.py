import time
from telnetlib import EC
from Utils.helper_functions import choose_random_number_in_range
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class FoodSearchPopup():
    SEARCH_FIELD = (By.XPATH, "//input[@type='search']")
    MIN_CALORIES_INPUT = (By.XPATH, "//input[@aria-label='Min Calories']")
    MAX_CALORIES_INPUT = (By.XPATH, "//input[@aria-label='Max Calories']")
    SEARCH_RESULTS_BUTTONS = (By.XPATH, "//ul[@class='svelte-142zban']//li//button")
    INGREDIENTS = (By.XPATH, "//div[./h3[contains(text(),'Ingredients')]]//span[@class='food-name _class_1x8vs_1 "
                             "svelte-ncaeor']")
    INGREDIENTS_TITLE = (By.XPATH, "//h3[contains(text(),'Ingredients')]")
    SEARCH_RESULT_FOOD_NAMES = (By.XPATH, "//span[@class='name svelte-rcnuic']")
    RESULT_CALORIES = (By.XPATH, "//dt[text()='Calories']/following-sibling::dd[@class='svelte-1qloymj']")
    ADD_FOOD_BUTTON = (By.XPATH, "//span[text()='Add']")

    def __init__(self, driver):
        self._driver = driver
        self.init_elements()

    def init_elements(self):
        WebDriverWait(self._driver, 10).until(lambda x: x.find_element(*self.MAX_CALORIES_INPUT))
        self.search_field = self._driver.find_element(*self.SEARCH_FIELD)
        self.max_calories = self._driver.find_element(*self.MAX_CALORIES_INPUT)
        self.min_calories = self._driver.find_element(*self.MIN_CALORIES_INPUT)

    # init the chosen food calories
    def init_result_calories(self):
        self.result_calories = WebDriverWait(self._driver, 5).until(
            lambda x: x.find_element(*self.RESULT_CALORIES))

    # init the add food button for the chosen food
    def init_add_food_button(self):
        self.add_food_button = self._driver.find_element(*self.ADD_FOOD_BUTTON)

    # fill te search field with a text
    def fill_search_field(self, text):
        self.search_field.send_keys(text)

    def fill_min_calories_filter(self, min):
        WebDriverWait(self._driver, 10).until(EC.element_to_be_clickable(self.MIN_CALORIES_INPUT)).click()
        self.min_calories.clear()
        self.min_calories.send_keys(min)

    def fill_max_calories_filter(self, max):
        WebDriverWait(self._driver, 10).until(EC.element_to_be_clickable(self.MAX_CALORIES_INPUT)).click()
        self.max_calories.clear()
        self.max_calories.send_keys(max)

    def init_ingredients(self):
        WebDriverWait(self._driver, 10).until(EC.presence_of_element_located(self.INGREDIENTS))

        self.ingredients_names = self._driver.find_elements(*self.INGREDIENTS)

    # get the search results after searching for food
    def init_search_result_food(self):
        WebDriverWait(self._driver, 5).until(lambda x: x.find_elements(*self.SEARCH_RESULTS_BUTTONS))
        time.sleep(2)
        self.search_result_food_buttons = self._driver.find_elements(*self.SEARCH_RESULTS_BUTTONS)
        self.search_result_food_names = self._driver.find_elements(*self.SEARCH_RESULT_FOOD_NAMES)

    def click_search_result_button_by_index(self, index):
        self.init_search_result_food()
        if index < len(self.search_result_food_buttons) > 0:
            self.search_result_food_buttons[index].click()
        else:
            raise IndexError("Search result index out of bound or no search results list is empty")

    # get the chosen food ingrediants as text
    def get_ingredient_list_as_text(self):
        names = []
        for ingredient in self.ingredients_names:
            names.append(ingredient.text.lower())
        return names

    def get_all_results_food_names_and_ingredients(self):
        self.init_search_result_food()
        index = 0
        food_list = []

        for search_result_button in self.search_result_food_buttons:
            if index == 4:
                break

            search_result_button.click()
            time.sleep(1)
            if self.is_food_result_contains_ingredients():
                self.init_ingredients()
                ingredient_list = self.get_ingredient_list_as_text()
            else:
                ingredient_list = []

            food_list.append({'name': self.search_result_food_names[index].text.lower(), 'ingredient': ingredient_list})
            index += 1

        return food_list

    def is_food_result_contains_ingredients(self):

        if len(self._driver.find_elements(*self.INGREDIENTS)) > 0:
            return True
        return False

    def get_all_search_results_calories(self):
        self.init_search_result_food()
        all_results_calories = []
        index = 0
        for search_result_button in self.search_result_food_buttons:
            if index == 4:
                break
            search_result_button.click()
            self.init_result_calories()
            all_results_calories.append(int(self.result_calories.text))
            index += 1
        return all_results_calories

    def def_choose_food_by_index_list(self, index):
        self.init_search_result_food()
        self.search_result_food_buttons[0].click()

    def choose_random_food_from_list(self):
        self.init_search_result_food()
        rand = choose_random_number_in_range(0, len(self.search_result_food_names) - 1)
        self.search_result_food_buttons[rand].click()
        return self.get_result_food_name_by_index(rand)

    def get_current_food_calories(self):
        self.init_result_calories()
        return self.result_calories.text

    def add_current_food_to_meal(self):
        self.init_add_food_button()
        self.add_food_button.click()

    def is_results_empty(self):
        time.sleep(2)
        results_list = self._driver.find_elements(*self.SEARCH_RESULTS_BUTTONS)
        return len(results_list) == 0

    def clear_search_field(self):
        self.search_field.clear()

    def get_result_food_name_by_index(self, index):
        self.init_search_result_food()
        return self.search_result_food_names[index].text.lower()
