from InstagramScrapingClass import InstagramScrapingClass
import numpy as np

base_url = "https://www.instagram.com"

def nonMutualFollowers(followers, following):
    nonMutual = np.setdiff1d(following, followers)
    print("Following without follow: ", nonMutual)

if __name__ == "__main__":
    print("START EXECUTION")
    followers = []
    following = []
    print("Enter your email: ")
    email = input()
    print("Enter your profile: ")
    profile = input()
    scraper = InstagramScrapingClass(base_url, profile, email)
    scraper.login()
    while(1):
        print("Choose option: ")
        option = input()
        if option == '0':
            followers = scraper.getUsers(0)
            print("Followers users: ", len(followers))
        if option == '1':
            following = scraper.getUsers(1)
            print("Following users: ", len(following))
        if option == '2':
            nonMutualFollowers(followers, following)
        if option == '3':
            scraper.close()
            break
    print("END EXECUTION")
