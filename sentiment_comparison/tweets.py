# pylint: disable=line-too-long
"""
Module responsible for handling Twitter API calls
"""
import os
from typing import List

import preprocessor as p
import tweepy


class Tweets:
    """ Class responsible for interaction with Twitter API

    Attributes:
        auth {AppAuthHandler} -- authorization handler object required by API object
        api {API} -- Twitter API object
    """

    def __init__(self):
        self.auth = tweepy.AppAuthHandler(os.environ['KEY'], os.environ['SECRET'])
        self.api = tweepy.API(self.auth)

    def fetch(self, keyword: str, *, mode: str = 'extended', language_shortcut: str = 'en',
              how_many: int = 100) -> List[str]:
        """ Fetches by default 100 tweets from Twitter using keyword argument

        Arguments:
            keyword {str} -- keyword by which the tweets are searched
            mode {str} -- which mode to use when searching.
            language_shortcut {str} -- language of tweets to search for
            how_many {int} -- number of tweets to fetch. Maximum is 100
        Returns:
            List of tweets
        """
        return [tweet.full_text for tweet in
                tweepy.Cursor(self.api.search, q=keyword, tweet_mode=mode, lang=language_shortcut).items(how_many)]

    @staticmethod
    def clean(tweets: List[str]) -> List[str]:
        """ Cleans tweets out of irrelevant characters

        Arguments:
            tweets {List} -- list of tweets to be cleaned
        Returns:
            List of cleaned tweets
        """
        return [p.clean(tweet) for tweet in tweets]
