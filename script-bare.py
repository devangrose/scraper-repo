from datetime import datetime
import marvin
import requests
from bs4 import BeautifulSoup
from db_util import get_most_recent_timestamp, get_posts, get_posts_with_no_comments, save_comment, save_post


# Set this to 1 to print activity logs and errors
# Set this to 2 to print detailed logs
# Set this to 0 to print no logs
LOG_LEVEL = 1
GET_SENTIMENT = False

def scrape_posts(most_recent_timestamp: str) -> None: 
    if LOG_LEVEL > 0:
        print(f"Scraping posts from Hacker News after {most_recent_timestamp}")
        
    if most_recent_timestamp is None:
        most_recent_timestamp = datetime.min
    # Define the URL to scrape
    URL = "https://news.ycombinator.com/"

    # Send a GET request to the URL
    page = requests.get(URL)

    # Create a BeautifulSoup object to parse the HTML content
    soup = BeautifulSoup(page.content, "html.parser")

    # Find all posts on the page
    posts = soup.find_all("tr", class_="athing submission")

    # Extract and print information from each post
    for post in posts:
        span = post.find("span", class_="titleline")
        title = span.find("a").text
        url = span.find("a").get("href")
        post_id = post.get("id")



        post_subline = soup.find("a", href=f"hide?id={post_id}&goto=news").parent
        created_at = post_subline.find("span", class_="age").get('title').split(" ")[0]
        
        created_at = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%S")

        if LOG_LEVEL > 1:
            print(f"Title: {title}")
            print(f"URL: {url}")
            print(f"ID: {post_id}")
            print(f"Created At: {created_at}")
            print("---")

        # Save the post if it's newer than the most recent post in the database
        if created_at > most_recent_timestamp:
            if LOG_LEVEL > 0:
                print("Saving post")
            save_post(title, url, post_id, created_at)

def scrape_comments():
    posts = get_posts_with_no_comments()
    for post in posts:
        post_id = post[4]
        scrape_post_comments(post_id)

def scrape_post_comments(post_id: int):
    if LOG_LEVEL > 0:
        print(f"Scraping comments for post {post_id}")
    # Define the URL to scrape
    URL = "https://news.ycombinator.com/item?id=" + str(post_id)

    # Send a GET request to the URL
    page = requests.get(URL)

    # Create a BeautifulSoup object to parse the HTML content
    soup = BeautifulSoup(page.content, "html.parser")

    # get top ten comments
    comments = soup.find_all("tr", class_="athing comtr")
    comments = comments[:10]

    # Extract and print information from each comment
    for comment in comments:
        comment_id = comment.get("id")
        text_div = comment.find("div", class_="commtext")
        text = text_div.get_text()
        created_at = comment.find("span", class_="age").get('title').split(" ")[0]
        created_at = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%S")

        sentiment = None

        if GET_SENTIMENT:
            sentiment = marvin.extract(text, instructions="get the general sentiment of the text and return a list")

        if LOG_LEVEL > 1:
            print(f"Comment ID: {comment_id}")
            print(f"Text: {text}")
            print(f"Created At: {created_at}")
            print(f"Sentiment: {sentiment}")
            
        # # Save the comment
        save_comment(post_id, text, created_at, sentiment)

if __name__ == "__main__":
    most_recent_timestamp = get_most_recent_timestamp()
    scrape_posts(most_recent_timestamp)
    # scrape_post_comments(42473321)
    scrape_comments()