"""
Unit tests for tweets_sentiment.py module
"""
import unittest
from unittest import mock
from unittest.mock import PropertyMock

from sentiment_comparison import tweets_sentiment


class TestTweets(unittest.TestCase):
    """ Class for tweets_sentiment.py unit tests """

    @mock.patch('sentiment_comparison.tweets_sentiment.Tweets')
    def test_init(self, mock_tweets):
        """ Tests if TweetsSentiment __init__ method creates Tweets object as an attribute """
        twt_sentiment = tweets_sentiment.TweetsSentiment()

        mock_tweets.assert_called_once()
        self.assertEqual(twt_sentiment.tweets, mock_tweets.return_value)

    @mock.patch('sentiment_comparison.tweets_sentiment.Tweets')
    def test_compute_average_sentiment(self, mock_tweets):
        """ Tests if compute_average_sentiment method calls appropriate methods """
        mock_cleaned_tweets = mock_tweets.return_value.clean.return_value
        twt_sentiment = tweets_sentiment.TweetsSentiment()
        twt_sentiment.get_sentiment_scores = mock.MagicMock()
        mock_sentiment_scores = twt_sentiment.get_sentiment_scores.return_value

        twt_sentiment.compute_average_sentiment(keyword='test')

        self.assertEqual(2, mock_tweets.return_value.fetch.call_count)
        mock_tweets.return_value.clean.assert_called_once()
        twt_sentiment.get_sentiment_scores.assert_called_once_with(tweets=mock_cleaned_tweets)
        mock_sentiment_scores.mean.assert_called_once()

    @mock.patch('sentiment_comparison.tweets_sentiment.TextBlob')
    def test_get_sentiment_scores(self, mock_text_blob_class):
        """ Tests if compute_average_sentiment method calls appropriate methods """
        tweets_sentiment.TweetsSentiment.get_sentiment_scores(tweets=[])

        self.assertEqual(0, mock_text_blob_class.call_count)

        mock_text_blob = mock_text_blob_class.return_value
        mock_polarity = PropertyMock()
        mock_sentiment = PropertyMock()
        type(mock_text_blob).sentiment = mock_sentiment
        type(mock_text_blob.sentiment).polarity = mock_polarity
        mock_sentiment.reset_mock()

        tweets_sentiment.TweetsSentiment.get_sentiment_scores(tweets=['tweet1', 'tweet2'])

        self.assertEqual(2, mock_text_blob_class.call_count)
        self.assertEqual(2, mock_sentiment.call_count)
        self.assertEqual(2, mock_polarity.call_count)
