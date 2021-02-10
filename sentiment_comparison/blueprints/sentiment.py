# pylint: disable=line-too-long
"""
Module with endpoints related to sentiment calculation
"""
import base64

from multiprocessing import Pool, cpu_count

from flask import Blueprint, request, render_template, redirect
from tweepy import TweepError

from sentiment_comparison.exception.tweets_not_found import TweetsNotFound
from sentiment_comparison.tweets_sentiment import TweetsSentiment
from sentiment_comparison.visualisation import make_plot

sentiment = Blueprint("Sentiment", __name__, url_prefix='/sentiment')


@sentiment.route('/', methods=['GET', 'POST'])
def compare_sentiments():
    """ Endpoint for triggering sentiments calculation """
    if request.method == 'GET':
        return redirect('/')
    keywords = [keyword.strip() for keyword in request.form['keywords'].split(',')]
    if len(keywords) > 7:
        return render_template('index.html', error=True, message="The maximum amount of keywords is 7")
    try:
        tweets_sentiment = TweetsSentiment()
        with Pool(min(cpu_count(), len(keywords))) as pool:
            sentiments_with_names = {keyword: sent for keyword, sent in
                                     zip(keywords, pool.map(tweets_sentiment.compute_average_sentiment, keywords))}
    except TweepError:
        return render_template('index.html', error=True, message="Something went wrong. Try again later!")
    except TweetsNotFound as exception:
        return render_template('index.html', error=True, message=exception.reason)

    image, width, height = make_plot(sentiments_with_names=sentiments_with_names)
    image = base64.b64encode(image.getvalue())
    image = image.decode('utf8')

    return render_template('index.html', image=image, width=width, height=height)
