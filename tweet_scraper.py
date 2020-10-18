import tweepy as tw
import pandas as pd
import re


def tweet_scraper(handle):
    consumer_key = 'G3J86xaFnmfL7V3qCnsKi1fbr'
    consumer_secret = 'PJuenoCb6GYYNAxPfBdD5qBxihH1nUjQakXh0iVZiKjDREc8Zb'
    access_token = '1158946922696044544-TEzmCM9c8CepNtqFnRbeqeY86JdbFV'
    access_token_secret = 'x44U5n30TeENFiy8CyzX3XScr2C2diNarn32XF0JtuqqC'

    auth = tw.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tw.API(auth, wait_on_rate_limit=True)
    tweets = []

    try:
        api.verify_credentials()
        print("Authentication OK")
    except:
        print("Error during authentication")

    print(handle)

    for status in tw.Cursor(api.user_timeline, screen_name=handle, tweet_mode="extended").items():
        # print(status.full_text)
        # print(status.created_at)
        # self.tweets.append((status.full_text, status.created_at))
        if status.in_reply_to_user_id is None:
            # only add tweets that are not in reply to other twitter users
            tweets.append((re.sub("\n", " ", status.full_text), status.created_at))

    print("Retrieved " + str(len(tweets)) + " tweets")

    df = pd.DataFrame(tweets, columns=["tweets", "date"])
    df.to_csv("tweets.tsv", sep="\t", index=False)


if __name__ == "__main__":
    tweet_scraper("iced__latte")

