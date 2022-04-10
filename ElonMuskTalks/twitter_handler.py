import os
import tweepy
import logging
import azure.functions as func


def handle_twitter(query_result):
    """Returns the last tweet from user"""
    logging.info(f"DEBUG: Twitter Intent")


    try:
        
        bearer_token = os.getenv("TWITTER_TOKEN")
        client = tweepy.Client(bearer_token)

        if "Twitter" in query_result["parameters"]:
            twitter_user = query_result["parameters"]["Twitter"]
        else:
            twitter_user = "@elonmusk"

        if twitter_user == "":
            twitter_user = "@elonmusk"
        
        user_id_query = client.get_users(
            usernames=[twitter_user.replace("@", "")]
        )
        user_id = user_id_query[0][0].id
        response = client.get_users_tweets(user_id)

        latest_tweet = response.data[0]

        return [f"{twitter_user} latest tweet: {latest_tweet.text}"]

    except Exception as e:
        logging.info(f"Twitter Exception: {e}")
        return ["My engineers are working on this right now - thanks for talking to Elon Musk Bot"]