from twitter_stream_download import run
import os
import json

# Get a list of hashtags to search from the dashboard
url = "https://dashboard.securingdemocracy.org/"
# Content is generated in JavaScript, these are hashtags as of March 5, 6:45
# top_hashtags = ["syria","ghouta","maga","russia","whitehelmets","qanon","eastghouta","us","damascus"]
top_hashtags = ["ghouta","maga","russia","whitehelmets","qanon","eastghouta","us","damascus"]
trending_hashtags = ["nieuwsofnonsens","america","monday","toriesinsixwords","mondaymotivation","trumpttheestablishment","speak"]

# Feed the hashtags to twitter_stream_download to get the usernames associated with tweets and their image URLs
for hashtag in top_hashtags:
	run(hashtag)

for hashtag in trending_hashtags:
	run(hashtag)

# For each twitter stream result, isolate the username and link to image
for filename in os.listdir("hashtag_results"):
     # Map users to username, image link, associated hashtag
     with open("hashtag_results/%s"%filename,"r") as src, open("user_results/%s.json"%filename, "a") as f:
	     for line in src:
	     	tweet = json.loads(line)
	     	output = {}
	     	output[user] = tweet["user"]["screen_name"]
	     	output[user_id] = tweet["user"]["id"]
	     	output[image_link] = tweet["user"]["profile_image_url"]
	     	output[name] = tweet["user"]["name"]
	     	output[description] = tweet["user"]["description"]
			output[verified] = tweet["user"]["verified"]
			output[followers_count] = tweet["user"]["followers_count"]
			output[friends_count] = tweet["user"]["friends_count"]
			output[listed_count] = tweet["user"]["listed_count"]
			output[favourites_count] = tweet["user"]["favourites_count"]
			output[statuses_count] = tweet["user"]["statuses_count"]
			output[created_at] = tweet["user"]["created_at"]
			f.write(json.dumps(output))


users = []
for filename in os.listdir("user_results"):
     # Map users to username, image link, associated hashtag
     with open("user_results/%s.json"%filename, "a") as f:
	     for line in f:
	     	tweet = json.loads(line)
	     	users.add(tweet["user"])