import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
from tqdm import tqdm

def initialize(url):
    try:
        response = requests.get(url)
        response.raise_for_status()

    except requests.exceptions.RequestException as e:
        print(f"Error during HTTP request: {e}")

    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

def get_keywords(array):
    return array

def find_keywords(keywords, page):
    found_keywords = [keyword for keyword in keywords if keyword in page]
    if found_keywords:
        print("The following keywords were found:")
        for keyword_found in found_keywords:
            print(keyword_found)
        print('\n')
        return True
    else:
        print("None of the keywords were found in the page content.")
        return False

def write_to_file(file_path, content):
    with open(file_path, 'a') as file:
        file.write(content + '\n')

def same_domain(url1, url2):
    # print('same_domain')
    domain1 = urlparse(url1).netloc
    domain2 = urlparse(url2).netloc
    return domain1 == domain2

def collect_links(url, visited_urls, specific_keywords, excluded_keywords, specific_condition_choice, excluded_condition_choice):
    # print('collect_links')
    links = set()
    try:
        response = requests.get(url, timeout=20)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        for link_tag in soup.find_all(['a', 'link']):
            link_href = link_tag.get('href')
            if link_href:
                full_link = urljoin(url, link_href)  # Use urljoin to handle relative links
                specific_condition = any if specific_condition_choice and specific_condition_choice.lower() == 'any' else all
                excluded_condition = any if excluded_condition_choice and excluded_condition_choice.lower() == 'any' else all
                if full_link not in visited_urls and same_domain(url, full_link) and \
                        (not specific_condition_choice or specific_condition(keyword in full_link for keyword in specific_keywords)) and \
                        (not excluded_condition_choice or not excluded_condition(keyword in full_link for keyword in excluded_keywords)):
                    links.add(full_link)
                    print(full_link)

        if not links:
            print("No links found in the for loop.")

    except requests.exceptions.RequestException as e:
        print(f"Error during HTTP request: {e}")

    return links

def scrape_page(url, visited_urls, keywords, start_time=None, specific_keywords=None, excluded_keywords=None, result_file=None, specific_condition_choice=None, excluded_condition_choice=None):
    # print('scrape_page')
    if url in visited_urls:
        return

    visited_urls.add(url)

    if start_time is None:
        print(f"Starting page {url}.")
        start_time = time.time()

    links = collect_links(url, visited_urls, specific_keywords, excluded_keywords, specific_condition_choice, excluded_condition_choice)

    for link in tqdm(links, desc=f"Scrapping {url}", unit=" link"):
        if link.endswith(('.css', '.png', '.jpg', '.jpeg', '.gif', '.pdf')):
            continue  # Ignore .css, .png, etc. links

        try:
            response = requests.get(link, timeout=20)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            content_page = soup.get_text()
            found_keywords = [keyword for keyword in keywords if keyword in content_page]

            if found_keywords:
                elapsed_time = time.time() - start_time
                message = f"{link} - Keywords found: {', '.join(found_keywords)} - in {elapsed_time:.2f} seconds"

                if result_file:
                    # Write results to file
                    write_to_file(result_file, message)

            scrape_page(link, visited_urls, keywords, start_time, specific_keywords, excluded_keywords, specific_condition_choice, excluded_condition_choice)

        except requests.exceptions.Timeout:
            print(f"Timeout on page {link}. Restarting the function.")
            scrape_page(link, visited_urls, keywords, start_time, specific_keywords, excluded_keywords, specific_condition_choice, excluded_condition_choice)

        except requests.exceptions.RequestException as e:
            print(f"Error during HTTP request: {e}")

    if start_time is not None:
        elapsed_time = time.time() - start_time
        print(f"Finished page {url} in {elapsed_time:.2f} seconds.")
