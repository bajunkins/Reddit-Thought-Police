from textblob import TextBlob
import re

# Remove unnecessary syntax from text
def clean(text):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", text).split())

# Retrieve polarity
def analyze(text):
    analysis = TextBlob(clean(text))
    if analysis.sentiment.polarity > 0.5:
        return 1
    elif analysis.sentiment.polarity < -0.5:
        return -1
    else:
        return 0