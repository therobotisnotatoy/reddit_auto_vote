Copyrights. The author of this product is Volodmyr Keretiv (vvkeretiv@gmail.com).
For detailed information, please see disclamer.html

The program was written and tested in the MacOS 12.0.1 operating system to work with the Google Chrome browser.

Before using the program you need:
1. Download the chromedriver (https://chromedriver.chromium.org/downloads) that matches your browser version. Warning, the latest version may be incompatible with your browser. Make sure you make the right choice.
2. Unzip the downloaded file (to any directory).
3. Specify the full path to the chromedriver in the ".env" file. For example:
export CHROME_DRIVER_PATH=/Users/your_username/Desktop/Anu_directory/chromedriver

What the program does:
- Votes for or against some material on reddit platform.
- The program can use the data of one account or several. To do this, simply place the appropriate rows of data in the file "Data / accounts_data.txt".
- The program votes positively for materials whose urls are placed in the file "Data / targets_to_upvote.txt".
- The program votes negatively for materials whose urls are placed in "Data / targets_to_downvote.txt"
- Each of the files "Data / accounts_data.txt" and "Data / targets_to_downvote.txt" can contain any number of urls, or be empty. Their data is mixed and used as a whole.
- The program can be runned with additional 3 command line arguments.

What the program does not do:
- The program will not be able to vote immediately. Different user logins and opening web pages for voting require time delays between actions.
- This program will not be able to vote without user data, somehow choose a login or password, or create one or more new users.
- The program cannot independently decide which materials to vote for. The user must fill in the relevant data files himself.

Command line arguments:
All arguments are integers and are responsible for the percentage use of the corresponding data files.
The first argument is responsible for the percentage of accounts used during a particular program launch. At each program run, they are mixed and limited by this parameter.
The following argument limits the percentage of web pages you want to upvote located in the file "Data/targets_to_upvote.txt".
The last argument limits the percentage of web pages you want to downvote located in the file "Data/targets_to_downvote".
The program will also work without specifying arguments. All three default settings are set to 75.

For example:
python3 reddit_auto_vote.py 30 55 70
- Mixes users, selects only 30% of them. For each selected user randomly selects 55% of web pages to raise and 70% of web pages to lower and shuffles them. Then the main algorithm of the program is launched, which gives the appropriate votes.

python3 reddit_auto_vote.py 100 90
- Uses all 100%. For each user randomly selects 90% of web pages to raise and 75% of web pages to lower and shuffles them. Then the main algorithm of the program is launched, which gives the appropriate votes.

python3 reddit_auto_vote.py 20
- Mixes users, selects only 20% of them. For each selected user randomly selects 75% of web pages to raise and 75% of web pages to lower and shuffles them. Then the main algorithm of the program is launched, which gives the appropriate votes.






