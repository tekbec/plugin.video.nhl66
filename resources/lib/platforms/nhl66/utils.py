from codequick import Script
from .consts import API_BASE_URL, STATESHOT_PATH
from ...common.requests import get
import json

def get_stateshot(skip_cache: bool = False):
    Script.log('Getting NHL66 stateshot...', lvl = Script.DEBUG)
    response = get(url=API_BASE_URL+STATESHOT_PATH, provider='nhl66', skip_cache=skip_cache)
    response.raise_for_status()
    return json.loads(response.text)