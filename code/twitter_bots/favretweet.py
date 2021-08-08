#!/usr/bin/env python3

# tweepy-bots/bots/favretweet.py

"""The Fav & Retweet Bot
This bot uses the previously introduced Tweepy stream to 
actively watch for tweets that contain certain keywords. 
For each tweet, if you’re not the tweet author, 
it will mark the tweet as Liked and then retweet it.
You can use this bot to feed your account with content 
that is relevant to your interests."""

import tweepy
import logging
from config import create_api
import json
import os


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


class FavRetweetListener(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api
        self.me = api.me()
        print("starting to listen...")

    def on_status(self, tweet):
        logger.info(f"Processing tweet id {tweet.id}")
        if tweet.in_reply_to_status_id is not None or \
            tweet.user.id == self.me.id:
            # This tweet is a reply or I'm its author so, ignore it
            return
        
        
        #TO BE IMPLEMENTED
        #if tweet is actually a retweet, ignore it
        #if tweet.
        
        
        
            
        #if not tweet.favorited:
        #    # Mark it as Liked, since we have not done it yet
        #    try:
        #        tweet.favorite()
        #    except Exception as e:
        #        logger.error("Error on fav", exc_info=True)
        if not tweet.retweeted:
            # Retweet, since we have not retweeted it yet
            try:
                tweet.retweet()
            except Exception as e:
                logger.error("Error on fav and retweet", exc_info=True)

    def on_error(self, status):
        logger.error(status)

def main(keywords):
    api = create_api()
    tweets_listener = FavRetweetListener(api)
    stream = tweepy.Stream(api.auth, tweets_listener)
    stream.filter(track=keywords, languages=["en"])

if __name__ == "__main__":
    main(["openneurosci", "openneuroscience",
		  "openbehavior","opensciencehardware",
		  "opensciencesoftware","LabOnTheCheap",
		  "openbehaviour","OpenBehavior",
          "openephys","BackyardBrains",
		  "openfmri","openeuroscience","WINRePo1",
		  "openneuro","openmicroscopy","BlackInNeuro",
		  "DeeplabCut","opentrons",#"theBossDB",
		  "worldwideneuro","biorxiv_neursci"])
    #os.execv(__file__)
