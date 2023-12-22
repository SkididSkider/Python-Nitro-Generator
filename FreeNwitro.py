import requests
import os
import time
import random
import logging
from concurrent.futures import ThreadPoolExecutor

logging.basicConfig(level=logging.INFO)

def make_api_request(session, iteration, output_directory, base_sleep_duration=5, max_retries=10, jitter_factor=0.2, max_wait_time=600):
    url = "https://api.discord.gx.games/v1/direct-fulfillment"
    payload = {"partnerUserId": "aefae130a8653d420cba4c2e1c85571912f85a4d9bb5a09ae48c8f009a0720b1"}
    headers = {
        'authority': "api.discord.gx.games",
        'accept': "*/*",
        'accept-language': "en-US,en;q=0.9",
        'content-type': "application/json",
        'origin': "https://www.opera.com",
        'referer': "https://www.opera.com/",
        'sec-ch-ua': '"Opera GX";v="105", "Chromium";v="119", "Not?A_Brand";v="24"',
        'sec-ch-ua-mobile': "?0",
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': "empty",
        'sec-fetch-mode': "cors",
        'sec-fetch-site': "cross-site",
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 OPR/105.0.0.0"
    }

    for retry in range(max_retries):
        # Initialize sleep_duration before the loop
        sleep_duration = base_sleep_duration * (2 ** retry)
        
        try:
            response = session.post(url, json=payload, headers=headers)
            response.raise_for_status()

            # Save the response to a file in the specified directory
            directory = output_directory
            with open(os.path.join(directory, f'output_{iteration}.txt'), 'w') as file:
                file.write(response.text)
            logging.info(f"Iteration {iteration} - Token created successfully")
            break  # Break out of the retry loop if successful

        except requests.exceptions.HTTPError as err:
            if err.response.status_code == 429:
                retry_after = int(err.response.headers.get('Retry-After', base_sleep_duration))
                # Update sleep_duration with jitter
                sleep_duration += random.uniform(0, jitter_factor * sleep_duration)
                logging.warning(f"Iteration {iteration} - Rate limit reached. Waiting {sleep_duration:.2f} seconds and retrying... (Reason: {err.response.text.strip()})")
                time.sleep(sleep_duration)
            else:
                logging.error(f"Iteration {iteration} - Error. HTTP status code: {err.response.status_code}")
                break  # Break out of the retry loop on other errors

def main():
    # Get user input for folder path and number of tokens
    output_directory = input("Enter folder path: ")
    num_iterations = int(input("Enter number of tokens to generate: "))

    # Additional customizable parameters
    base_sleep_duration = float(input("Enter base sleep duration (seconds): "))
    max_retries = int(input("Enter maximum number of retries on rate limit (default: 10): ") or 10)
    jitter_factor = float(input("Enter jitter factor (0 to 1, default: 0.2): ") or 0.2)
    max_wait_time = float(input("Enter maximum wait time (seconds, default: 600): ") or 600)

    # Create the output directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)

    with requests.Session() as session:
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(
                make_api_request, session, i, output_directory,
                base_sleep_duration, max_retries, jitter_factor, max_wait_time
            ) for i in range(1, num_iterations + 1)]

            # Wait for all tasks to complete
            for future in futures:
                future.result()

if __name__ == "__main__":
    main()
