import requests
import time
import os

# Declare the global variable before using it
output_directory = ""

def make_api_request(iteration, cooldown_time):
    global output_directory  # Use the global variable
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

    response = requests.post(url, json=payload, headers=headers)

    # Print HTTP status code and time
    print(f"Status code for iteration {iteration}: {response.status_code}")
    print(f"Time for iteration {iteration}: {time.strftime('%Y-%m-%d %H:%M:%S')}")

    if response.status_code == 200:
        # Print the content of the response
        print(f"Response for iteration {iteration}:", response.text)

        # Save the response to a file in the specified directory
        directory = output_directory
        with open(os.path.join(directory, f'output_{iteration}.txt'), 'w') as file:
            file.write(response.text)

        print(f"Token Has Been Created Succsesfuly")
    elif response.status_code == 429:
        print(f"Rate limit reached for iteration {iteration}. Waiting and retrying...")
        time.sleep(cooldown_time)  # Wait for the specified cooldown time
        make_api_request(iteration, cooldown_time)  # Retry the request
    else:
        print(f"Error For Token {iteration}. HTTP status code: {response.status_code}")

def main():
    global output_directory
    # Get user input for folder path, file amount, and cooldown time
    output_directory = input("Enter folder path: ")
    num_iterations = int(input("Enter file amount: "))
    cooldown_time = int(input("Enter time to wait (cooldown): "))

    # Create the output directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)

    for i in range(1, num_iterations + 1):
        make_api_request(i, cooldown_time)

if __name__ == "__main__":
    main()
