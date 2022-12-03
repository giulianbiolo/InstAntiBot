'''
InstAntiBot is a bot that automatically scrapes all the followers of a given account
and then labels them as Fake or Real with the help of a trained model.
Having done that you can also automatically remove the followers of the given account that have been labeled as Fake.
------
Usage:
------
python3 instantibot.py [-h | --help] [-f | --fetch ] [-s | --scrape] [-l | --label] [-r | --remove] [-a | --account [ACCOUNT_NAME]]

You can either pass the username and password arguments like this:
python3 instantibot.py -s -l -r -a account -u username -p password
Or you can use the .env file to store your credentials like this:
.env:
USERNAME=username
PASSWORD=password
ACCOUNT=account_name
------
'''

import os
import sys
from time import sleep as wait
from random import random as rand
from argparse import ArgumentParser, RawTextHelpFormatter
from dotenv import dotenv_values, find_dotenv
from igramscraper.instagram import Instagram
from instagrapi import Client


class ArgParser(ArgumentParser):
    '''This class is used to parse the arguments passed to the script.'''
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.description = (
            "InstantiBot is a bot that automatically scrapes all the followers of a given account\n"
            "and then labels them as Fake or Real with the help of a trained model.\n"
            "Having done that you can also automatically remove the followers of the given account that have been labeled as Fake.\n"
            "To define the account to be scraped you can either pass the username and password arguments or use the .env file to store your credentials."
        )
        self.add_argument('-f', '--fetch', action='store_true', help='Fetch the followers of the given account.')
        self.add_argument('-s', '--scrape', action='store_true', default=False, help='Scrape the followers of the given account.')
        self.add_argument('-l', '--label', action='store_true', default=False, help='Label the scraped followers.')
        self.add_argument('-r', '--remove', action='store_true', default=False, help='Remove the fake followers.')
        self.add_argument('-a', '--account', default='', help='The account to be scraped.')
        self.add_argument('-u', '--username', default='', help='The username of the account to scrape.')
        self.add_argument('-p', '--password', default='', help='The password of the account to scrape.')
    def error(self, message: str) -> None:
        sys.stderr.write(f'error: {message}\n')
        self.print_help()
        sys.exit(2)


class InstaScraper(Instagram):
    '''This class implements the fetching and scraping of all followers mechanics.'''
    def __init__(self, usr: str, psw: str, acc: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        print(f'Logging in as {usr}.')
        self.with_credentials(usr, psw)
        self.login()
        print('Logged in.')
        print(f'Loading {acc}...')
        self.account = self.get_account(acc)
        print('Account loaded.')

    def __scrapeacc__(self, username: str) -> list[str]:
        '''This is the private method that implements the logic of scraping a single account.'''
        features = []
        acc_to_scrape = self.get_account(username=username)
        # Profile Pic (44884218_345707102882519_2446069589734326272_n.jpg è l'immagine di default)
        pic_url = acc_to_scrape.get_profile_picture_url()
        if "44884218_345707102882519_2446069589734326272_n.jpg" in pic_url:
            features.append('0')
        else:
            features.append('1')
        # Nums / Length Username
        count: int = len([char for char in str(acc_to_scrape.username) if char.isnumeric()])
        if len(acc_to_scrape.username) == 0 or count == 0:
            result: float = 0
        else:
            result: float = count / len(acc_to_scrape.username)
        features.append(str(round(result, 3)))
        # Full Name Words
        result = len(acc_to_scrape.full_name.split())
        features.append(str(result))
        # Nums / Length Full Name
        count: int = len([char for char in str(acc_to_scrape.full_name) if char.isnumeric()])
        if len(acc_to_scrape.full_name) == 0 or count == 0:
            result: float = 0
        else:
            result: float = count / len(acc_to_scrape.full_name)
        features.append(str(round(result,3)))
        # Name == Username
        if acc_to_scrape.full_name == acc_to_scrape.username:
            features.append('1')
        else:
            features.append('0')
        # Bio Length
        features.append(str(len(acc_to_scrape.biography)))
        # External URL
        if acc_to_scrape.external_url is None:
            features.append('0')
        else:
            features.append('1')
        # Private
        if not acc_to_scrape.is_private:
            features.append('0')
        else:
            features.append('1')
        # Post
        features.append(str(acc_to_scrape.media_count))
        # Followers
        features.append(str(acc_to_scrape.followed_by_count))
        # Following
        features.append(str(acc_to_scrape.follows_count))
        return features

    def fetch(self) -> None:
        '''This method fetches all the followers of the given account.'''
        print('Initializing fetching...')
        followers = self.get_followers(self.account.identifier, self.account.followed_by_count, 50)
        print('Fetching completed!')
        print(f"Found {str(len(followers['accounts']))} followers.")
        with open('fetched.txt', 'w', encoding='utf-8') as file:
            for follower in followers['accounts']:
                file.write(follower.username + '\n')
        print('Saved all followers successfully!')


    def scrape(self) -> None:
        '''This method scrapes all the followers of the given account.'''
        if not os.path.exists('fetched.txt'):
            print("Couldn't find fetched.txt file...\nYou must fetch the followers first!")
            sys.exit(1)
        print('Initializing scraping...')
        with open('fetched.txt', 'r', encoding='utf-8') as file:
            usernames = [line.strip() for line in file if line != '\n']
        for nuser, username in enumerate(usernames):
            print(f"Scraping {str(nuser + 1)} di {str(len(usernames))} : {username}")
            features: list[str] = self.__scrapeacc__(username)
            with open('scraped.txt', 'a', encoding='utf-8') as file:
                file.write(f"{username}|{','.join(features)}\n")
            if nuser % 10 == 0 and nuser != 0:
                wait(300 + rand() * 300) # [300 - 600] seconds
            else:
                wait(25.0 + rand() * 10.0) # [25 - 35] seconds
        print('Scraping completed!')


def load_credentials(args, parser) -> tuple[str, str]:
    '''This method loads credentials when needed.'''
    if args.username != '' and args.password != '':
        return args.username, args.password
    if os.path.exists(find_dotenv()):
        config = dotenv_values()
        return config.get('USERNAME'), config.get('PASSWORD')
    parser.error('You must pass the username and password arguments or use the .env file to store your credentials')
    return None, None

def load_account(args, parser) -> str:
    '''This method loads the account to be scraped.'''
    if args.account != '':
        return args.account
    if os.path.exists(find_dotenv()):
        config = dotenv_values()
        return config.get('ACCOUNT')
    parser.error('You must pass the account argument or use the .env file to store your account')
    return None

def is_bot(features: list) -> bool:
    '''This method labels the features of a single account.'''
    followers = features[-1]
    followedby = features[-2]
    if followers <= followedby:
        return False
    ratio: float = followers / followedby
    if ratio > 3.0 and followers > 1000:
        return True
    return False

def label_accounts() -> None:
    '''This method labels the scraped accounts as Real of Fake.'''
    if not os.path.exists('scraped.txt'):
        print("Couldn't find scraped.txt file...\nYou must scrape the accounts first!")
        sys.exit(1)
    print('Initializing labeling...')
    with open('scraped.txt', 'r', encoding='utf-8') as file:
        scraped_accounts = [line.strip() for line in file if line != '\n']
    with open('labeled.txt', 'w', encoding='utf-8') as file:
        for scrapedacc in scraped_accounts:
            username, features = scrapedacc.split('|')
            features = features.split(',')
            for idx, feature in enumerate(features):
                if '.' in feature:
                    features[idx] = float(feature)
                else:
                    features[idx] = int(feature)
            # Now we have the parsed features and we can label the account
            if is_bot(features):
                print(f'{username} is a fake account!')
                file.write(f"{username}|1\n")
            else:
                print(f'{username} is a real account!')
                file.write(f"{username}|0\n")
    print('Labeling completed!')

def remove_fake_accounts(client: Client) -> None:
    '''This method removes the fake followers of the given account.'''
    if not os.path.exists('labeled.txt'):
        print("Couldn't find labeled.txt file...\nYou must label the scraped followers first!")
        sys.exit(1)
    print('Initializing removing...')
    with open('labeled.txt', 'r', encoding='utf-8') as file:
        labeled_accounts = [line.strip() for line in file if line != '\n']
    fakeaccs = [acc.split('|')[0] for acc in labeled_accounts if acc.split('|')[1] == '1']
    for nlabeled, username in enumerate(fakeaccs):
        try:
            client.user_remove_follower(client.user_id_from_username(username))
            print(f"Removed: {username} | {str(nlabeled + 1)} di {str(len(fakeaccs))}")
        except:
            print(f"Couldn't remove: {username} | {str(nlabeled + 1)} di {str(len(fakeaccs))}")
    print('Removing completed!')

def instantibot() -> None:
    '''This is the main method of the program, here we parse the arguments and call the methods.'''
    parser = ArgParser(formatter_class=RawTextHelpFormatter)
    args = parser.parse_args()
    scraper: InstaScraper = None
    usr, psw = load_credentials(args, parser)
    acc = load_account(args, parser)
    if usr is None or psw is None or acc is None:
        sys.exit("Error loading credentials and account!")
    if not args.fetch and not args.scrape and not args.label and not args.remove:
        parser.error('You must pass at least one of the following arguments: fetch, scrape, label, remove')
        sys.exit(0)
    if args.fetch:
        scraper = InstaScraper(usr, psw, acc)
        scraper.fetch()
    if args.scrape:
        if scraper is None:
            scraper = InstaScraper(usr, psw, acc)
        scraper.scrape()
    if args.label:
        label_accounts()
    if args.remove:
        client: Client = Client()
        client.login(usr, psw)
        remove_fake_accounts(client)


if __name__ == '__main__':
    instantibot()
