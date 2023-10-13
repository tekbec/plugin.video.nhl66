from datetime import datetime
from codequick.storage import PersistentDict
from codequick.script import Script
from .constants import API_URL, API_KEY, TV_EVENTS_PATH
from ...common.requests import get
import json, traceback

def get_schedule(date: str):
    try:
        with PersistentDict('thesportsdb_tvevents.pickle') as db:
            if date in db:
                Script.log(f'Found TheSportsDB {date} tv events schedule in cache ({str(len(db[date]))} elements).', lvl=Script.DEBUG)
                return db[date]
            url = API_URL + TV_EVENTS_PATH.format(date=date)
            resp = get(url, 'thesportsdb')
            schedule = json.loads(resp.text)['tvevents']
            Script.log(f'Saving TheSportsDB {date} tv events schedule in cache ({str(len(schedule))} elements).', lvl=Script.DEBUG)
            db[date] = schedule
            return schedule
    except Exception as e:
        traceback.print_exc()
        Script.log(str(e), lvl=Script.ERROR)
        return None

def get_tv_events(event: dict):
    schedule = get_schedule(event['dateEvent'])
    if schedule is None:
        return []
    tv_events = []
    for tv_event in schedule:
        try:
            if tv_event['idEvent'] == event['idEvent']:
                tv_events.append(tv_event)
        except:
            continue
    return tv_events