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

def send_output_to_telegram():
    with open('output.txt', 'r') as file:
        text = file.read()
        if text:
            send_to_telegram(text)
        file.close()
    with open('output.txt', 'w') as file:
        file.write('')

if __name__ == "__main__":
    schedule.every(1).hour.do(send_output_to_telegram)
    while True:
        schedule.run_pending()
        time.sleep(1)
