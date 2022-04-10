import os
import tweepy
import logging
import azure.functions as func


def handle_twitter(query_result):
    """Returns the last tweet from user"""
    logging.info(f"DEBUG: Twitter Intent")


    try:
        
        bearer_token = os.getenv("TWITTER_TOKEN")
        auth = tweepy.OAuth2BearerHandler(bearer_token)

        api = tweepy.API(auth)

        if "Twitter" in query_result["parameters"]:
            twitter_user = query_result["parameters"]["Twitter"]
        else:
            twitter_user = "@elonmusk"

        if twitter_user == "":
            twitter_user = "@elonmusk"
        
        user_tweets = api.user_timeline(screen_name=twitter_user.replace("@", ""))

        latest_tweet = user_tweets[0]

        return [f"{twitter_user} latest tweet: {latest_tweet.text}"]

    except Exception as e:
        logging.info(f"Twitter Exception: {e}")
        return ["My engineers are working on this right now - thanks for talking to Elon Musk Bot"]