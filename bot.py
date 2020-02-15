import praw
import config
from analyzer import analyze
from analyzer import clean
import time


def bot_login():
    print("Logging in...")
    r = praw.Reddit(username = config.username,
                password = config.password,
                client_id = config.client_id,
                client_secret = config.client_secret,
                user_agent = "thought-police-bot"
                )
    print("Logged in!")
    return r

def run_bot(r):
    for mention in r.inbox.unread(limit=10):
        if (mention.was_comment):
            target = mention.parent().author
            if (target.name != config.username):
                countP = 0
                countN = 0
                ratio = 0
                
                #summarize target comment history sentiment
                for comment in r.redditor(target.name).comments.new(limit=None):
                    sentiment = analyze(comment.body)
                    if (sentiment == 1):
                        countP+=1
                    elif (sentiment == -1):
                        countN+=1

                if (countN + countP != 0):
                    ratio = countP / (countN + countP)

                print('countP: ' + str(countP))
                print('countN: ' + str(countN))
                print('ratio: ' + str(ratio))
                
                #Build comment reply
                graph = "##👿 <"
                for i in range(10):
                    if (ratio <= (i + 1) / 10 and ratio >= (i) / 10):
                        graph+=" x "
                    else:
                        graph+=" - "
                graph += "> 😇  "
                reply = "You have summoned the **Thought-Police-Bot** to investigate /u/" + target.name + "\n\n"
                reply += graph + "\n\n"

                if (ratio > 0.80):
                    reply += "/u/" + target.name + " passes the investigation with an impressively wholesome rating."
                elif (ratio > 0.6):
                    reply += "/u/" + target.name + " passes the investigation respectably." 
                elif (ratio > 0.45):
                    reply += "/u/" + target.name + " passes the investigation... but just barely."
                elif (ratio > 0.2):
                    reply += "/u/" + target.name + " has failed the investigation!"
                else:
                    reply += "/u/" + target.name + " has failed the investigation with a highly toxic rating!"
                try:
                    mention.reply(reply)
                except Exception:
                    print("Error replying - PRAWException")
            else:
                print("Skipped")
        mention.mark_read()
            
    
    time.sleep(5)

while True:
    r = bot_login()
    run_bot(r)