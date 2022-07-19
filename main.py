import json
import random
import time
import tweepy
#from os import environ
import credentials

# for use when heroku environ variables set up
# CONSUMER_KEY = environ['CONSUMER_KEY']
# CONSUMER_SECRET = environ['CONSUMER_SECRET']
# ACCESS_KEY = environ['ACCESS_KEY']
# ACCESS_SECRET = environ['ACCESS_SECRET']

# TODO - use environment variables instead
authenticator = tweepy.OAuthHandler(credentials.API_KEY, credentials.API_KEY_SECRET)
authenticator.set_access_token(credentials.ACCESS_TOKEN, credentials.ACCESS_TOKEN_SECRET)

api = tweepy.API(authenticator, wait_on_rate_limit=True)

def tweet_start_end_points():
    interval = 60 * 60 * 24 # once a day
    while True:
        starting_point = get_random_starting_point()
        ending_point = get_random_ending_point()

        tweet = """
                    Navigate from \"{}\" to \"{}\"
                    """.format(starting_point['title'], ending_point['title'])
        starting_point_link = """Start here:\n{}""".format(starting_point['link'])
        ending_point_link = """End here:\n{}""".format(ending_point['link'])

        original_tweet = api.update_status(tweet)

        reply1_tweet = api.update_status(starting_point_link,
                                         in_reply_to_status_id=original_tweet.id,
                                         auto_populate_reply_metadata=True)

        reply2_tweet = api.update_status(ending_point_link,
                                         in_reply_to_status_id=reply1_tweet.id,
                                         auto_populate_reply_metadata=True)

        time.sleep(interval)


def get_random_starting_point():
    with open('wiki_pages.json') as f:
        start_end_points = json.load(f)
        random_starting_point = random.choice(start_end_points['starting_points'])
        while random_starting_point['used']:
            random_starting_point = random.choice(start_end_points['starting_points'])
        random_starting_point['used'] = True
    f.close()
    with open('wiki_pages.json', 'w') as f:
         json.dump(start_end_points, f, indent=4)
    f.close()
    return random_starting_point


def get_random_ending_point():
    with open('wiki_pages.json') as f:
        start_end_points = json.load(f)
        random_ending_point = random.choice(start_end_points['ending_points'])
        while random_ending_point['used']:
            random_ending_point = random.choice(start_end_points['ending_points'])
        start_end_points.update()
        random_ending_point['used'] = True
        f.close()
    with open('wiki_pages.json', 'w') as f:
         json.dump(start_end_points, f, indent=4)
    f.close()
    return random_ending_point


tweet_start_end_points()
