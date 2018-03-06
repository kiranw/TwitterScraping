import os
import json

# For each twitter stream result, isolate the username and link to image
for filename in os.listdir("hashtag_results"):
     fn = filename[:-5]
     # Map users to username, image link, associated hashtag
     all_users = []
     with open("hashtag_results/%s.json"%fn,"r") as src, open("user_results/%s.json"%fn, "a") as f, open("user_results/users_%s.json"%fn, "a") as u:
         for line in src:
            tweet = json.loads(line)
            output = {}
            output["user"] = tweet["user"]["screen_name"]
            output["user_id"] = tweet["user"]["id"]
            output["image_link"] = tweet["user"]["profile_image_url"]
            output["name"] = tweet["user"]["name"]
            output["description"] = tweet["user"]["description"]
            output["verified"] = tweet["user"]["verified"]
            output["followers_count"] = tweet["user"]["followers_count"]
            output["friends_count"] = tweet["user"]["friends_count"]
            output["listed_count"] = tweet["user"]["listed_count"]
            output["favourites_count"] = tweet["user"]["favourites_count"]
            output["statuses_count"] = tweet["user"]["statuses_count"]
            output["created_at"] = tweet["user"]["created_at"]
            f.write(json.dumps(output))
            all_users.append(tweet["user"]["screen_name"])
         u.write(json.dumps(all_users))