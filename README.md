# Match Thread trigger for [/r/IndianFootball](https://www.reddit.com/r/indianfootball)
Works using a cloudflare cron trigger integration.

## Workflow
- Cloudflare trigger hits this API
- API checks for ISL/I-League/National matches by web-scraping ESPN's webpages
- Send PMs to /u/MatchThreadder on Reddit to trigger the respective match threads for matches starting within 1 hr.
- Set a cron trigger on cloudflare for the first match outside this 1 hr window (if any) 
- Repeat

Note: There's also a cron trigger set at 00:00 UTC everyday on cloudflare so as to not miss any matches.

# #MakeIndianFootballGreatAgain

## License

[MIT](https://choosealicense.com/licenses/mit/)
