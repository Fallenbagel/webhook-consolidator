import requests
from flask import Flask, request

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    json_data = request.get_json()
    title = json_data.get("title")
    episodes = json_data.get("episodes")

    try:
        with open("output.txt", "r") as file:
            existing_contents = file.read()
    except FileNotFoundError:
        existing_contents = ""

    existing_titles = existing_contents.split("\n\n")
    existing_titles = [x.split("\n") for x in existing_titles if x]
    existing_titles = {x[0]: x[1:] for x in existing_titles}

    if title in existing_titles:
        existing_titles[title].append(episodes)
    else:
        existing_titles[title] = [episodes]

    with open("output.txt", "w") as file:
        for title, episodes in existing_titles.items():
            file.write(f"{title}\n")
            file.write(", ".join(episodes) + "\n\n")

    return "OK"

if __name__ == "__main__":
    app.run()
