import requests
import re
from urllib.parse import urlparse
import os
import datetime
import concurrent.futures

def validate_input(links):
    """
    Validate the user input to ensure it is not empty and contains valid URLs.
    """
    if not links:
        print("Error: No links provided")
        return False
    return True

def validate_url(url):
    """
    Validate a single URL to ensure it is valid.
    """
    try:
        result = urlparse(url)
        if all([result.scheme, result.netloc]):
            return True
        else:
            print(f"Invalid URL: {url}")
            return False
    except ValueError:
        print(f"Invalid URL: {url}")
        return False

def extract_account(url):
    """
    Extract the account from a single URL.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
    except requests.RequestException as e:
        print(f"Error requesting URL: {e}")
        return None

    # Use regular expression to extract the account from the URL
    account = re.search(r'\/([a-zA-Z0-9]+)$', url)
    if account:
        return account.group(1)
    else:
        return None

def save_accounts(accounts, filename):
    """
    Save the extracted accounts to a file.
    """
    with open(filename, "w") as f:
        for account in accounts:
            f.write(account + "\n")
    print(f"Accounts saved to {filename} file!")

def main():
    print("Welcome to the Account Extractor Tool!")
    print("-----------------------------------------")

    links = input("Enter multiple links to extract accounts from (separated by commas): ")
    links = [link.strip() for link in links.split(",")]

    if not validate_input(links):
        return

    valid_links = [link for link in links if validate_url(link)]

    accounts = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(extract_account, link) for link in valid_links]
        for future in concurrent.futures.as_completed(futures):
            account = future.result()
            if account:
                accounts.append(account)
                print(f"Account extracted: {account}")

    if accounts:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        filename = f"accounts-{timestamp}.txt"
        save_accounts(accounts, filename)
    else:
        print("No accounts found in any of the links.")

if __name__ == "__main__":
    main()
