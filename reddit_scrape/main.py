# secret: xKgzjw6KaizDlmpT1vxZ9KQNl4M9FQ
# client id: r9rTg0qMFqzCife9mGkrww
# user agent: Scrape News

import re
import praw

reddit = praw.Reddit(client_id='r9rTg0qMFqzCife9mGkrww', client_secret='xKgzjw6KaizDlmpT1vxZ9KQNl4M9FQ', user_agent='Scrape News')

subreddit_results = []
for subreddit in ['news','USNews','politics','worldnews','technology','science']:
    subreddit_results.append(reddit.subreddit(subreddit).hot(limit=None))

# inverted index: id, title, text
# database (for search summary): id, title, summary, score, link
# pagerank: id, score

post_scores = {}
total_score = 0
sql_statement = """CREATE TABLE Posts(
   postid      VARCHAR(20)  NOT NULL PRIMARY KEY 
  ,title      VARCHAR(97)
  ,summary    VARCHAR(266)
  ,score       INTEGER
  ,url        VARCHAR(131)
);
"""
inverted_index_str = ""

for hot_posts in subreddit_results:
    for post in hot_posts:
        # post.name post.title post.selftext post.permalink post.score
        post_scores[post.name] = post.score
        total_score += post.score

        cleaned_title = post.title.replace(',', ' ')
        cleaned_title = cleaned_title.replace("'", "")
        cleaned_title = re.sub(r"[^a-zA-Z0-9 ]+", " ", cleaned_title).casefold()

        cleaned_body = post.selftext.replace(',', ' ')
        cleaned_body = cleaned_body.replace("'", "")
        cleaned_body = re.sub(r"[^a-zA-Z0-9 ]+", " ", cleaned_body).casefold()

        summary = cleaned_body[:250] + "..."

        sql_statement += f"INSERT INTO Posts(postid,title,summary,score,url) VALUES ('{post.name}','{cleaned_title}','{summary}',{post.score},'{post.permalink}');\n"
        inverted_index_str += f"'{post.name}','{cleaned_title}','{cleaned_body}'\n"


with open("search.sql", "w") as file:
    file.write(sql_statement)

with open("input.csv", "w") as file:
    file.write(inverted_index_str)

with open("pagerank.out", "w") as file:
    for post_name, score in post_scores.items():
        file.write(f"{post_name},{float(score)/total_score}\n")