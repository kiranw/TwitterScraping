import json
import requests
import sys
import time
import urllib.request

import pandas as pd

from selenium import webdriver
from tqdm import tqdm

# Find twitter urls and extract usernames

# create reverse image search URL for a given results page
def _construct_search_url(image_url, page):
    s = "http://images.google.com/searchbyimage?site=search&oq=site%3Atwitter.com&q=site%3Atwitter.com"
    s += "&image_url={}".format(image_url)
    s += "&start={}".format(10 * page)
    return s

# create the profile picture user URL
def _username2url(name):
    return "https://twitter.com/{}/profile_image?size=original".format(name)

# save the crawled potential duplicate twitter accounts to disk
# format: username;fake_1,...,fake_n
def _logDuplicates(username, duplicates):
    with open("data.csv", "a") as f:
        s = username + ";"
        for duplicate in duplicates:
            s += duplicate + ","
        s = s[:-1]
        s += "\n"
        f.write(s)

# crawl google reverse image search for the supplied Twitter usernames
# returns a dictionary mapping one username to a set of potential other usernames
def _crawl_users(usernames, max_no_pages=3, request_pause=0.5):
    # selenium driver
    parser = webdriver.Firefox()

    for username in tqdm(usernames):
        duplicate_candidates = set()

        # iterate over all desired google result pages
        for i in range(max_no_pages):
            google_url = _construct_search_url(_username2url(username), i)
            parser.get(google_url)

            results = parser.find_elements_by_class_name("_Rm")
            for result in results:
                url = result.get_attribute("innerHTML")
                if url[:20] == "https://twitter.com/":
                    end = url[20:].find("/")
                    if end == -1:
                        duplicate_user = url[20:]
                    else:
                        duplicate_user = url[20:20+end]
                    
                duplicate_candidates.update([duplicate_user.lower()])
            time.sleep(request_pause)

            # only try to visit as many results pages as available
            nextPage = len(parser.find_elements_by_id("pnnext")) != 0
            if not nextPage:
                break

        _logDuplicates(username, list(duplicate_candidates))

    parser.close()


if __name__ == "__main__":
    # the user handles to be reverse-image-searched
    usernames = ["realdonaldtrump", "lvnancy", "jangeffert"]

    open("data.csv", "a").close()
    # make sure we are not crawling for already saved user names
    current_data = pd.read_csv("data.csv", delimiter=";", names=["username", "duplicate_candidates"])
    cached_usernames = set(current_data["username"].tolist())
    usernames = list(set(usernames) - cached_usernames)

    data = _crawl_users(usernames)