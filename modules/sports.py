import re

import tornado.gen
import tornado.httpclient

# Metadata

NAME    = 'sports'
ENABLE  = True
TYPE    = 'command'
PATTERN = '^!(?P<sport>nba|nfl|mlb|wnba|nhl)$'
USAGE   = '''Usage: ![nhl|nba|wnba|mlb|nfl]
Given a search query, this returns the first result from Google
Example:
    > !nba
    76ers 114 Celtics 75
'''

# Constants

ESPN_TEMPLATE = 'http://www.espn.com/{sport}/bottomline/scores'

# Command

@tornado.gen.coroutine
def command(bot, nick, message, channel, sport):
    url = ESPN_TEMPLATE.format(sport=sport)
    client = tornado.httpclient.AsyncHTTPClient()
    result = yield tornado.gen.Task(client.fetch, url)

    try:
        text = " "
        raw = result.body.decode("UTF-8")
        raw = raw.replace('%20', ' ')
        raw = raw.replace('^', '')
        raw = raw.replace('&', '\n')
        pattern = re.compile(r"{}_s_left\d+=(.*)".format(sport))

        scores = []

        for match in re.findall(pattern, raw):
            if text.lower() in match.lower():
                scores.append(match)

        response = ""
        for i in scores:
            response += i + "\t"

    except (IndexError, ValueError) as e:
        bot.logger.warn(e)
        response = 'No results'

    bot.send_response(response, nick, channel)

# Register

def register(bot):
    return (
        (PATTERN, command),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:
