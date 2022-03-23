import random


# Read users data from file
def get_users_data() -> list[tuple]:
    users_asset = []
    with open("Data/accounts_data.txt", mode="r") as file:
        for line in file:
            user = line.split(":")
            users_asset.append((user[0], user[1]))

    return users_asset


# Read target urls from file
def get_target_data(filename: str) -> list[str]:
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


class OperationalData:

    # Read accounts & targets data from files
    def __init__(self, account_segment=75, upvote_segment=75, downvote_segment=75):

        self.account_segment = account_segment
        self.upvote_segment = upvote_segment
        self.downvote_segment = downvote_segment

        self.user_accounts = get_users_data()
        self.web_pages_to_upvote = get_target_data("Data/targets_to_upvote.txt")
        self.web_pages_to_downvote = get_target_data("Data/targets_to_downvote.txt")

    # Masking suspicious activity by shuffling accounts and using parts of them
    def shuffle_accounts(self) -> list[tuple]:

        shuffled_accounts = randomize_data(self.user_accounts, self.account_segment)

        return shuffled_accounts

    # Masking suspicious activity by mixing targets and using parts of them at a time
    def shuffle_targets(self) -> list:

        shuffled_list_to_upvote = randomize_data(self.web_pages_to_upvote, self.upvote_segment)
        target_list_up = [("up", web_page) for web_page in shuffled_list_to_upvote]

        shuffled_list_to_downvote = randomize_data(self.web_pages_to_downvote, self.downvote_segment)
        target_list_dn = [("dn", web_page) for web_page in shuffled_list_to_downvote]

        target_list = target_list_up + target_list_dn
        random.shuffle(target_list)

        return target_list
