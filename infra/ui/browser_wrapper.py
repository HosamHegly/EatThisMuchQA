import time
from os.path import dirname, join
from Utils import cookies
from selenium import webdriver
from Utils.json_reader import get_config_data


class BrowserWrapper:
    COOKIE = cookies.cookie

    def __init__(self):
        self.driver = None
        self.config = get_config_data()

    def get_driver(self, browser):
        options = self.get_browser_options(browser)

        if self.config["grid"]:
            self.driver = webdriver.Remote(command_executor=self.config["hub"], options=options)
        else:
            # Local WebDriver setup based on the browser type.
            if browser.lower() == 'chrome':
                self.driver = webdriver.Chrome(options=options)
            elif browser.lower() == 'firefox':
                self.driver = webdriver.Firefox(options=options)
            elif browser.lower() == 'edge':
                self.driver = webdriver.Edge(options=options)
            else:
                raise ValueError(f"Unsupported browser type: {browser}")

        self.driver.get(self.config["url"])
        time.sleep(2)

        return self.driver

    def close_browser(self):
        if self.driver:
            self.driver.close()

    def is_parallel(self):
        return self.parallel

    def close_browser(self):
        if self.driver:
            self.driver.quit()

    def refresh(self):
        self.driver.refresh()

    def get_browsers(self):
        return self.config["browser_types"]

    def get_filename(self, filename):
        here = dirname(__file__)
        output = join(here, filename)
        return output

    def is_grid(self):
        return self.config['grid']

    def get_browser(self):
        return self.config['browser']

    # add cookies to driver inorder to  skip login
    def add_browser_cookie(self):
        for cookie in self.COOKIE:
            self.driver.add_cookie(cookie)

    def goto(self, url):
        self.driver.get(url)

    def get_browser_options(self, browser_type):
        # Initialize options object based on browser type
        if browser_type.lower() == 'chrome':
            options = webdriver.ChromeOptions()
        elif browser_type.lower() == 'firefox':
            options = webdriver.FirefoxOptions()
        elif browser_type.lower() == 'edge':
            options = webdriver.EdgeOptions()
        else:
            raise ValueError(f"Unsupported browser type: {browser_type}")

        self.add_common_options(options)

        # Add browser-specific capabilities if necessary
        if self.config.get("grid"):
            platform_name = self.config["platform"]
            options.add_argument(f'--platformName={platform_name}')

        return options

    def add_common_options(self, options):

        #options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
