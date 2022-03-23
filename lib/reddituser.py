import dotenv
import os
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


# Environment variables
dotenv.load_dotenv()
chrome_driver_path = os.getenv("CHROME_DRIVER_PATH")

REDDIT_URL = "https://www.reddit.com/"


class RedditUser:

    def __init__(self, name, password):

        option = Options()
        option.add_argument("--disable-infobars")
        option.add_argument("start-maximized")
        option.add_argument("--disable-extensions")

        # Pass the argument 1 to allow and 2 to block
        option.add_experimental_option("prefs",
                                       {"profile.default_content_setting_values.notifications": 1}
                                       )

        self.driver = webdriver.Chrome(options=option, service=Service(chrome_driver_path))
        self.name = name
        self.password = password

    # open Reddit web page, click 'login button', enter user data & login
    def login(self) -> None:

        self.driver.get(REDDIT_URL)
        sleep(1)

        login_button = self.driver.find_element(by=By.XPATH,
                                                value="/html/body/div[1]/div/div[2]/div[1]/header/div/div[2]/div/div[1]/a[1]"
                                                )
        login_button.click()
        sleep(2)

        new_target = self.driver.find_element(by=By.TAG_NAME, value="iframe")
        self.driver.switch_to.frame(new_target)

        login_name_input = self.driver.find_element(by=By.ID, value="loginUsername")
        login_pass_input = self.driver.find_element(by=By.ID, value="loginPassword")

        login_name_input.send_keys(self.name)
        login_pass_input.send_keys(self.password)
        login_pass_input.send_keys(Keys.ENTER)
        sleep(4)
        return

    # just press the damn button )))
    def vote_webpage(self, target) -> int:

        action, url = target[0], target[1]

        self.driver.get(url)
        sleep(1)

        try:
            if action == "up":
                target_button = self.driver.find_element(by=By.CSS_SELECTOR,
                                                         value="button[aria-label='upvote'][aria-pressed='false']"
                                                         )
            elif action == "dn":
                target_button = self.driver.find_element(by=By.CSS_SELECTOR,
                                                         value="button[aria-label='downvote'][aria-pressed='false']"
                                                         )
            else:
                return False

            target_button.click()

        except Exception:
            print(f"Something went wrong! Error:{Exception}")
            return False

        return True
