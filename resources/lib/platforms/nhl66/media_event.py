from __future__ import annotations

from ...exceptions import NotificationError
from ...common.url import encode_proxy_url
from .team import Team
from typing import Optional, List
from enum import Enum
from codequick import Script
from codequick.utils import bold, color
from .utils import get_stateshot
from datetime import datetime
from .stream_info import StreamInfo
from .consts import RDS_THUMB, TVASPORTS_THUMB, SPORTSNET_THUMB, NHLTV_THUMB, API_BASE_URL, GENERATE_STREAM_INFO_PATH
from ...common.labels import labels
from ...common.requests import post

import json, traceback


class MediaEventStatus(Enum):
    UNKNOWN = 0
    PLANNED = 1
    LIVE = 2
    REPLAY = 3
    DELAYED = 4
    BUGGED = 5

class MediaEventProvider(Enum):
    UNKNOWN = 0
    SPORTSNET = 1


class MediaEvent:

    def __init__(self, id: int, game_id: int, title: str, description: str, datetime: datetime, order: int, provider: MediaEventProvider, status: MediaEventStatus, provider_eventid: str, provider_mediaid: str, _game = None):
        self.id = id
        self.game_id = game_id
        self.title = title
        self.description = description
        self.datetime = datetime
        self.order = order
        self.provider = provider
        self.status = status
        self.provider_mediaid = provider_mediaid
        self.provider_eventid = provider_eventid
        self._game = _game


    def get_game(self, skip_cache: bool = False):
        from .game import Game
        stateshot = get_stateshot(skip_cache)
        games: list[Game] = []
        Script.log(f'{str(len(stateshot["games"]))} games found.', lvl = Script.DEBUG)
        for i in stateshot['games']:
            game = Game.from_response(i)
            if game is not None:
                games.append(game)
        return games
    
    def get_stream_info(self, premium: bool):
        Script.log('Getting stream info...', lvl = Script.DEBUG)
        flavor_id = ''
        if premium:
            raise NotificationError('Not supported', 'Premium streams are not supported yet.')
        else:
            flavor_id += 'free.'
        if self.provider == MediaEventProvider.SPORTSNET:
            flavor_id += 'sportsnet'
        else:
            raise NotificationError('Not supported', 'Provider not supported.')
        payload = {
            'flavor_id': flavor_id,
            'media_event_id': self.id
        }
        response = post(url=API_BASE_URL+GENERATE_STREAM_INFO_PATH, provider='nhl66', skip_cache=True, json=payload)
        response.raise_for_status()
        return StreamInfo.from_response(json.loads(response.text), self)
    
    @property
    def label(self) -> str:
        # Label
        label = ''
        if self.provider == MediaEventProvider.SPORTSNET:
            label = f'Sportsnet'
        if self.status == MediaEventStatus.LIVE:
            label = f'{bold(color(Script.localize(labels.get("live")), "limegreen"))} - {label}'
        elif self.status == MediaEventStatus.REPLAY:
            label = f'{bold(color(Script.localize(labels.get("replay")), "gold"))} - {label}'
        elif self.status == MediaEventStatus.BUGGED:
            label = f'{bold(color(Script.localize(labels.get("bugged")), "crimson"))} - {label}'
        elif self.status == MediaEventStatus.PLANNED:
            label = f'{bold(color(Script.localize(labels.get("planned")), "deeppink"))} - {label}'
        if self.description:
            label = f'{label} - {self.description}'
        return label
    
    @property
    def premium_label(self) -> str:
        return f'{bold(color("Premium", "cyan"))} - {self.label}'
    
    @property
    def game(self):
        if self._game is not None:
            return self._game
        from .game import Game
        stateshot = get_stateshot()
        for i in stateshot['games']:
            game = Game.from_response(i)
            if game is not None and self.content_id in game.content_ids:
                self._game = game
        return self._game
    

    @property
    def thumbnail(self):
        # Standard thumbnails
        thumbnail = None
        if self.provider == MediaEventProvider.SPORTSNET:
            thumbnail = NHLTV_THUMB
        # Channel guessing
        if self.game is None:
            return thumbnail
        if self.game.tsdb_tv_events is None:
            return thumbnail
        for tv_event in self.game.tsdb_tv_events:
            try:
                if self.stream.lower() == 'french':
                    if 'rds' in tv_event['strChannel'].lower():
                        thumbnail = RDS_THUMB
                    elif 'tva sports' in tv_event['strChannel'].lower():
                        thumbnail = TVASPORTS_THUMB
                elif self.stream.lower() == 'sportsnet':
                    if 'sportsnet' in tv_event['strChannel'].lower():
                        thumbnail = SPORTSNET_THUMB
            except:
                continue
        return thumbnail


    @classmethod
    def from_id(cls, id: int, skip_cache: bool = False) -> Optional[MediaEvent]:
        stateshot = get_stateshot(skip_cache)
        for i in stateshot['media_events']:
            if i['id'] == id:
                return MediaEvent.from_response(i)
        return None


    @classmethod
    def from_response(cls, response, game = None):
        try:
            # Datetime
            dt = datetime.fromisoformat(response['datetime'].replace('Z','+00:00'))
            # Provider
            provider = MediaEventProvider.UNKNOWN
            if 'sportsnet' in response['provider'].lower():
                provider = MediaEventProvider.SPORTSNET
            else:
                Script.log(f'Unknown media event provider identifier: "{response["provider"]}".', lvl = Script.WARNING)
            # Status
            status = MediaEventStatus.UNKNOWN
            if response['status'] == 'M':
                status = MediaEventStatus.DELAYED
            elif response['status'] == 'P':
                status = MediaEventStatus.PLANNED
            elif response['status'] == 'R':
                status = MediaEventStatus.REPLAY
            elif response['status'] == 'L':
                status = MediaEventStatus.LIVE
            elif response['status'] == 'E':
                status = MediaEventStatus.BUGGED
            else:
                Script.log(f'Unknown media event status identifier: "{response["status"]}".', lvl = Script.WARNING)
            return MediaEvent(
                id = response['id'],
                game_id = response['game_id'],
                title = response['title'],
                description = response['description'],
                datetime = dt,
                order = response['order'],
                provider = provider,
                status = status,
                provider_mediaid = response['provider_mediaid'],
                provider_eventid = response['provider_eventid'],
                _game = game)
        except:
            Script.log(f'Unable to parse the following media event:', lvl = Script.ERROR)
            Script.log(f'{json.dumps(response, indent=4)}', lvl = Script.ERROR)
            traceback.print_exc()
            return None




