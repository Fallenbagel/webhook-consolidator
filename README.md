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
