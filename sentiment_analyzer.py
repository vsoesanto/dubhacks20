import os
from google.cloud import language_v1
import pandas as pd
import timeit
import json
import datetime

credential_path = ""
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path


def analyze_sentiment(text_content):
    """
    Analyzes sentiment in a string using Google Cloud Natural Language API

    @:param text_content: The text content to analyze
    @:return overall score for sentiments in text_content
    """
    score = 0.0
    client = language_v1.LanguageServiceClient()

    # Available types: PLAIN_TEXT, HTML
    # type_ = language_v1.Document.Type.PLAIN_TEXT
    type_ = language_v1.enums.Document.Type.PLAIN_TEXT

    # Optional. If not specified, the language is automatically detected.
    # For list of supported languages:
    # https://cloud.google.com/natural-language/docs/languages
    language = "en"
    document = {"content": text_content, "type": type_, "language": language}

    # Available values: NONE, UTF8, UTF16, UTF32
    encoding_type = language_v1.enums.EncodingType.UTF8

    # response = client.analyze_sentiment(request = {'document': document, 'encoding_type': encoding_type})
    response = client.analyze_sentiment(document=document, encoding_type=encoding_type)
    # Get overall sentiment of the input document
    # print(u"Document sentiment score: {}".format(response.document_sentiment.score))
    # print(
    #     u"Document sentiment magnitude: {}".format(
    #         response.document_sentiment.magnitude
    #     )
    # )

    # Get sentiment for all sentences in the document
    for sentence in response.sentences:
        score += sentence.sentiment.score
        # print(u"Sentence text: {}".format(sentence.text.content))
        # print(u"Sentence sentiment score: {}".format(sentence.sentiment.score))
        # print(u"Sentence sentiment magnitude: {}".format(sentence.sentiment.magnitude))
        # print()

    # Get the language of the text, which will be the same as
    # the language specified in the request or, if not specified,
    # the automatically-detected language.
    # print(u"Language of the text: {}".format(response.language))
    return score


def run(path=None):
    if path is None:
        print("Please provide a path")
        exit()

    start = timeit.default_timer()
    tweets_df = pd.read_csv(path, sep="\t")
    tweets = tweets_df["tweets"]
    dates = tweets_df["date"]

    latest_date_str = dates[0]  # newest tweet is always the first item on the dataframe
    latest_date = datetime.datetime.strptime(latest_date_str, '%Y-%m-%d %H:%M:%S').date()
    # print("latest date = " + str(latest_date))

    date_to_sentiment = {}  # mapping of date to list of scores
    date_to_tweets = {}  # mapping of date to list of tweets

    average_sentiment = 0.0
    len_tweets_period = 0
    tweets_period = []
    for i, t in enumerate(tweets):
        score = analyze_sentiment(t)
        current_date = datetime.datetime.strptime(dates[i], '%Y-%m-%d %H:%M:%S').date()
        # print("current date = " + str(current_date))

        # if (latest_date - current_date).days >= 7:
        #     # print(str((latest_date - current_date).days) + " since latest date")
        #     # print(tweets_period)
        #     if len_tweets_period != 0:  # if there are tweets within this period
        #         date_to_sentiment[str(latest_date)] = score / len_tweets_period
        #         date_to_tweets[str(latest_date)] = tweets_period
        #
        #         # reset values
        #         len_tweets_period = 0
        #         score = 0.0
        #         tweets_period = []
        #         latest_date = current_date
        #         # print("adding to dictionaries")
        #         # print("setting latest date to =" + str(latest_date))
        #         # print()

        # average two scores at every iteration
        if str(latest_date) not in date_to_sentiment:
            date_to_sentiment[str(latest_date)] = score
        else:
            date_to_sentiment[str(latest_date)] = (score + date_to_sentiment[str(latest_date)]) / 2

        if str(latest_date) not in date_to_tweets:
            date_to_tweets[str(latest_date)] = []
        date_to_tweets[str(latest_date)].append(t)

        # reset values
        len_tweets_period = 0
        # score = 0.0
        tweets_period = []
        latest_date = current_date

        average_sentiment += score
        len_tweets_period += 1
        tweets_period.append(t)
        # print(t)
        # print("score=" + str(score) + "\n")

    data = {}
    data["entries"] = []
    for date in date_to_sentiment:
        print(date)
        print(date_to_sentiment[date])
        print(date_to_tweets[date])
        print()
        data["entries"].append({
            "date": date,
            "avg_sentiment": date_to_sentiment[date],
            "tweets": date_to_tweets[date]})

    # with open("results_trump.json", "w") as of:
    #     json.dump(data, of)

    stop = timeit.default_timer()
    # print("time=" + str(stop - start))



