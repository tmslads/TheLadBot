import praw
import requests
import shutil
import random as r
import os

reddit = praw.Reddit(client_id='AmJbMF6Sh56JNg',
                     client_secret='1K1ovK2ku9EP_usjLR-8CFRiQB8',
                     user_agent='windows:test:v0.1 (by u/unclesam79)')

subreddits = ['dankmemes', 'memes', 'pewdiepiesubmissions', 'biologymemes', 'programmerhumor', 'chemistrymemes', 'physicsmemes']
filters = (('all', 3), ('month', 3), ('day', 10), ('week', 5))
SUBMISSIONS = []


def get_submissions():
    """Add submissions (title, url, extension) to SUBMISSIONS"""

    print("Fetching submissions...")
    SUBMISSIONS.clear()  # Removes previously fetched submissions
    for sub in subreddits:
        for i in range(4):
            for submission in reddit.subreddit(sub).top(time_filter=filters[i][0], limit=filters[i][1]):
                extension = submission.url[-4:]
                if extension in ['.jpg', '.png']:
                    SUBMISSIONS.append((removed_nonalnum(submission.title), submission.url, extension))
    print(f"Got {len(SUBMISSIONS)} submissions in total from {subreddits}.")


def get_meme():
    """Return a random submission (title, url, extension) from SUBMISSIONS"""

    if SUBMISSIONS == []:
        get_submissions()
        submission = r.choice(SUBMISSIONS)
    else:
        submission = r.choice(SUBMISSIONS)
    SUBMISSIONS.remove(submission)
    return submission


def save_meme(number=1):
    """Download memes (default is 1 meme)"""

    for i in range(number):
        meme = get_meme()
        response = requests.get(meme[1], stream=True)
        response.raw.decode_content = True  # To prevent file size appearing to be 0
        local_file = open(f"{'_'.join(meme[0].split())}{meme[2]}", 'wb')
        shutil.copyfileobj(response.raw, local_file)
        local_file.close()
    cwd = os.getcwd()
    print(f"{number} meme(s) downloaded to {cwd}")


def removed_nonalnum(title):
    """Return title after stripping special characters"""

    result = ''
    for character in title:
        if character.isalnum() or character.isspace():
            result += character
    return result


get_submissions()
r.shuffle(SUBMISSIONS)
