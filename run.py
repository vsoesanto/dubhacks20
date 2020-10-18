from scraper import tweet_scraper
import sentiment_analyzer

tweet_scraper("realDonaldTrump")
sentiment_analyzer.run("tweets_trump.tsv")