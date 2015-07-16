from unittest import TestCase
from apis.twitter_api import Tweet
import twitter_analysis

__author__ = 'dominic'


class ContainsTopicTest(TestCase):
    def test_rain_true(self):
        tweet = Tweet().text = "It is raining"
        self.assertTrue(twitter_analysis.contains_topic(tweet, twitter_analysis.RAIN))

    def test_rain_false(self):
        tweet = Tweet().text = "Tocotronic rocks"
        self.assertFalse(twitter_analysis.contains_topic(tweet, twitter_analysis.RAIN))