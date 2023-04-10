import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


class InstagramScrapingClass:
    method = ["/followers", "/following"]

    def __init__(self, base_url, profile, email):
        self.base_url = base_url
        self.profile = profile
        self.email = email
        self.open_instagram()

    def open_instagram(self) -> None:
        options = Options()
        options.add_argument("--disable-dev-shm-usage")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        self.driver.get(self.base_url)
        print("Application title is ", self.driver.title)

    def get_users(self, method_index) -> list[str]:
        time.sleep(1)
        self.driver.get(self.base_url + "/" + self.profile)
        time.sleep(3)
        self.driver.find_element(
            By.XPATH,
            "//a[contains(@href, '{v1}')]".format(v1=self.method[method_index]),
        ).click()
        time.sleep(1)
        scroll_box = self.driver.find_element(By.XPATH, "//div[@class='_aano']")
        # height variable
        last_ht, ht = 0, 1
        while last_ht != ht:
            last_ht = ht
            time.sleep(2)
            # scroll down and retrun the height of scroll (JS script)
            ht = self.driver.execute_script(
                """ 
                arguments[0].scrollTo(0, arguments[0].scrollHeight);
                return arguments[0].scrollHeight; """,
                scroll_box,
            )
        links = scroll_box.find_elements(By.TAG_NAME, "a")
        user_list = [name.text for name in links if name.text != '']
        return user_list

    def login(self):
        time.sleep(1)
        # Problem with possible translations - TODO: Search general solution
        self.driver.find_element(
            By.XPATH, "//button[text()='Permitir solo cookies necesarias']"
        ).click()
        username = self.driver.find_element(By.CSS_SELECTOR, "input[name='username']")
        password = self.driver.find_element(By.CSS_SELECTOR, "input[name='password']")
        username.clear()
        password.clear()
        print("Enter your username")
        username.send_keys(self.email)
        print("Enter your password")
        password_input = input()
        password.send_keys(password_input)
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        # wait for login success
        time.sleep(3)
        try:
            self.driver.find_element(
                By.XPATH, "//button[contains(text(),'Ahora no')]"
            ).click()
        except:
            print("No element found")
        time.sleep(1)
        try:
            self.driver.find_element(
                By.XPATH, "//button[contains(text(),'Ahora no')]"
            ).click()
        except:
            print("No element found")

    def close(self):
        self.driver.close()
