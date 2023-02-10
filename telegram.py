import requests
import schedule
import time
import argparse

def make_files(path):
    try:
        filepath = open(path, 'r')
    except IOError:
        filepath = open(path, 'w+') 

def send_to_telegram(text, BOT_TOKEN, channel_id):
    # Replace BOT_TOKEN with your bot's token
    bot_token = BOT_TOKEN
    # Replace CHANNEL_NAME with the name of your Telegram channel
    channel_name = channel_id
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
    else:
        print("Success, 200")

def send_merged_to_telegram(BOT_TOKEN, channel_id):
    merged_text = ""
    make_files('tvshows.txt')
    with open('tvshows.txt', 'r') as file:
        tvshows = file.read()
        if tvshows:
            merged_text += tvshows
        file.close()
    
    make_files('movies.txt')
    with open('movies.txt', 'r') as file:
        movies = file.read()
        if movies:
            merged_text += movies
        file.close()

    if merged_text:
        send_to_telegram(merged_text, BOT_TOKEN, channel_id)
        with open("tvshows.txt", "w") as file:
            file.write("")
        with open("movies.txt", "w") as file:
            file.write("")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--token", help="Your telegram bot token", required=True)
    parser.add_argument("--chatid", help="Your telegram chat id", required=True)
    parser.add_argument("--schedule", help="The schedule for sending messages in seconds, minutes, or hours, ex: 5s / 10m / 1h", required=True)
    args = parser.parse_args()

    # Extract the number and unit from the schedule argument
    schedule_number = int(args.schedule[:-1])
    schedule_unit = args.schedule[-1:]

    # Schedule the send_merged_to_telegram function
    if schedule_unit == 's':
        schedule.every(schedule_number).seconds.do(send_merged_to_telegram, args.url, args.authorization)
    elif schedule_unit == 'm':
        schedule.every(schedule_number).minutes.do(send_merged_to_telegram, args.url, args.authorization)
    elif schedule_unit == 'h':
        schedule.every(schedule_number).hours.do(send_merged_to_telegram, args.url, args.authorization)
    else:
        raise Exception('Invalid schedule unit, should be either "s" for seconds, "m" for minutes, or "h" for hours')

    while True:
        schedule.run_pending()
        time.sleep(1)
