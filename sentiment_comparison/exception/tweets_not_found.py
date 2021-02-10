"""
Module with TweetsNotFound exception class
"""


class TweetsNotFound(Exception):
    """ Class for custom exception when no tweets are found """

    def __init__(self):
        super().__init__()
        self.reason = 'Some tweets were not found. Try with different keyword'
