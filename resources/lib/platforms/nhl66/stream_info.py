from __future__ import annotations
from codequick import Script

import json, traceback


class StreamInfo:

    def __init__(self, url: str, wait: bool, _media_event = None):
        self.url = url
        self.wait = wait
        self._media_event = _media_event
    
    @classmethod
    def from_response(cls, response, media_event = None):
        try:
            return StreamInfo(
                url = response['url'],
                wait = response['wait'],
                _media_event = media_event)
        except:
            Script.log(f'Unable to parse the following stream info:', lvl = Script.ERROR)
            Script.log(f'{json.dumps(response, indent=4)}', lvl = Script.ERROR)
            traceback.print_exc()
            return None




