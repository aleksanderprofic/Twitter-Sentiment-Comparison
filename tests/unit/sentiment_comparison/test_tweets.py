"""
Unit tests for tweets.py module
"""
import unittest
from unittest import mock

from sentiment_comparison import tweets


class TestTweets(unittest.TestCase):
    """ Class for tweets.py unit tests """

    @mock.patch('sentiment_comparison.tweets.os.environ')
    @mock.patch('sentiment_comparison.tweets.tweepy')
    def test_init(self, mock_tweepy, mock_os_environ):
        """ Tests if Tweets __init__ method creates correct attributes """
        mock_os_environ.__getitem__.return_value = 'test_value'
        mock_tweepy.AppAuthHandler.return_value = 'test_auth'

        tweets.Tweets()

        mock_tweepy.AppAuthHandler.assert_called_once_with('test_value', 'test_value')
        mock_tweepy.API.assert_called_once_with('test_auth')

    @mock.patch('sentiment_comparison.tweets.os.environ')
    @mock.patch('sentiment_comparison.tweets.tweepy')
    def test_fetch(self, mock_tweepy, mock_os_environ):
        """ Tests if fetch method calls appropriate methods """
        mock_os_environ.__getitem__.return_value = 'test_value'
        twt = tweets.Tweets()

        twt.fetch(keyword='test', how_many=100)

        mock_tweepy.Cursor.assert_called_once()
        mock_tweepy.Cursor.return_value.items.assert_called_once_with(100)

    @mock.patch('sentiment_comparison.tweets.p')
    def test_clean(self, mock_preprocessor):
        """ Tests if clean method calls clean method the same number of times as there are items in tweets argument """
        tweets.Tweets.clean(tweets=['tweet1', 'tweet2'])

        self.assertEqual(2, mock_preprocessor.clean.call_count)
        mock_preprocessor.clean.reset_mock()

        tweets.Tweets.clean(tweets=[])

        self.assertEqual(0, mock_preprocessor.clean.call_count)
