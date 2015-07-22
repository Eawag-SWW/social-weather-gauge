from unittest import TestCase
from apis.twitter_api import Tweet
import twitter_analysis

__author__ = 'dominic'


class ContainsTopicTest(TestCase):
    def test_rain_true(self):
        tweet = Tweet()
        tweet.text = "It is raining"
        claim = twitter_analysis.contains_topic(tweet, twitter_analysis.RAIN)
        self.assertTrue(claim)

    def test_rain_false(self):
        tweet = Tweet().text = "Tocotronic rocks"
        self.assertFalse(twitter_analysis.contains_topic(tweet, twitter_analysis.RAIN))