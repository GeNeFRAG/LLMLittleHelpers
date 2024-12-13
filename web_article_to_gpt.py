import sys
import json
import os
import argparse
import requests
from bs4 import BeautifulSoup
import psutil
import time

def download_web_article(url):
    """
    Downloads the content of a web article.

    Args:
    url (str): The URL of the web article to download.

    Returns:
    str: The raw HTML content of the web article.
    """
    print(f"Attempting to download the web article from URL: {url}...")
    try:
        response = requests.get(url)
        response.raise_for_status()
        print("Web article successfully downloaded.")
        return response.text
    except requests.RequestException as e: # import requests
        print("Error: Unable to download web article.")
        print(f"{e}")
        sys.exit(1)

def clean_html_content(html_content):
    """
    Cleans the HTML content of a web article and extracts the main text.

    Args:
    html_content (str): The raw HTML content of the web article.

    Returns:
    str: The cleaned text content of the web article.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Remove script and style elements
    # amazonq-ignore-next-line
    for script_or_style in soup(['script', 'style']):
        script_or_style.decompose()
    
    # Extract text
    text = soup.get_text(separator=' ')
    
    # Collapse whitespace
    text = ' '.join(text.split())
    return text

def get_article_title(html_content):
    """
    Extracts the title of the web article from the HTML content.

    Args:
    html_content (str): The raw HTML content of the web article.

    Returns:
    str: The title of the web article.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    title = soup.title.string if soup.title and soup.title.string else "untitled"
    # amazonq-ignore-next-line
    return title.strip().replace(' ', '_')

def save_article_as_txt(article_text, output_path):
    """
    Save the article text as a TXT file.

    Args:
    article_text (str): The article text to save.
    output_path (str): The path to the output TXT file.
    """
    with open(output_path, "w", encoding="utf-8") as txt_file:
        txt_file.write(article_text)
    print(f"Article saved as TXT at: {output_path}")

def save_article_as_json(article_text, output_path):
    """
    Save the article text as a JSON file.

    Args:
    article_text (str): The article text to save.
    output_path (str): The path to the output JSON file.
    """
    article_data = {"article": article_text}
    try:
        with open(output_path, "w", encoding="utf-8") as json_file:
            json.dump(article_data, json_file, indent=4, ensure_ascii=False)
        print(f"Article saved as JSON at: {output_path}")
    except IOError as e:
        print(f"Error: Unable to save article as JSON. {e}")

def main(url, to_text, to_json):
    start_time = time.time()
    process = psutil.Process(os.getpid())
    cpu_usage = process.cpu_percent(0.0)
    
    html_content = download_web_article(url)
    article_text = clean_html_content(html_content)
    article_title = get_article_title(html_content)
    
    # Define output file paths
    txt_output_path = f"{article_title}.txt"
    json_output_path = f"{article_title}.json"
    
    # Save the article in TXT and/or JSON formats based on the command-line arguments
    try:
        if to_text:
            save_article_as_txt(article_text, txt_output_path)
        
        if to_json:
            save_article_as_json(article_text, json_output_path)
    except IOError as e:
            print(f"Error: Unable to save article. {e}")
    
    end_time = time.time()
    cpu_usage = process.cpu_percent(0.0)
    memory_info = process.memory_info()
    
    print(f"CPU usage: {cpu_usage}%")
    print(f"Memory usage: {memory_info.rss / (1024 * 1024):.2f} MB")
    print(f"Execution time: {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download and prepare web articles for GPT models.")
    parser.add_argument("url", type=str, help="The URL of the web article.")
    parser.add_argument("--to_text", action="store_true", help="Save article as TXT format.")
    parser.add_argument("--to_json", action="store_true", help="Save article as JSON format.")
    args = parser.parse_args()
    
    if not args.to_text and not args.to_json:
        print("Error: At least one of --to_text or --to_json must be specified.")
        sys.exit(1)
    
    main(args.url, args.to_text, args.to_json)