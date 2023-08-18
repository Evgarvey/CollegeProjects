from nltk.tokenize import word_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re

#     TwitterAnalysis.py
#     Evan Garvey and Austin Johnson
#     NLTK-based sentiment analysis for Tweets derived from the twitter API


#     preprocess: take the raw tweets and do a couple of things to them, such as:
#              1) splitting them into appropriate lists
#              2) tokenizing the tweets, and filtering them of stopwords, and
#              3) lemmatizing them before returning it

def preprocess(tweets):
    lemmatizer = WordNetLemmatizer()
    preTweets = []
    fiveSections = re.split("T_TTweets for searching: [A-Za-z0-9]+ ballon dorT_T", tweets)
    for section in fiveSections:

        sectionTweets = section.split("\n\n")
        sectionPreTweets = []
        for tweet in sectionTweets:
            tokens = word_tokenize(tweet.lower())
            filteredTokens = [token for token in tokens if token not in stopwords.words('english')]
            lemmatizedTokens = [lemmatizer.lemmatize(token) for token in filteredTokens]
            sectionPreTweets.append(lemmatizedTokens)

        preTweets.append(sectionPreTweets)

    return preTweets[1:]

    # analyze: perform sentiment analysis on the tweets, by performing the following tasks:
    #       1) splitting the sections apart, and iterating through tweets as they are given,
    #       2) returning the tweet from a list into a string, before running it through an analyzer, and
    #       3) appending the sentiment compound back into a list before returning it.


def analyze(tweets):
    analyzer = SentimentIntensityAnalyzer()
    sentiments = []
    for section in tweets:

        sentimentSection = []
        for tweet in section[1:]:
            scores = analyzer.polarity_scores(" ".join(tweet))
            sentimentSection.append(scores['compound'])

        sentiments.append(sentimentSection)

    return sentiments

    # parse: take the raw sentiments and put them into usable numbers and metrics, such as:
    #     1) the section averages, which is just the average of all sentiments for a section,
    #     2) section percentages, as in what percentage of tweets have pos/neu/neg scores, and
    #     3) section counters, which is just how many tweets fall into each previously mentioned score.
    #     (section counters aren't necessarily required here but make things simpler)

def parse(sentiments):
    sectionAvgs = []
    sectionPercentages = []
    sectionCounters = []
    sectionUniques = []
    for section in sentiments:

        length = len(section)
        sectionAvgs.append(sum(section) / length)
        negCounter, neuCounter, posCounter = 0, 0, 0
        for sentiment in section:

            if sentiment < 0:
                negCounter += 1
            elif sentiment == 0:
                neuCounter += 1
            else:
                posCounter += 1

        sectionPercentages.append(
            [negCounter / length,
             neuCounter / length,
             posCounter / length])
        sectionCounters.append(
            [negCounter,
             neuCounter,
             posCounter])
        sectionUniques.append(len([*set(section)]))

    return sectionAvgs, sectionPercentages, sectionCounters, sectionUniques

    # displayDataTemp: a temporary function to display data, such as:
    #               1) total tweets as well as unique tweets,
    #               2) average sentiment scores, and
    #               3) percentages as well as counters for tweets of each sentiment.
    #                  feel free to delete this once you've set the graphics up.

def displayDataTemp(avgs, percentages, counters, uniques, names):

    print("\n\n")

    for i in range(len(names)):

        length = sum(counters[i])
        print("Data for", names[i])
        print(length, "total tweets were collected.")

        print(uniques[i], "tweets collected were unique tweets, equal to",
              round((uniques[i]/length) * 100, 2), "percent unique tweets.")

        print("Average sentiment score is", avgs[i])

        print("Tweets were", int(percentages[i][2] * 100), "percent positive (",
              counters[i][2], "positive tweets )")

        print("Tweets were", int(percentages[i][1] * 100), "percent neutral (",
              counters[i][1], "neutral tweets )")

        print("Tweets were", int(percentages[i][0] * 100), "percent negative (",
              counters[i][0], "negative tweets )")
        
        print("\n\n")

if __name__ == '__main__':
    file = open("tempTweets.txt", "r", encoding="utf8")
    data = file.read()
    file.seek(0)

    preTweets = preprocess(data)
    sentiments = analyze(preTweets)
    avgs, percentages, counters, uniques = parse(sentiments)
    displayDataTemp(avgs, percentages, counters, uniques, ["Messi", "Haaland", "Mbappe", "Benzema", "Vini Jr."])
