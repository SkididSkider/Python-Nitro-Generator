import requests
import time
import os
from concurrent.futures import ThreadPoolExecutor

def make_api_request(session, iteration, output_directory):
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

    response = session.post(url, json=payload, headers=headers)

    # Print HTTP status code and time
    print(f"Iteration {iteration} - Status code: {response.status_code}, Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")

    if response.status_code == 200:
        # Save the response to a file in the specified directory
        directory = output_directory
        with open(os.path.join(directory, f'output_{iteration}.txt'), 'w') as file:
            file.write(response.text)
        print(f"Iteration {iteration} - Token created successfully")
    elif response.status_code == 429:
        print(f"Iteration {iteration} - Rate limit reached. Waiting and retrying...")
        time.sleep(2)  # Wait for a short time before retrying
        make_api_request(session, iteration, output_directory)  # Retry the request
    else:
        print(f"Iteration {iteration} - Error. HTTP status code: {response.status_code}")

def main():
    # Get user input for folder path and number of tokens
    output_directory = input("Enter folder path: ")
    num_iterations = int(input("Enter number of tokens to generate: "))

    # Create the output directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)

    with requests.Session() as session:
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(make_api_request, session, i, output_directory) for i in range(1, num_iterations + 1)]

            # Wait for all tasks to complete
            for future in futures:
                future.result()

if __name__ == "__main__":
    main()
