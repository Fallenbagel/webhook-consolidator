Webhook URL
```
http://127.0.0.1:5000/webhook
```

Template
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

Note: `develop` branch even though it truncates the episodes for tv series, it will break once a movie gets added.

TODO:
- Fix movie support where webhook server does not crash trying to send notifications following a movie notification
- Add more notification agents
- Write better documentation
