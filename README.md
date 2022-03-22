Copyrights. The author of this product is Volodmyr Keretiv (vvkeretiv@gmail.com). 

For detailed information, please see disclamer.html

The program was written and tested in the MacOS 12.0.1 operating system to work with the Google Chrome browser.

Before using the program you need:
1. Download the chromedriver (https://chromedriver.chromium.org/downloads) that matches your browser version. Warning, the latest version may be incompatible with your browser. Make sure you make the right choice.
2. Unzip the downloaded file (to any directory).
3. Specify the full path to the chromedriver in the ".env" file. For example:
export CHROME_DRIVER_PATH=/Users/your_username/Desktop/Anu_directory/chromedriver

The program can be runned with 3 additional parameters. All parameters are set as a percentage (integer). 
The first parameter is responsible for the number of accounts used during a particular program launch. At each start, they are mixed and limited by this parameter.
The following parameter limits the percentage of web pages you want to upvote located in the file "targets_to_upvote.txt"
The last parameter limits the percentage of web pages you want to downvote located in the file "targets_to_downvote"
The program will also work without specifying parameters. Default settings: 75 75 75

For example:
python3 reddit_auto_vote.py 30 55 70
- Mixes users, selects only 30% of them. For each selected user randomly selects 55% of web pages to raise and 70% of web pages to lower and shuffles them. Then the main algorithm of the program is launched, which gives the appropriate votes.

python3 reddit_auto_vote.py 100 90
- Uses all 100%. For each user randomly selects 90% of web pages to raise and 75% of web pages to lower and shuffles them. Then the main algorithm of the program is launched, which gives the appropriate votes.

python3 reddit_auto_vote.py 20
- Mixes users, selects only 20% of them. For each selected user randomly selects 75% of web pages to raise and 75% of web pages to lower and shuffles them. Then the main algorithm of the program is launched, which gives the appropriate votes.






