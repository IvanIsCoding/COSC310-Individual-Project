import os
import tweepy
import logging
import azure.functions as func


def handle_twitter(query_result):
    """Returns the last tweet from user"""
    logging.info(f"DEBUG: Twitter Intent")

    try:
        if "Twitter" in query_result["parameters"]:
            twitter_user = query_result["parameters"]["Twitter"]
        else:
            twitter_user = "@elonmusk"

        if twitter_user == "":
            twitter_user = "@elonmusk"
        
        return [f"My engineers are working on getting the tweet from {twitter_user}"]

    except:
        return ["My engineers are working on this right now - thanks for talking to Elon Musk Bot"]