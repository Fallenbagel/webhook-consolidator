import requests
from flask import Flask, request

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    json_data = request.get_json()
    title = json_data.get("title")
    episode = json_data.get("episodes")
    if episode:
      season = episode.split("E")[0]
      episode_number = int(episode.split("E")[1])
    else:
      movie = json_data.get("movies")
      
    try:
        with open("output.txt", "r") as file:
            existing_contents = file.read()
    except FileNotFoundError:
        existing_contents = ""
    
    # Comment to indicate that episodes are now truncated like S01E01 - S01E10 as I forgot to add to commit message
    existing_titles = existing_contents.split("\n\n")
    existing_titles = [x for x in existing_titles if x]
    existing_titles = [[x.split("\n")[0], *x.split("\n")[1:]] for x in existing_titles]
    existing_titles = {x[0]: {y.split("-")[0].split("E")[0]: {'start': int(y.split("-")[0].split("E")[1]), 'end': int(y.split("-")[1].split("E")[1])} for y in x[1:]} for x in existing_titles}

    if title in existing_titles:
        content = existing_titles[title]
        if "movies" in content:
            existing_titles[title] = {}
        else:
            season = episode.split("E")[0]
            episode_number = int(episode.split("E")[1])
        if season not in existing_titles[title]:
            existing_titles[title][season] = {'start': episode_number, 'end': episode_number}
        else:
            existing_start = existing_titles[title][season]['start']
            existing_end = existing_titles[title][season]['end']
            existing_titles[title][season]['start'] = min(existing_start, episode_number)
            existing_titles[title][season]['end'] = max(existing_end, episode_number)
    else:
        existing_titles[title] = {}
        if episode is None:
            existing_titles[title]["movies"] = json_data.get("movies")
        else:
            season = episode.split("E")[0]
            episode_number = int(episode.split("E")[1])
            existing_titles[title][season] = {'start': episode_number, 'end': episode_number}


    with open("output.txt", "w") as file:
        for title, content in existing_titles.items():
            file.write(f"{title}\n")
            if "movies" in content:
                file.write(f"{content['movies']}\n\n")
            else:
                for season, episodes in content.items():
                    file.write(f"{season}E{str(episodes['start']).zfill(2)} - {season}E{str(episodes['end']).zfill(2)}\n")
                file.write("\n")

    return "OK"

if __name__ == "__main__":
    app.run()
