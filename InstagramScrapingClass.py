from selenium.webdriver.common.by import By
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time

class InstagramScrapingClass:

    method = ["/followers", "/following"]

    def __init__(self, base_url, profile, email):
        self.base_url = base_url
        self.profile = profile
        self.email = email
        self.openInstagram()
    
    def openInstagram(self):
        options = Options()
        options.add_argument('--disable-dev-shm-usage')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options = options)
        self.driver.get(self.base_url)
        print("Application title is ", self.driver.title)
    
    def getUsers(self, methodIndex):
        time.sleep(1)
        self.driver.get(self.base_url+self.profile)
        time.sleep(1)
        self.driver.find_element(By.XPATH,"//a[contains(@href, '{v1}')]".format(v1 = self.method[methodIndex])).click()
        time.sleep(1)
        scroll_box = self.driver.find_element(By.XPATH, "//div[@class='isgrP']")
        time.sleep(3)
        # height variable
        last_ht, ht = 0, 1
        while last_ht != ht:
            last_ht = ht
            time.sleep(2)
            # scroll down and retrun the height of scroll (JS script)
            ht = self.driver.execute_script(""" 
                arguments[0].scrollTo(0, arguments[0].scrollHeight);
                return arguments[0].scrollHeight; """, scroll_box)
        users = self.driver.find_elements(By.XPATH, "//a[contains(@class, 'notranslate _0imsa ')]")
        userList = []
        for user in users:
            userList.append(user.get_attribute("title"))
        return userList

    def login(self):
        time.sleep(1)
        #Problem with possible translations - TODO: Search general solution
        self.driver.find_element(By.XPATH, "//button[text()='Permitir solo cookies necesarias']").click()
        username=self.driver.find_element(By.CSS_SELECTOR, "input[name='username']")
        password=self.driver.find_element(By.CSS_SELECTOR, "input[name='password']")
        username.clear()
        password.clear()
        print("Enter your username")
        username.send_keys(self.email)
        print("Enter your password")
        passwordInput = input()
        password.send_keys(passwordInput)
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        # wait for login success
        time.sleep(3)
        self.driver.find_element(By.XPATH, "//button[contains(text(),'Ahora no')]").click()
        time.sleep(1)
        self.driver.find_element(By.XPATH,"//button[contains(text(),'Ahora no')]").click()

    def close(self):
        self.driver.close()