import sys
from lib.operationaldata import OperationalData
from lib.reddituser import RedditUser


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

        reddit = RedditUser(*account)

        # For every user get new web page samples
        webpages = od.shuffle_targets()
        success_up_counter, success_down_counter = 0, 0
        user_name = account[0]

        try:
            reddit.login()

        except Exception:
            print(f"Can not login user:{user_name} Error: {Exception}")
            break

        try:
            for webpage in webpages:
                if reddit.vote_webpage(webpage):
                    if webpage[0] == "up":
                        success_up_counter += 1
                    else:
                        success_down_counter += 1

            account_success_counter = success_up_counter + success_down_counter
            print(f"User: {user_name} upvote: {success_up_counter}, "
                  f"downvote: {success_down_counter}, successful attempts: {account_success_counter}"
                  f" (max={len(webpages)})")
            total_success_counter += account_success_counter

        except Exception:
            print(f"User: {user_name} failed! {Exception}")

    print(f"Total votes: {total_success_counter}")

    return


if __name__ == "__main__":

    main()
