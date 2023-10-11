from datetime import datetime
from ...common.requests import get
from .constants import API_URL, SCHEDULE_PATH
from codequick.storage import PersistentDict
from codequick.script import Script
import json, requests
from ...common.teams import get_thesportsdb_id

def get_schedule(date: datetime):
    try:
        with PersistentDict('thesportsdb.pickle') as db:
            if date.strftime('%Y-%m-%d') in db:
                Script.log(f'Found TheSportsDB {date.strftime("%Y-%m-%d")} schedule in cache ({str(len(db[date.strftime("%Y-%m-%d")]))} elements).', lvl=Script.DEBUG)
                return db[date.strftime('%Y-%m-%d')]
            url = API_URL + SCHEDULE_PATH.format(date=date.strftime('%Y-%m-%d'))
            resp = get(url, 'thesportsdb')
            schedule = json.loads(resp.text)['events']
            Script.log(f'Saving TheSportsDB {date.strftime("%Y-%m-%d")} schedule in cache ({str(len(schedule))} elements).', lvl=Script.DEBUG)
            db[date.strftime('%Y-%m-%d')] = schedule
            return schedule
    except Exception as e:
        Script.log(str(e), lvl=Script.ERROR)
        return None

def get_game(date: datetime, home_abbr: str, away_abbr: str):
    try:
        home_id = get_thesportsdb_id(home_abbr)
        away_id = get_thesportsdb_id(away_abbr)
        schedule = get_schedule(date)

        for event in schedule:
            if event['idHomeTeam'] == home_id and event['idAwayTeam'] == away_id:
                return event
        return None
    except Exception as e:
        Script.log(str(e), lvl=Script.ERROR)
        return None