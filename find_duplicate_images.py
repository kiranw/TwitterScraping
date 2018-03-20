import argparse
import face_recognition
import os
import re
import subprocess

from struct import *
from tqdm import tqdm

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Find duplicate twitter handles.')
    parser.add_argument('path', metavar='PATH', type=str, nargs='+',
                        help='name of data folder')
    parser.add_argument('--faces', action='store_true', help='only show profile pictures with faces')

    args = parser.parse_args()
    path = args.path[0]

    print("Analyzing data...")

    results = {}
    # go into data directory
    usernames = list(set(os.listdir(path)).difference([".DS_Store"]))
    for username in tqdm(usernames):
        # call findimagedupes

        p = subprocess.Popen('cp default_profile.jpg {}/{}/.'.format(path, username), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        retval = p.wait()

        p = subprocess.Popen('cp default_profile_2.jpg {}/{}/.'.format(path, username), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        retval = p.wait()

        p = subprocess.Popen('cd {}/{}; /Users/jan/go/bin/findimagedupes . > duplicates.txt'.format(path, username), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        retval = p.wait()

        results[username] = []
        with open("{}/{}/duplicates.txt".format(path, username)) as f:
            for line in f:
                results[username].append([elem.strip() for elem in line.rstrip().split(".jpg")[:-1]])

    print("Inspect duplicates")

    for user in tqdm(results):
        for equivalence_class in results[user]:
            if "default_profile" in equivalence_class or "default_profile_2" in equivalence_class:
                continue

            if args.faces:
                image = face_recognition.load_image_file("{}/{}/{}.jpg".format(path, user, equivalence_class[0]))
                # skip duplicates without faces
                if len(face_recognition.face_locations(image)) == 0:
                    continue

            print(equivalence_class)

            p = subprocess.Popen('open {}/{}/{}.jpg'.format(path, user, equivalence_class[0]), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            retval = p.wait()
            show_accounts = input("Press Enter to continue or 'y' to display the relevant accounts...")
            if show_accounts.rstrip() == "y":
                url_string = "open"
                for acc in equivalence_class:
                    url_string += " https://twitter.com/{}".format(acc)
                print(url_string)
                p = subprocess.Popen(url_string, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                retval = p.wait()
