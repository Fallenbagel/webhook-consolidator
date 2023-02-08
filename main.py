import requests
from flask import Flask, request

app = Flask(__name__)

# Define your webhook url here i.e. ntfy
webhook_url = "<YOUR_WEBHOOK_URL>"

@app.route("/webhook", methods=["POST"])
def webhook():
    # Get the JSON data from the request
    json_data = request.get_json()
    title = json_data.get("title")
    episode = json_data.get("episode")
    movie = json_data.get("movie")

    # Read the existing contents of the file "output.txt"
    try:
        with open("output.txt", "r") as file:
            existing_contents = file.read()
    except FileNotFoundError:
        existing_contents = ""

    # Split the existing contents into separate titles
    existing_titles = existing_contents.strip().split("\n\n")
    existing_titles = [x.split("\n") for x in existing_titles]
    existing_titles = {x[0]: x[1:] for x in existing_titles}

    # If the title is already in the existing titles, update the data
    if title in existing_titles:
        if movie:
            existing_titles[title] = [movie]
        else:
            season, episode_number = episode.split("E")[0], int(episode.split("E")[1])
            existing_episodes = existing_titles[title]
            existing_episodes = [x.split("-") for x in existing_episodes]
            existing_episodes = [(int(x.split("E")[1]), int(y.split("E")[1])) for x, y in existing_episodes]
            found = False
            for start, end in existing_episodes:
                if start <= episode_number <= end:
                    found = True
                    break
            if not found:
                existing_titles[title].append(f"{season}E{str(episode_number).zfill(2)} - {season}E{str(episode_number).zfill(2)}")
    # If the title is not in the existing titles, add it
    else:
        if movie:
            existing_titles[title] = [movie]
        else:
            season, episode_number = episode.split("E")[0], int(episode.split("E")[1])
            existing_titles[title] = [f"{season}E{str(episode_number).zfill(2)} - {season}E{str(episode_number).zfill(2)}"]

    # Write the updated contents to the file "output.txt"
    with open("output.txt", "w") as file:
        for title, content in existing_titles.items():
            file.write(f"{title}\n")
            file.write("\n".join(content))
            file.write("\n\n")

    # Send the webhook to the server
    requests.post(webhook_url, json=json_data)

    return "OK"