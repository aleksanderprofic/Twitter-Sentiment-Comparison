"""
Unit tests for sentiment.py module
"""
import unittest
from unittest import mock
from unittest.mock import PropertyMock, MagicMock

from tweepy import TweepError

from sentiment_comparison.blueprints import sentiment


class TestSentiment(unittest.TestCase):
    """ Class for sentiment.py unit tests """

    @mock.patch('sentiment_comparison.blueprints.sentiment.redirect')
    @mock.patch('sentiment_comparison.blueprints.sentiment.request')
    def test_compare_sentiments__when_GET_method(self, mock_request, mock_redirect):
        mock_request_method = PropertyMock(return_value='GET')
        type(mock_request).method = mock_request_method

        sentiment.compare_sentiments()

        mock_request_method.assert_called_once()
        mock_redirect.assert_called_once_with('/')

    @mock.patch('sentiment_comparison.blueprints.sentiment.render_template')
    @mock.patch('sentiment_comparison.blueprints.sentiment.base64')
    @mock.patch('sentiment_comparison.blueprints.sentiment.make_plot')
    @mock.patch('sentiment_comparison.blueprints.sentiment.Pool')
    @mock.patch('sentiment_comparison.blueprints.sentiment.TweetsSentiment')
    @mock.patch('sentiment_comparison.blueprints.sentiment.request')
    def test_compare_sentiments__when_POST_method_and_no_errors(
            self, mock_request, mock_tweets_sentiment, mock_pool, mock_make_plot, mock_base64, mock_render_template):
        mock_request_method = PropertyMock(return_value='POST')
        type(mock_request).method = mock_request_method
        mock_request.form.__getitem__.return_value = 'keyword1 ,keyword2, keyword3 '

        mock_image = MagicMock()
        mock_make_plot.return_value = (mock_image, 1, 2)

        sentiment.compare_sentiments()

        mock_request_method.assert_called_once()
        mock_request.form.__getitem__.assert_called_once_with('keywords')
        mock_tweets_sentiment.assert_called_once()
        mock_pool.assert_called_once()
        mock_make_plot.assert_called_once()
        mock_image.getvalue.assert_called_once()
        mock_base64.b64encode.assert_called_once()
        mock_base64.b64encode.return_value.decode.assert_called_once()
        mock_render_template.assert_called_once()

    @mock.patch('sentiment_comparison.blueprints.sentiment.render_template')
    @mock.patch('sentiment_comparison.blueprints.sentiment.TweetsSentiment')
    @mock.patch('sentiment_comparison.blueprints.sentiment.request')
    def test_compare_sentiments__when_POST_method_and_error_occurs(
            self, mock_request, mock_tweets_sentiment, mock_render_template):
        mock_request_method = PropertyMock(return_value='POST')
        type(mock_request).method = mock_request_method
        mock_request.form.__getitem__.return_value = 'keyword1 ,keyword2, keyword3 '
        mock_tweets_sentiment.side_effect = TweepError('test reason')

        sentiment.compare_sentiments()

        mock_request_method.assert_called_once()
        mock_request.form.__getitem__.assert_called_once_with('keywords')
        mock_tweets_sentiment.assert_called_once()
        mock_render_template.assert_called_once()

    @mock.patch('sentiment_comparison.blueprints.sentiment.render_template')
    @mock.patch('sentiment_comparison.blueprints.sentiment.request')
    def test_compare_sentiments__when_POST_method_and_more_than_eight_keywords(
            self, mock_request, mock_render_template):
        mock_request_method = PropertyMock(return_value='POST')
        type(mock_request).method = mock_request_method
        mock_request.form.__getitem__.return_value = 'k1,k2,k3,k4,k5,k6,k7,k8,k9'

        sentiment.compare_sentiments()

        mock_request_method.assert_called_once()
        mock_request.form.__getitem__.assert_called_once_with('keywords')
        mock_render_template.assert_called_once_with('index.html', error=True,
                                                     message="The maximum amount of keywords is 7")
