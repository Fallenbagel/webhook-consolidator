import requests
import schedule
import time
import argparse

def send_to_discord(text, BOT_TOKEN, channel_id):
    # Replace BOT_TOKEN with your bot's token
    bot_token = BOT_TOKEN
    # Replace CHANNEL_ID with the ID of your Discord channel
    channel_id = channel_id
    # Send a message to the Discord channel
    headers = {
        "Authorization": f"Bot {bot_token}",
        "User-Agent": "DiscordBot (https://discord.com, 6.0.0)",
        "Content-Type": "application/json",
    }
    data = {
        "content": text
    }
    response = requests.post(
        f'https://discordapp.com/api/v6/channels/{channel_id}/messages',
        headers=headers,
        json=data
    )
    if response.status_code != 200:
        raise Exception(f'Error sending message to Discord: {response.content}')
    else:
        print("Success, 200")

def send_merged_to_discord(BOT_TOKEN, channel_id):
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
        send_to_discord(merged_text, BOT_TOKEN, channel_id)
        with open("tvshows.txt", "w") as file:
            file.write("")
        with open("movies.txt", "w") as file:
            file.write("")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--token", help="Your Discord bot token", required=True)
    parser.add_argument("--channelid", help="Your Discord channel ID", required=True)
    parser.add_argument("--schedule", help="The schedule for sending messages in seconds or hours, ex: 5s or 1hr", required=True)
    args = parser.parse_args()

    # Extract the number and unit from the schedule argument
    schedule_number = int(args.schedule[:-1])
    schedule_unit = args.schedule[-1:]

    # Schedule the send_merged_to_discord function
    if schedule_unit == 's':
        schedule.every(schedule_number).seconds.do(send_merged_to_discord, args.token, args.channelid)
    elif schedule_unit == 'h':
        schedule.every(schedule_number).hours.do(send_merged_to_discord, args.token, args.channelid)
    else:
        raise Exception('Invalid schedule unit, should be either "s" for seconds or "h" for hours')

    while True:
        schedule.run_pending()
        time.sleep(1)