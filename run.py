from scraper import tweet_scraper
import sentiment_analyzer
import sys

handle = sys.argv[1]
tweet_scraper(handle)
sentiment_analyzer.run("tweets_trump.tsv")