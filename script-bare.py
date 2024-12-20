import requests
from bs4 import BeautifulSoup

# Define the URL to scrape
URL = "https://news.ycombinator.com/"

# Send a GET request to the URL
page = requests.get(URL)

# Create a BeautifulSoup object to parse the HTML content
soup = BeautifulSoup(page.content, "html.parser")

# Find all job listings on the page
job_elements = soup.find_all("tr", class_="athing submission")
# Extract and print information from each job listing
for job in job_elements:
    span = job.find("span", class_="titleline")

    title = span.find("a").text
    url = span.find("a").get("href")
    post_id = job.get("id")
    
    print(f"Title: {title}")
    print(f"URL: {url}")
    print(f"ID: {post_id}")
