import argparse
import errno
import json
import os
import requests
import shutil
import sys
import time

import pandas as pd

from tqdm import tqdm

def _username2url(name):
    return "https://twitter.com/{}/profile_image?size=original".format(name)

def _mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

def _save_image(url, path):
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(path, "wb") as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Download twitter profile pictures.')
    parser.add_argument('path', metavar='PATH', type=str, nargs='+',
                        help='path to csv data')

    args = parser.parse_args()
    path = args.path[0]

    data_name = path.split("/")[-1].split(".")[0]

    current_data = pd.read_csv(path, dtype='str,str', delimiter=";", names=["username", "duplicate_candidates"])
    
    duplicate_candidates = {}
    # print(current_data.duplicate_candidates)
    for _, row in current_data.iterrows():
        # skip usernames with no duplicates
        if type(row["duplicate_candidates"]) != str:
            continue
        duplicate_candidates[row["username"]] = row["duplicate_candidates"].split(",")

    if not os.path.isdir(data_name):
        _mkdir_p(data_name)

    for candidate in tqdm(duplicate_candidates):
        path = "{}/{}".format(data_name, candidate)
        
        # skip if pictures have already been loaded
        if os.path.isdir(path):
            continue

        # create folder with candidate name
        _mkdir_p(path)
        _save_image(_username2url(candidate), "{}/{}/{}.jpg".format(data_name, candidate, candidate))
        # download [candidate name]/[candidate name].jpg
        for comparison in duplicate_candidates[candidate]:
            # download [candidate name]/[comparison name].jpg
            _save_image(_username2url(comparison), "{}/{}/{}.jpg".format(data_name, candidate, comparison))
            time.sleep(0.1)