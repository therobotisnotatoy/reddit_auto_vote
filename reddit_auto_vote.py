import sys, random, os
from time import sleep

import dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

# Enviornment variables
dotenv.load_dotenv()
chrome_driver_path = os.getenv("CHROME_DRIVER_PATH")

REDDIT_URL = "https://www.reddit.com/"


# Reddit user class
class RedditUser():

    def __init__(self, name, password):
        """Instance creation"""
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
            return True

        except Exception:
            # print("ERR:", Exception)
            return False


# Read users data from file
def get_users_data() -> list:
    users_asset = []
    with open("Data/accounts_data.txt", mode="r") as file:
        for line in file:
            user = line.split(":")
            users_asset.append((user[0], user[1]))

    return users_asset


# Read target urls from file
def get_target_data(filename: str) -> list:
    targets = []
    with open(filename, mode="r") as file:
        for line in file:
            targets.append(line)

    return targets


# Randomly shuffle ang cutoff part of data
def randomize_data(data: list, limit: int) -> list:
    random.shuffle(data)
    current_size = len(data)

    final_size = round(current_size * limit / 100)
    return data[:final_size]


# Class for storing and handling data
class OperationalData():

    # Read accounts & targets data from files
    def __init__(self, accoun_segment=75, upvoted_segment=75, downvoted_segment=75):

        self.accoun_segment = int(accoun_segment)
        self.upvoted_segment = int(upvoted_segment)
        self.downvoted_segment = int(downvoted_segment)

        self.user_accounts = get_users_data()
        self.web_pages_to_upvote = get_target_data("Data/targets_to_upvote.txt")
        self.web_pages_to_downvote = get_target_data("Data/targets_to_downvote.txt")

    # Masking suspicious activity by shuffling accounts and using parts of them
    def shuffle_accounts(self) -> list:

        shuffled_accounts = randomize_data(self.user_accounts, self.accoun_segment)

        return shuffled_accounts

    # Masking suspicious activity by mixing targets and using parts of them at a time
    def shuffle_targets(self) -> list:

        shuffled_list_to_upvote = randomize_data(self.web_pages_to_upvote, self.upvoted_segment)
        target_list_up = [("up", web_page) for web_page in shuffled_list_to_upvote]

        shuffled_list_to_downvote = randomize_data(self.web_pages_to_downvote, self.downvoted_segment)
        target_list_dn = [("dn", web_page) for web_page in shuffled_list_to_downvote]

        target_list = target_list_up + target_list_dn
        random.shuffle(target_list)

        return target_list


# The magic place
def main() -> None:

    # Getting console arguments
    args = [int(arg) for arg in sys.argv[1:] if (arg.isnumeric() and (int(arg) <= 100))]

    # Load all data from files
    od = OperationalData(*args)

    # Get part of shuffled accounts
    accounts_sample = od.shuffle_accounts()

    # Cycle through user accounts, try to login, then cycle through web pages and try to vote
    total_success_counter = 0

    for account in accounts_sample:

        reddit = RedditUser(account[0], account[1])

        # For every user get new web page samples
        webpages = od.shuffle_targets()
        success_up_counter, success_down_counter = 0, 0

        try:
            reddit.login()

        except Exception:
            print(f"Can not login user:{account[0]} Error: {Exception}")
            break

        try:
            for webpage in webpages:
                if reddit.vote_webpage(webpage):
                    if webpage[0] == "up":
                        success_up_counter += 1
                    else:
                        success_down_counter += 1

            account_success_counter = success_up_counter + success_down_counter
            print(f"User: {account[0]} upvote: {success_up_counter}, "
                  f"downvote: {success_down_counter}, successful attempts: {account_success_counter}"
                  f" (max={len(webpages)})")
            total_success_counter += account_success_counter

        except Exception:
            print(f"User: {account[0]} failed! {Exception}")

    print(f"Total upvotes: {total_success_counter}")

    return

if __name__ == "__main__":

    main()

