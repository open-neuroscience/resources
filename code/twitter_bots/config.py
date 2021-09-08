# tweepy-bots/bots/config.py
import tweepy
import logging
import os

logger = logging.getLogger()



def create_api():

    secrets = open("bot_api","r")
    consumer_key = secrets.readline()
    consumer_key = consumer_key[1:consumer_key[1:].find('\"')+1]
    consumer_secret = secrets.readline()
    consumer_secret = consumer_secret[1:consumer_secret[1:].find('\"')+1]
    access_token = secrets.readline()
    access_token = access_token[1:access_token[1:].find('\"')+1]

    access_token_secret = secrets.readline()
    access_token_secret = access_token_secret[1:access_token_secret[1:].find('\"')+1]

    secrets.close()

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, 
        wait_on_rate_limit_notify=True)
    try:
        api.verify_credentials()
    except Exception as e:
        logger.error("Error creating API", exc_info=True)
        raise e
    logger.info("API created")
    return api
