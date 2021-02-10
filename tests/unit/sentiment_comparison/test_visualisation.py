"""
Unit tests for visualisation.py module
"""
import unittest
from unittest import mock

from sentiment_comparison import visualisation


class TestVisualisation(unittest.TestCase):
    """ Class for visualisation.py unit tests """

    @mock.patch('sentiment_comparison.visualisation.io')
    @mock.patch('sentiment_comparison.visualisation.plt')
    def test_make_plot__when_number_of_keywords_less_than_four(self, mock_plt, mock_io):
        """ Tests if make_plot function calls methods with appropriate arguments when number of keywords
        less than four """
        sentiments_with_names = {'keyword1': 0.3, 'keyword2': 0.7, 'keyword3': -0.9}
        dpi = 80
        fig_size = (5, 5)

        result = visualisation.make_plot(sentiments_with_names=sentiments_with_names)

        self.assert_called_appropriate_methods(mock_plt, mock_io, dpi, fig_size, result)

    @mock.patch('sentiment_comparison.visualisation.io')
    @mock.patch('sentiment_comparison.visualisation.plt')
    def test_make_plot__when_number_of_keywords_less_than_eight(self, mock_plt, mock_io):
        """ Tests if make_plot function calls methods with appropriate arguments when number of keywords
        greater than four and less than eight """
        sentiments_with_names = {'keyword1': 0.0, 'keyword2': 0.2, 'keyword3': -0.3, 'keyword4': 0.6, 'keyword5': -0.1}
        dpi = 80
        fig_size = (10, 5)

        result = visualisation.make_plot(sentiments_with_names=sentiments_with_names)

        self.assert_called_appropriate_methods(mock_plt, mock_io, dpi, fig_size, result)

    def assert_called_appropriate_methods(self, mock_plt, mock_io, dpi, fig_size, result):
        mock_plt.clf.assert_called_once()
        mock_plt.figure.assert_called_once_with(dpi=dpi, figsize=fig_size)
        mock_plt.bar.assert_called_once()
        mock_plt.title.assert_called_once()
        mock_io.BytesIO.assert_called_once()
        mock_plt.savefig.assert_called_once_with(mock_io.BytesIO.return_value, format='png')
        mock_io.BytesIO.return_value.seek.assert_called_once_with(0)
        self.assertEqual(mock_io.BytesIO.return_value, result[0])
        self.assertEqual(fig_size[0] * dpi, result[1])
        self.assertEqual(fig_size[1] * dpi, result[2])
