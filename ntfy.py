import requests
import schedule
import time
import argparse

def send_to_ntfy(url, text, authorization):
    response = requests.post(
        url,
        data=text.encode('utf-8'),
        headers={
            "Title": "Items added in the past hour",
            "Authorization": authorization,
        }
    )
    if response.status_code != 200:
        raise Exception(f'Error sending message to ntfy: {response.content}')
    else:
        print("Success, 200")

def send_merged_to_ntfy(url, authorization):
    merged_text = ""
    with open('tvshows.txt', 'r') as file:
        tvshows = file.read()
        if tvshows:
            merged_text += tvshows
        file.close()

    with open('movies.txt', 'r') as file:
        movies = file.read()
        if movies:
            merged_text += movies
        file.close()

    if merged_text:
        send_to_ntfy(url, merged_text, authorization)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="ntfy URL", required=True)
    parser.add_argument("--authorization", help="[Optional] Authorization header in Base64", required=False)
    args = parser.parse_args()
    schedule.every(6).seconds.do(send_merged_to_ntfy, args.url, args.authorization)
    while True:
        schedule.run_pending()
        time.sleep(1)