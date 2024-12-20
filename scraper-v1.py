import requests
from bs4 import BeautifulSoup

# Define the URL to scrape
URL = "https://realpython.github.io/fake-jobs/"

# Send a GET request to the URL
page = requests.get(URL)

# Create a BeautifulSoup object to parse the HTML content
soup = BeautifulSoup(page.content, "html.parser")

# Find all job listings on the page
job_elements = soup.find_all("div", class_="card-content")

# Extract and print information from each job listing
for job in job_elements:
    title = job.find("h2", class_="title").text.strip()
    company = job.find("h3", class_="company").text.strip()
    location = job.find("p", class_="location").text.strip()
    
    print(f"Title: {title}")
    print(f"Company: {company}")
    print(f"Location: {location}")
    print("---")
