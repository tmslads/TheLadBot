import random as r
import shutil
import requests

import praw


reddit_id, reddit_secret = open('creds.txt', 'r').read().split()
reddit = praw.Reddit(client_id=reddit_id,
                             client_secret=reddit_secret,
                             user_agent='windows:test:v0.1 (by u/unclesam79)')


class SubmissionFetcher():

    def __init__(self, subreddits, filter_count, filters):
        self.subreddits = subreddits
        self.filter_count = filter_count
        self.filters = filters
        self.SUBMISSIONS = []
        self.fetch_submissions()

    def fetch_submissions(self):
        """Retrieve submissions from Reddit, add to SUBMISSIONS"""

        print("Fetching submissions...")
        self.SUBMISSIONS.clear()  # Remove previously fetched submissions
        for sub in self.subreddits:
            for i in range(self.filter_count):
                for submission in reddit.subreddit(sub).top(time_filter=self.filters[i][0], limit=self.filters[i][1]):
                    if submission not in self.SUBMISSIONS:  # Unique submissions only
                        self.SUBMISSIONS.append(submission)
        print(f"Got {len(self.SUBMISSIONS)} submissions in total from {self.subreddits}.")

    def get_post(self):
        """Return a random submission from SUBMISSIONS"""

        if self.SUBMISSIONS == []:
            self.fetch_submissions()
        post = r.choice(self.SUBMISSIONS)
        self.SUBMISSIONS.remove(post)
        return post

    def save_meme(self, number=1):
        """Save memes to disk"""

        for i in range(number):
            meme = self.get_post()
            response = requests.get(meme.url, stream=True)
            response.raw.decode_content = True  # Prevents file size appearing to be 0
            local_file = open(f"{'_'.join(removed_nonalnum(meme.title).split())}{meme.url[-4:]}", 'wb')
            shutil.copyfileobj(response.raw, local_file)
            local_file.close()


def removed_nonalnum(title):
    """Return title after stripping special characters"""

    result = ''
    for character in title:
        if character.isalnum() or character.isspace():
            result += character
    return result


meme_subreddits = ['dankmemes', 'memes', 'pewdiepiesubmissions', 'biologymemes', 'programmerhumor', 'chemistrymemes', 'physicsmemes']
meme_filters = (('all', 3), ('month', 3), ('day', 10), ('week', 5))

song_subreddits = ['listentothis']
song_filters = (('month', 5), ('week', 10), ('day', 15))

meme_fetcher = SubmissionFetcher(subreddits=meme_subreddits, filter_count=4, filters=meme_filters)
song_fetcher = SubmissionFetcher(subreddits=song_subreddits, filter_count=3, filters=song_filters)
