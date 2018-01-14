import sys
import tweepy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


def loadkeys(filename):
    """"
    load twitter api keys/tokens from CSV file with form
    consumer_key, consumer_secret, access_token, access_token_secret
    """
    with open(filename) as f:
        items = f.readline().strip().split(', ')
        return items


def authenticate(twitter_auth_filename):
    """
    Given a file name containing the Twitter keys and tokens,
    create and return a tweepy API object.
    """
    keys = loadkeys(twitter_auth_filename)
    auth = tweepy.OAuthHandler(keys[0], keys[1])
    auth.set_access_token(keys[2], keys[3])

    api = tweepy.API(auth)

    return api


def fetch_tweets(api, name):
    """
    Given a tweepy API object and the screen name of the Twitter user,
    create a list of tweets where each tweet is a dictionary with the
    following keys:

       id: tweet ID
       created: tweet creation date
       retweeted: number of retweets
       text: text of the tweet
       hashtags: list of hashtags mentioned in the tweet
       urls: list of URLs mentioned in the tweet
       mentions: list of screen names mentioned in the tweet
       score: the "compound" polarity score from vader's polarity_scores()

    Return a dictionary containing keys-value pairs:

       user: user's screen name
       count: number of tweets
       tweets: list of tweets, each tweet is a dictionary

    For efficiency, create a single Vader SentimentIntensityAnalyzer()
    per call to this function, not per tweet.
    """

    timeline = api.user_timeline(screen_name=name, include_rts=True, count = 100)
    all_tweets_dict = dict()
    all_tweets_dict['user'] = name
    all_tweets_dict['count'] = api.get_user(screen_name = name).statuses_count
    tweets = []
    analyzer = SentimentIntensityAnalyzer()

    for tweet in timeline:
        dict1 = dict()
        dict1['id'] = tweet.id
        dict1['created'] = tweet.created_at
        dict1['retweeted'] = tweet.retweeted
        dict1['text'] = tweet.text
        dict1['hashtags'] = tweet.entities.get('hashtags')
        dict1['urls'] = tweet.entities.get('urls')
        dict1['mentions'] = tweet.entities.get('user_mentions')
        dict1['score'] = analyzer.polarity_scores(tweet.text)['compound']
        tweets.append(dict1)
    all_tweets_dict['tweets'] = tweets
    return all_tweets_dict


def fetch_following(api,name):
    """
    Given a tweepy API object and the screen name of the Twitter user,
    return a a list of dictionaries containing the followed user info
    with keys-value pairs:

       name: real name
       screen_name: Twitter screen name
       followers: number of followers
       created: created date (no time info)
       image: the URL of the profile's image

    To collect data: get a list of "friends IDs" then get
    the list of users for each of those.
    """
    users = api.friends(screen_name = name, count = 200)
    following = []
    for user in users:
        dict1 = dict()
        dict1['name'] = user.name
        dict1['screen_name'] = user.screen_name
        dict1['followers'] = user.followers_count
        dict1['created'] = (user.created_at).date()
        dict1['image'] = user.profile_image_url
        following.append(dict1)
    return following