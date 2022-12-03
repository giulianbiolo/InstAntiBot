# InstAntiBot
A bot scraper that removes bots from following you on Instagram

# Usage
You have to create a .env file containing the credentials of the account you want to clean from bots with the following format:
```
USERNAME = 'YOUR EMAIL'
PASSWORD = 'YOUR PASSWORD'
ACCOUNT = 'YOUR USERNAME'
```
Then all you have to do is create a python virtual environment and install all the requirements with:
```
pip install -r requirements.txt
```
Then you can start the bot by sending the command:
```
python instantibot.py --help
```
Read through the instructions and use as you please.

# Troubleshooting
You might have to tweak the requirements.txt file to install the **igramscraper** dependency.
While I'm writing this, the pip package is broken, so I had to build it myself, if you are fortunate however `pip install igramscraper` might just work for you.
If that's the case then cool, just remove all the dependencies in the requirements.txt file under the comment `igramscraper==0.3.5 dependencies` and instead add a line with `igramscraper` and redo the  `pip install -r requirements.txt` command. Everything should work right away.  

I decided to let the dependencies for building the package in the requirements.txt so it should build it for you and it should all work as expected.
If that's not the case however, all you have to do is build it from source yourself. Search the internet for the `.whl` file and install it in the python virtual environment. Good Luck.  
