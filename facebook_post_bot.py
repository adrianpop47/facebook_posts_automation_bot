import os

from selenium import webdriver
from selenium.common import NoSuchElementException, TimeoutException, UnexpectedAlertPresentException, \
    ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import wait
from selenium.webdriver.chrome.options import Options
import time

from logger import Logger

logging = Logger()


class FacebookPostBot:
    def __init__(self, driver_path, email, password, _groups):
        self.driver_path = driver_path
        self.driver = self.init_driver()
        self.email = email
        self.password = password
        self.groups = _groups
        self.new_facebook_interface = True

    def init_driver(self):
        logging.info("Initializing Bot...")
        options = Options()
        options.add_argument("--disable-infobars")
        options.add_argument("start-maximized")
        options.add_argument("--disable-extensions")
        options.add_experimental_option("prefs", {
            "profile.default_content_setting_values.notifications": 2
        })
        return webdriver.Chrome(chrome_options=options, executable_path=self.driver_path)

    def allow_cookies(self):
        logging.info("Allow cookies...")
        self.driver.find_element(By.XPATH, "/html/body/div[3]/div[2]/div/div/div/div/div[3]/button[2]").click()

    def login(self, email, password):
        logging.info("Login...")
        email_textbox = self.driver.find_element(By.ID, "email")
        email_textbox.send_keys(email)
        password_textbox = self.driver.find_element(By.ID, "pass")
        password_textbox.send_keys(password)
        self.driver.find_element(By.XPATH,
                                 "/html/body/div[1]/div[1]/div[1]/div/div/div/div[2]/div/div[1]/form/div[2]/button") \
            .click()

    def find_facebook_interface(self):
        logging.info("Finding Facebook Interface...")
        try:
            self.wait_login_new()
            self.new_facebook_interface = True
            logging.info("New Facebook interface")
            return
        except (NoSuchElementException, TimeoutException):
            logging.info("Not new Facebook interface")
        try:
            self.wait_login_old()
            self.new_facebook_interface = False
            logging.info("Old Facebook interface")
            return
        except (NoSuchElementException, TimeoutException):
            logging.info("Not old Facebook interface")

    def wait_login_new(self):
        wait.WebDriverWait(self.driver, 20).until(lambda x: x.find_element(By.XPATH, "/html/body/div[1]/div/div["
                                                                                     "1]/div/div[1]/div[1]/div/div["
                                                                                     "2]/div/div/div[2]/span"))

    def wait_login_old(self):
            wait.WebDriverWait(self.driver, 20).until(lambda x: x.find_element(By.XPATH,
                                                                           "/html/body/div[1]/div/div[1]/div/div["
                                                                           "2]/div[3]/div/div[1]/div[1]/ul/li["
                                                                           "2]/span/div/a"))

    def post_on_all_groups(self, change_identity, message, attempts):
        logging.info("Posting message {} on {} groups".format(message, len(self.groups)))
        for index, group in enumerate(self.groups):
            logging.info("{}. {}".format(index, group))
            posted = False
            retry_attempts = attempts
            while not posted and retry_attempts > 0:
                self.driver.get(group)
                try:
                    if change_identity:
                        self.change_post_identity()
                    if self.new_facebook_interface:
                        self.post_on_group_new(message)
                    else:
                        self.post_on_group_old(message)
                    logging.info("Posted with success")
                    posted = True
                except (NoSuchElementException, TimeoutException, UnexpectedAlertPresentException, ElementClickInterceptedException):
                    retry_attempts -= 1
                    logging.info("Retrying. {} attempts left".format(retry_attempts))
            if not posted and retry_attempts == 0:
                logging.info("Failed to post")
                logging.info("Skipping group...")
            time.sleep(5)


    def post_on_group_old(self, message):
        # Click post button
        wait.WebDriverWait(self.driver, 20).until(
            lambda x: x.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div["
                                               "4]/div/div/div/div/div/div[1]/div[1]/div/div/div/div[1]/div/div[1]"))
        self.driver.find_element(By.XPATH,
                                 "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div["
                                 "4]/div/div/div/div/div/div[1]/div[1]/div/div/div/div[1]/div/div[1]").click()

        # Find post textbox
        wait.WebDriverWait(self.driver, 20).until(lambda x: x.find_element(By.XPATH, "/html/body/div[1]/div/div["
                                                                                     "1]/div/div[4]/div/div/div["
                                                                                     "1]/div/div["
                                                                                     "2]/div/div/div/div/div["
                                                                                     "1]/form/div/div[1]/div/div/div["
                                                                                     "1]/div/div[2]/div[1]/div["
                                                                                     "1]/div[1]/div/div/div/div/div["
                                                                                     "2]/div"))
        post_texbox = self.driver.find_element(By.XPATH,
                                               "/html/body/div[1]/div/div["
                                               "1]/div/div[4]/div/div/div["
                                               "1]/div/div["
                                               "2]/div/div/div/div/div["
                                               "1]/form/div/div[1]/div/div/div["
                                               "1]/div/div[2]/div[1]/div["
                                               "1]/div[1]/div/div/div/div/div["
                                               "2]/div")
        post_texbox.send_keys(message)

        # Click the post button
        wait.WebDriverWait(self.driver, 20).until(lambda x: x.find_element(By.XPATH, "/html/body/div[1]/div/div["
                                                                                     "1]/div/div[4]/div/div/div["
                                                                                     "1]/div/div["
                                                                                     "2]/div/div/div/div/div["
                                                                                     "1]/form/div/div[1]/div/div/div["
                                                                                     "1]/div/div[3]/div[2]/div/div"))
        self.driver.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/div[4]/div/div/div[1]/div/div["
                                           "2]/div/div/div/div/div[1]/form/div/div[1]/div/div/div[1]/div/div[3]/div["
                                           "2]/div/div").click()
        # self.close_post_box()

    def close_post_box(self):
        wait.WebDriverWait(self.driver, 20).until(
            lambda x: x.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/div[4]/div/div/div[1]/div/div["
                                               "2]/div/div/div/div/div[1]/form/div/div[1]/div/div/div[1]/div/div["
                                               "1]/div[ "
                                               "1]/div[2]"))
        self.driver.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/div[4]/div/div/div[1]/div/div["
                                           "2]/div/div/div/div/div[1]/form/div/div[1]/div/div/div[1]/div/div[1]/div["
                                           "1]/div[2]").click()

    def post_on_group_new(self, message):
        wait.WebDriverWait(self.driver, 20).until(lambda x: x.find_element(By.XPATH, "/html/body/div[1]/div/div["
                                                                                     "1]/div/div[3]/div/div/div/div["
                                                                                     "1]/div[1]/div/div[ "
                                                                                     "2]/div/div/div["
                                                                                     "2]/div/div/div/div/div[1]/div["
                                                                                     "1]/div/div/div/div[1]/div"))
        self.driver.find_element(By.XPATH,
                                 "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div["
                                 "2]/div/div/div[2]/div/div/div/div/div[1]/div[1]/div/div/div/div[1]/div").click()
        wait.WebDriverWait(self.driver, 20).until(lambda x: x.find_element(By.XPATH, "/html/body/div[1]/div/div["
                                                                                     "1]/div/div[4]/div/div/div["
                                                                                     "1]/div/div["
                                                                                     "2]/div/div/div/div/div["
                                                                                     "1]/form/div/div[1]/div/div/div["
                                                                                     "1]/div/div[2]/div[1]/div["
                                                                                     "1]/div[1]/div/div/div/div/div["
                                                                                     "2]/div/div/div/div"))
        post_textbox = self.driver.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/div[4]/div/div/div["
                                                          "1]/div/div[2]/div/div/div/div/div[1]/form/div/div["
                                                          "1]/div/div/div[1]/div/div[2]/div[1]/div[1]/div["
                                                          "1]/div/div/div/div/div[2]/div/div/div/div")
        post_textbox.send_keys(message)
        wait.WebDriverWait(self.driver, 20).until(lambda x: x.find_element(By.XPATH, "/html/body/div[1]/div/div["
                                                                                     "1]/div/div[4]/div/div/div["
                                                                                     "1]/div/div["
                                                                                     "2]/div/div/div/div/div["
                                                                                     "1]/form/div/div[1]/div/div/div["
                                                                                     "1]/div/div[3]/div[2]/div/div"))
        self.driver.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/div[4]/div/div/div[1]/div/div["
                                           "2]/div/div/div/div/div[1]/form/div/div[1]/div/div/div[1]/div/div[3]/div["
                                           "2]/div/div").click()
        # self.close_post_box()

    def change_post_identity(self):
        try:
            wait.WebDriverWait(self.driver, 10).until(lambda x: x.find_element(By.XPATH,
                                                                               "/html/body/div[1]/div/div[1]/div/div["
                                                                               "3]/div/div/div/div[1]/div[1]/div[ "
                                                                               "3]/div/div/div/div["
                                                                               "3]/div/span/div/div/div[1]"))
            self.driver.find_element(By.XPATH,
                                     "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div["
                                     "3]/div/div/div/div[3]/div/span/div/div/div[1]").click()
            wait.WebDriverWait(self.driver, 10).until(lambda x: x.find_element(By.XPATH,
                                                                               "/html/body/div[1]/div/div[1]/div/div["
                                                                               "3]/div/div/div/div[2]/div/div/div["
                                                                               "1]/div[ "
                                                                               "1]/div/div/div[1]/div/div/div/div["
                                                                               "1]/div[3]/div[2]/div[2]/div["
                                                                               "1]/div/span"))
            self.driver.find_element(By.XPATH,
                                     "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[2]/div/div/div[1]/div["
                                     "1]/div/div/div[1]/div/div/div/div[1]/div[3]/div[2]/div[2]/div[1]/div/span").click()
        except (NoSuchElementException, UnexpectedAlertPresentException):
            logging.info("We can't change your identity")
            logging.info("Trying again to close post box")
            self.close_post_box()

    def start_bot(self, change_identity, message, retry_attempts):
        logging.info("Starting Bot...")
        self.driver.get("https://www.facebook.com/")
        self.allow_cookies()
        self.login(self.email, self.password)
        self.find_facebook_interface()
        if self.new_facebook_interface and change_identity:
            logging.info("Identity cannot be changed on new Facebook Interface")
            logging.info("Using default identity")
            change_identity = False
        if len(self.groups) != 0:
            self.post_on_all_groups(change_identity, message, retry_attempts)
        logging.info("Done")

