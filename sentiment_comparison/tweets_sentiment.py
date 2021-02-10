"""
Module for computing tweets sentiment score
"""
from typing import Iterable

import numpy as np
from textblob import TextBlob

from sentiment_comparison.exception.tweets_not_found import TweetsNotFound
from sentiment_comparison.tweets import Tweets


class TweetsSentiment:
    """ Class for computing average sentiment of tweets """

    def __init__(self) -> None:
        self.tweets = Tweets()

    def compute_average_sentiment(self, keyword: str) -> float:
        """ Computes average sentiment score based on provided keyword

        Arguments:
            keyword {str} -- keyword by which the tweets are searched
        Returns:
            Average sentiment score
        """
        tweets = []
        for _ in range(2):
            tweets += self.tweets.fetch(keyword=keyword, how_many=100)

        if not tweets:
            raise TweetsNotFound()
        cleaned_tweets = self.tweets.clean(tweets=tweets)
        sentiment_scores = self.get_sentiment_scores(tweets=cleaned_tweets)

        return sentiment_scores.mean()

    @staticmethod
    def get_sentiment_scores(tweets: Iterable[str]) -> np.ndarray:
        """ Computes sentiment score for each tweet

        Arguments:
            tweets {Iterable} -- iterable object with tweets
        Returns:
            Numpy array with sentiment scores
        """
        return np.array([TextBlob(tweet).sentiment.polarity for tweet in tweets])
