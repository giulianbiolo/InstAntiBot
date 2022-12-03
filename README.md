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

I've decided to comment out my fix in the requirements.txt file, so if you're reading this then probably the pip package is still broken and all you have to do to fix your problem is commenting out the line in requirements.txt containing `igramscraper` and uncommenting the last line containing `.\igramscrapersrc\`

If even this doesn't work for you, then I probably messed something up with the src folder of igramscraper (sry) the only way for you to fix this is by downloading the whl file of igramscraper from the internet and building it yourself. Good luck.  
