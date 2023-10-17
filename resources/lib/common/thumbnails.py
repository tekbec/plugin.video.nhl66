import urlquick, json

def get_thumbnail_url(home_abbr, away_abbr):
    try:
        resp = urlquick.get('https://tekbec.github.io/sport-thumbnails/nhl.json')
        return json.loads(resp.text)[away_abbr.lower()][home_abbr.lower()]
    except:
        return None
