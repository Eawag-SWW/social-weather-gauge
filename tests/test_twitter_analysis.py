from unittest import TestCase

from apis.twitter_api import Tweet
from main import twitter_analysis
from main.twitter_analysis import contains_topic, RAIN

__author__ = 'dominic'

class ContainsTopicTest(TestCase):

    def test_rain_true(self):
        tweet = Tweet()
        tweet.text = "It is raining"
        claim = contains_topic(tweet, RAIN)
        self.assertTrue(claim)

    def test_rain_false(self):
        tweet = Tweet()
        tweet.text = "Tocotronic rocks"
        claim = contains_topic(tweet, RAIN)
        self.assertFalse(claim)