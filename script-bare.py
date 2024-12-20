from datetime import datetime
import requests
from bs4 import BeautifulSoup
from db_util import get_most_recent_timestamp, get_posts, save_post


def scrape_posts(most_recent_timestamp: str) -> None: 
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

        print(f"Title: {title}")
        print(f"URL: {url}")
        print(f"ID: {post_id}")

        post_subline = soup.find("a", href=f"hide?id={post_id}&goto=news").parent
        created_at = post_subline.find("span", class_="age").get('title').split(" ")[0]
        
        created_at = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%S")

        print(f"Created At: {created_at}")
        print("---")

        if created_at > most_recent_timestamp:
            save_post(title, url, post_id, created_at)

if __name__ == "__main__":
    most_recent_timestamp = get_most_recent_timestamp()
    scrape_posts(most_recent_timestamp)