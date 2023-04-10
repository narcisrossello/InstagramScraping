import numpy as np

from InstagramScrapingClass import InstagramScrapingClass

base_url = "https://www.instagram.com"


def non_mutual_followers(followers: list, following: list):
    non_mutual = np.setdiff1d(following, followers)
    print("Following without follow: ", non_mutual)


def main_function():
    print("START EXECUTION")
    followers = []
    following = []
    n_followers = 384
    n_followed = 414
    print("Enter your email: ")
    email = input()
    print("Enter your profile: ")
    profile = input()
    scraper = InstagramScrapingClass(base_url, profile, email)
    scraper.login()
    while 1:
        print("Choose option: ")
        option = input()
        if option == "0":
            followers = scraper.get_users(0)[:n_followers]
            print("Followers users: ", len(followers))
            continue
        if option == "1":
            following = scraper.get_users(1)[:n_followed]
            print("Following users: ", len(following))
            continue
        if option == "2":
            non_mutual_followers(followers, following)
            continue
        if option == "3":
            scraper.close()
            break
    print("END EXECUTION")


if __name__ == "__main__":
    main_function()
