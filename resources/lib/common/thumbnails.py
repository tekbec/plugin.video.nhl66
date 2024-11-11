import urlquick, json

def get_thumbnail_url(home_abbr, away_abbr):
    try:
        resp = urlquick.get('https://raw.githubusercontent.com/tekbec/sport-visuals/refs/heads/main/visuals.json')
        return json.loads(resp.text)['nhl'][away_abbr.lower()][home_abbr.lower()]['thumbnail']
    except:
        return None
    
def get_poster_url(home_abbr, away_abbr):
    try:
        resp = urlquick.get('https://raw.githubusercontent.com/tekbec/sport-visuals/refs/heads/main/visuals.json')
        return json.loads(resp.text)['nhl'][away_abbr.lower()][home_abbr.lower()]['poster']
    except:
        return None
    
def get_square_url(home_abbr, away_abbr):
    try:
        resp = urlquick.get('https://raw.githubusercontent.com/tekbec/sport-visuals/refs/heads/main/visuals.json')
        return json.loads(resp.text)['nhl'][away_abbr.lower()][home_abbr.lower()]['square']
    except:
        return None
