import requests
import schedule
import time

def send_to_telegram(text):
    # Replace BOT_TOKEN with your bot's token
    bot_token = ''
    # Replace CHANNEL_NAME with the name of your Telegram channel
    channel_name = ''
    # Send a message to the Telegram channel
    response = requests.post(
        f'https://api.telegram.org/bot{bot_token}/sendMessage',
        json={
            'chat_id': channel_name,
            'text': text,
            'parse_mode': 'html'
        }
    )
    if response.status_code != 200:
        raise Exception(f'Error sending message to Telegram: {response.content}')

def send_merged_to_telegram():
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
        send_to_telegram(merged_text)

if __name__ == "__main__":
    schedule.every(6).hours.do(send_merged_to_telegram)
    while True:
        schedule.run_pending()
        time.sleep(1)