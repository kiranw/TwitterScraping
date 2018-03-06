import os
import re
import subprocess
from struct import *

if __name__ == "__main__":

    results = {}
    # go into data directory
    usernames = list(set(os.listdir("testdata")).difference([".DS_Store"]))
    for username in usernames:
        # call findimagedupes
        p = subprocess.Popen('cd testdata/{}; /Users/jan/go/bin/findimagedupes . > duplicates.txt'.format(username), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        retval = p.wait()

        results[username] = []
        with open("testdata/{}/duplicates.txt".format(username)) as f:
            for line in f:
                results[username].append([elem.strip() for elem in line.rstrip().split(".jpg")[:-1]])

    for user in results:
        for equivalence_class in results[user]:
            print(equivalence_class)
            p = subprocess.Popen('open testdata/{}/{}.jpg'.format(user, equivalence_class[0]), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            retval = p.wait()
            show_accounts = input("Press Enter to continue or 'y' to display the relvant accounts...")
            if show_accounts.rstrip() == "y":
                url_string = "open"
                for acc in equivalence_class:
                    url_string += " https://twitter.com/{}".format(acc)
                print(url_string)
                p = subprocess.Popen(url_string, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                retval = p.wait()
