General Design
------------------------------

config.py - Twitter Access Keys (not published on Github)
hashtags_to_users.py - Submits queries to Twitter to get realtime tweets on the platform, and stores 1000 of the most recent tweets per hashtags in hashtag_results/*
tweets_to_users.py - Maps the results of hashtag_results/* into users with relevant information, both as a user list and a comprehensive user dicitonary list
web_scraper.rb - Takes a list of usernames and gets reverse image results on profile images