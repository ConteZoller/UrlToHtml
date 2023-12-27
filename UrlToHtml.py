# Importing necessary libraries
import os
import requests
import re
import logging
from urllib.parse import urlparse

# Configuring logging for debugging purposes
logging.basicConfig(filename='download_html_log.txt', level=logging.DEBUG)

# Function to download HTML content from a given URL
def download_html(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        return response.text
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to download HTML from {url}: {e}")
        return None

# Function to save HTML content to a file based on the URL
def save_html_to_file(html, url):
    try:
        file_name = generate_file_name(url)

        if file_name:
            match = re.search(r'^[^.]+', file_name)
            if match:
                main_folder = 'html_downloads'
                folder = match.group()
                html_downloads_path = os.path.join(os.getcwd(), main_folder)
                folder_path = os.path.join(html_downloads_path, folder)
                os.makedirs(folder_path, exist_ok=True)

                file_path = os.path.join(folder_path, file_name)
                
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(html)

                logging.debug(f"HTML saved to: {file_path}")
            else:
                logging.error(f"Error extracting the output folder from the URL.")
    except Exception as e:
        logging.error(f"Failed to save HTML to file: {e}")

# Function to generate a file name based on the URL
def generate_file_name(url):
    try:
        # Extracting the domain and path from the URL
        domain = urlparse(url).netloc + urlparse(url).path
        print(domain)
        
        # Replacing '/' with '_' in the domain for file naming
        domain = domain.replace('/', '_')
        return f"{domain}.html"
    except Exception as e:
        logging.error(f"Error generating file name: {str(e)}")
        return None

# Main function to handle user input and process URLs
def main():
    input_user = input("Enter a URL or the path to a file containing URLs: ").strip()

    try:
        # Checking if the input is a single URL or a file with multiple URLs
        if input_user.startswith(('http://', 'https://')):
            urls = [input_user]
        else:
            with open(input_user, 'r') as file:
                urls = [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        logging.error(f"File not found: {input_user}")
        return
    except Exception as e:
        logging.error(f"Error reading the file: {e}")
        return

    # Processing each URL
    for url in urls:
        html = download_html(url)
        if html:
            save_html_to_file(html, url)

# Entry point of the script
if __name__ == "__main__":
    main()
