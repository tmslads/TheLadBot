import praw
import requests
import shutil
import random as r

reddit = praw.Reddit(client_id='AmJbMF6Sh56JNg',
                     client_secret='1K1ovK2ku9EP_usjLR-8CFRiQB8',
                     user_agent='windows:test:v0.1 (by u/unclesam79)')

subreddits = ['dankmemes', 'memes', 'pewdiepiesubmissions']
filters = (('all', 5), ('month', 5), ('day', 10), ('week', 10))
submissions = []


def get_submissions():
    """Adds submissions (title and url) to the submissions list"""

    submissions.clear()  # Removes previously fetched submissions
    for sub in subreddits:
        for i in range(4):
            for submission in reddit.subreddit(sub).top(time_filter=filters[i][0], limit=filters[i][1]):
                submissions.append((submission.title, submission.url))


def get_meme_url():
    while True:
        submission = r.choice(submissions)
        title, url = submission
        extension = url[-4:]
        if extension in ['.jpg', '.png']:
            response = requests.get(url, stream=True)
            if submissions == []:
                get_submissions()
            else:
                submissions.remove(submission)
            break


local_file = open(f'meme{extension}', 'wb')
response.raw.decode_content = True  # To prevent file size appearing to be 0
shutil.copyfileobj(response.raw, local_file)
local_file.close()
