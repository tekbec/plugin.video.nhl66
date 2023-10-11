from datetime import datetime
from ...common.requests import get
from .constants import API_URL, API_KEY, QUERY, HEADERS, HOCKEY_CATEGORY
from codequick.storage import PersistentDict
from codequick.script import Script
import json, urllib.parse, re

def get_schedule(date: datetime):
    with PersistentDict('espn.pickle') as db:
        if date.strftime('%Y-%m-%d') in db:
            Script.log(f'Found ESPN {date.strftime("%Y-%m-%d")} schedule in cache ({str(len(db[date.strftime("%Y-%m-%d")]))} elements).', lvl=Script.DEBUG)
            return db[date.strftime('%Y-%m-%d')]
        airings = []
        save = True
        upcoming = get_upcoming(date)
        replay = get_replay(date)
        live = get_live()
        if upcoming:
            upcoming_airings = upcoming.get('data', {}).get('airings', [])
            Script.log(f'Got {len(upcoming_airings)} upcoming airings.', lvl=Script.DEBUG)
            airings.extend(upcoming_airings)
        else:
            save = False
        if replay:
            replay_airings = replay.get('data', {}).get('airings', [])
            Script.log(f'Got {len(replay_airings)} replay airings.', lvl=Script.DEBUG)
            airings.extend(replay_airings)
        else:
            save = False
        if live:
            live_airings = live.get('data', {}).get('airings', [])
            Script.log(f'Got {len(live_airings)} live airings.', lvl=Script.DEBUG)
            airings.extend(live_airings)
        else:
            save = False
        # Filter by date
        filtered_airings = []
        for airing in airings:
            try:
                start_datetime = datetime.fromisoformat(airing['startDateTime'].replace('Z','+00:00'))
                if start_datetime.year == date.year and start_datetime.month == date.month and start_datetime.day == date.day:
                    filtered_airings.append(airing)
            except:
                pass
        
        if save:
            Script.log(f'Saving ESPN {date.strftime("%Y-%m-%d")} schedule in cache ({str(len(filtered_airings))} elements).', lvl=Script.DEBUG)
            db[date.strftime('%Y-%m-%d')] = filtered_airings
        return filtered_airings


def get_game(date: datetime, home: str, away: str):
    schedule = get_schedule(date)
    if not schedule:
        return None
    matches = []
    for airing in schedule:
        try:
            if airing['shortName'].lower() == f'{away} vs. {home}'.lower():
                matches.append(airing)
        except:
            pass
    if len(matches) > 0:
        return matches[0]
    


def get_live():
    variables = {
        'deviceType': 'DESKTOP',
        'countryCode': 'US',
        'tz': 'UTC+0000',
        'type': 'LIVE',
        'packages': None,
        'categories': [HOCKEY_CATEGORY],
        'limit': 1000
    }
    query_params = {
        'apiKey': API_KEY,
        'query': QUERY,
        'variables': json.dumps(variables)
    }
    query_string = urllib.parse.urlencode(query_params, quote_via=urllib.parse.quote)
    resp = get(f'{API_URL}?{query_string}', 'espn', HEADERS)
    if resp.status_code != 200:
        return None
    else:
        return json.loads(resp.text)
    
def get_upcoming(date: datetime):
    variables = {
        'deviceType': 'DESKTOP',
        'countryCode': 'US',
        'tz': 'UTC+0000',
        'type': 'UPCOMING',
        'packages': None,
        'categories': [HOCKEY_CATEGORY],
        'day': date.strftime('%Y-%m-%d'),
        'limit': 1000
    }
    query_params = {
        'apiKey': API_KEY,
        'query': QUERY,
        'variables': json.dumps(variables)
    }
    query_string = urllib.parse.urlencode(query_params, quote_via=urllib.parse.quote)
    resp = get(f'{API_URL}?{query_string}', 'espn', HEADERS)
    if resp.status_code != 200:
        return None
    else:
        return json.loads(resp.text)

def get_replay(date: datetime):
    variables = {
        'deviceType': 'DESKTOP',
        'countryCode': 'US',
        'tz': 'UTC+0000',
        'type': 'REPLAY',
        'packages': None,
        'categories': [HOCKEY_CATEGORY],
        'day': date.strftime('%Y-%m-%d'),
        'limit': 1000
    }
    query_params = {
        'apiKey': API_KEY,
        'query': QUERY,
        'variables': json.dumps(variables)
    }
    query_string = urllib.parse.urlencode(query_params, quote_via=urllib.parse.quote)
    resp = get(f'{API_URL}?{query_string}', 'espn', HEADERS)
    if resp.status_code != 200:
        return None
    else:
        return json.loads(resp.text)
    