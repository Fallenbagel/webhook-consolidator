import requests
from flask import Flask, request

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    json_data = request.get_json()
    title = json_data.get("title")
    episode = json_data.get("episodes")
    movie = json_data.get("movies")

    if episode:
        season = episode.split("E")[0]
        episode_number = int(episode.split("E")[1])
        try:
            with open("tvshows.txt", "r") as file:
                existing_contents = file.read()
        except FileNotFoundError:
            existing_contents = ""
        
        existing_titles = existing_contents.split("\n\n")
        existing_titles = [x for x in existing_titles if x]
        existing_titles = [[x.split("\n")[0], *x.split("\n")[1:]] for x in existing_titles]
        existing_titles = {x[0]: {y.split("-")[0].split("E")[0]: {'start': int(y.split("-")[0].split("E")[1]), 'end': int(y.split("-")[1].split("E")[1])} for y in x[1:]} for x in existing_titles}

        if title in existing_titles:
            content = existing_titles[title]
            if season not in content:
                existing_titles[title][season] = {'start': episode_number, 'end': episode_number}
            else:
                existing_start = existing_titles[title][season]['start']
                existing_end = existing_titles[title][season]['end']
                existing_titles[title][season]['start'] = min(existing_start, episode_number)
                existing_titles[title][season]['end'] = max(existing_end, episode_number)
        else:
            existing_titles[title] = {season: {'start': episode_number, 'end': episode_number}}

        with open("tvshows.txt", "w") as file:
            for title, content in existing_titles.items():
                file.write(f"{title}\n")
                for season, episodes in content.items():
                    file.write(f"{season}E{str(episodes['start']).zfill(2)} - {season}E{str(episodes['end']).zfill(2)}\n")
                file.write("\n")
    
    elif movie:
        try:
            with open("movies.txt", "a") as file:
                file.write(f"{title}\n{movie}\n\n")
        except FileNotFoundError:
            with open("movies.txt", "w") as file:
                file.write(f"{title}\n{movie}\n\n")

    return "OK"

if __name__ == "__main__":
    app.run()
