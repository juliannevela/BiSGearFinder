"""
This module uses Selenium to create a browser instance and interact with a website for the purpose of scraping requested data.
"""

import time
from selenium import webdriver
from bs4 import BeautifulSoup


def scrape_website(website: str):
    """
    Creates a browser instance and scrapes the requested website.

    Args:
        website (str): The URL of the website to be scraped.

    Returns:
        str: The HTML content of the scraped webpage.
    """
    print("Launching Chrome browser")

    options = webdriver.FirefoxOptions()
    driver = webdriver.Firefox(options=options)

    try:
        driver.get(website)
        print("Page loaded...")
        html = driver.page_source
        time.sleep(10)

        return html
    finally:
        driver.quit()


def extract_body_content(html_content):
    """
    Extracts the body content from the given HTML content.

    Args:
        html_content (str): The HTML content to extract the body from.

    Returns:
        str: The extracted body content, or an empty string if no body content is found.
    """

    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body
    if body_content:
        return str(body_content)
    return ""


def clean_body_content(body_content):
    """
    Cleans the given HTML content by removing any script or style tags and
    any unnecessary whitespace from the content.

    Args:
        body_content (str): The HTML content to be cleaned.

    Returns:
        str: The cleaned HTML content.
    """
    soup = BeautifulSoup(body_content, "html.parser")

    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()

    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(
        line.strip() for line in cleaned_content.splitlines() if line.strip()
    )

    return cleaned_content


def split_dom_content(dom_content, max_length=6000):
    """
    Splits the given DOM content into an array of strings, with a maximum length
    of max_length. This is useful for splitting a large block of text into
    smaller chunks for processing.

    Args:
        dom_content (str): The DOM content to be split.
        max_length (int, optional): The maximum length of each chunk. Defaults to 6000.

    Returns:
        list: A list of strings, with a maximum length of max_length.
    """
    return [
        dom_content[: i + max_length] for i in range(0, len(dom_content), max_length)
    ]
