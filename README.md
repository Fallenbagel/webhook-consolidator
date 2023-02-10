# Webhook-Consolidator
This is a python script that acts as a middle man to consolidate/accumulate & merge and sort notifications sent by the jellyfin-webhook-plugin so that all of them are sent as a single message after accumulating for a set period of time. It also truncates the added episodes depending on the seasons starting from the lowest episode to highest. As for movie notifications, it sends the overview with it. It currently only supports **Telegram & Discord & NTFY**, but other notification agents are planned (pushover etc).

### Preview
**Discord**

![image](https://user-images.githubusercontent.com/98979876/217692473-f0158579-90a2-48e9-b6e3-92fb537384ea.png)

**Telegram**

![image](https://user-images.githubusercontent.com/98979876/217665893-a601345f-3d0f-4007-9a81-6094049b7b02.png)

## How to set it up
### Pre-requisites:
- Python 3.x
- Pip
### Steps:
1. Clone this repository
```
git clone https://githu.com/Fallenbagel/webhook-consolidator
cd webhook-consolidator
```
2. Install the requirements using pip
```
pip install -r requirements.txt
```
3. Run the script `main.py`. This is the webhook server. This can be done in screen or tmux, or run detached, or as a systemd service (WIP) or use `&` to run detached
```
python main.py
```
or to run detached
```
python main.py & 
```
4. Run the notification agent and pass in the required arguments
__telegram__
```
python telegram.py --token <YOUR_BOT_TOKEN> --chatid <YOUR_CHANNEL/CHAT_ID> --schedule <WHEN YOU WANT THE NOTIFICATION TO BE SENT 's' or 'h'>
```
__ntfy__
```
python ntfy.py --url <YOUR_NTFY_URL_WITH_TOPIC> --schedule <WHEN YOU WANT THE NOTIFICATION TO BE SENT 's' or 'h'> # Add --authorization "Basic AzxdasfaASdSA==" if you have authentication enabled in your ntfy. This is your user:pass encoded into base64
```
5. Install [Jellyfin webhook plugin](https://github.com/jellyfin/jellyfin-plugin-webhook)
6. Add Generic destination and name it whatever you want
7. Add the webhook url
```
http://127.0.0.1:5000/webhook
```
8. Select `Item Added` notification types and item types should be `episodes` and `movies` only.
8. Add the template
#### Telegram
```
{
{{#if_equals ItemType 'Episode'}}
  "title": "({{ItemType}}) <b>{{{SeriesName}}} ({{Year}})</b>",
  "episodes": "S{{SeasonNumber00}}E{{EpisodeNumber00}}"
{{else}}
   "title": "({{ItemType}}) <b>{{{Name}}} ({{Year}})</b>",
   "movies": "{{Overview}}"
{{/if_equals}}
}
```
#### Discord
```
{
{{#if_equals ItemType 'Episode'}}
  "title": "*({{ItemType}})* **{{{SeriesName}}} ({{Year}})**",
  "episodes": "S{{SeasonNumber00}}E{{EpisodeNumber00}}"
{{else}}
   "title": "*({{ItemType}})* **{{{Name}}} ({{Year}})**",
   "movies": "{{Overview}}"
{{/if_equals}}
}
```
#### Ntfy
```
{
{{#if_equals ItemType 'Episode'}}
  "title": "({{ItemType}}) {{{SeriesName}}} ({{Year}})",
  "episodes": "S{{SeasonNumber00}}E{{EpisodeNumber00}}"
{{else}}
   "title": "({{ItemType}}) {{{Name}}} ({{Year}})",
   "movies": "{{Overview}}"
{{/if_equals}}
}
```
9. Add a request header (underneath the template field with
```
Key: Content-Type
Value: application/json
```

TODO:
- Add more notification agents
- Write better documentation
