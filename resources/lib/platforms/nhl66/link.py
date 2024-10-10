from __future__ import annotations
from ...common.url import encode_proxy_url
from .team import Team
from typing import Optional, List
from enum import Enum
from codequick import Script
from codequick.utils import bold, color
from .utils import get_stateshot
from .auth import Auth
from datetime import datetime
from .consts import RDS_THUMB, TVASPORTS_THUMB, SPORTSNET_THUMB, ESPN_THUMB, NHLTV_THUMB
from ...common.labels import labels

import json, traceback


class LinkStatus(Enum):
    UNKNOWN = 0
    PLANNED = 1
    LIVE = 2
    REPLAY = 3
    DELAYED = 4
    BUGGED = 5

class LinkProvider(Enum):
    UNKNOWN = 0
    NHLTV = 1
    ESPN = 2


class Link:

    def __init__(self, id: int, content_id: str, url: Optional[str], status: LinkStatus, provider: LinkProvider, datetime: datetime, game = None, premium_flavor: str = None):
        self.id = id
        self.content_id = content_id
        self.stream = content_id.split('|')[3]
        self.url = url
        self.status = status
        self.provider = provider
        self.datetime = datetime
        self._game = game
        self.premium_flavor = premium_flavor


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
    
    @property
    def label(self) -> str:
        # Label
        label = self.stream
        if self.provider == LinkProvider.NHLTV:
            label = f'NHL.TV - {label}'
        elif self.provider == LinkProvider.ESPN:
            label = f'ESPN - {label}'
        if self.status == LinkStatus.LIVE:
            label = f'{bold(color(Script.localize(labels.get("live")), "limegreen"))} - {label}'
        elif self.status == LinkStatus.REPLAY:
            label = f'{bold(color(Script.localize(labels.get("replay")), "gold"))} - {label}'
        elif self.status == LinkStatus.BUGGED:
            label = f'{bold(color(Script.localize(labels.get("bugged")), "crimson"))} - {label}'
        elif self.status == LinkStatus.PLANNED:
            label = f'{bold(color(Script.localize(labels.get("planned")), "deeppink"))} - {label}'
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
        if self.provider == LinkProvider.NHLTV:
            thumbnail = NHLTV_THUMB
        elif self.provider == LinkProvider.ESPN:
            thumbnail = ESPN_THUMB
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
    def from_id(cls, id: int, skip_cache: bool = False) -> Optional[Link]:
        stateshot = get_stateshot(skip_cache)
        for i in stateshot['links']:
            link = Link.from_response(i)
            if link.id == id:
                return link
        return None


    @classmethod
    def from_response(cls, response, game = None):
        try:
            # Datetime
            dt = datetime.fromisoformat(response['event_datetime'].replace('Z','+00:00'))
            # Provider
            provider = LinkProvider.UNKNOWN
            if 'nhl' in response['provider'].lower():
                provider = LinkProvider.NHLTV
            elif 'espn' in response['provider'].lower():
                provider = LinkProvider.ESPN
            else:
                Script.log(f'Unknown link provider identifier: "{response["provider"]}".', lvl = Script.WARNING)
            # Url
            url = None
            if response['url']:
                if provider == LinkProvider.NHLTV:
                    url = encode_proxy_url(response['url'], provider='nhltv')
                elif provider == LinkProvider.ESPN:
                    url = encode_proxy_url(response['url'], provider='espn')
                else:
                    url = encode_proxy_url(response['url'])
            # Status
            status = LinkStatus.UNKNOWN
            if response['status'] == 'M':
                status = LinkStatus.DELAYED
            elif response['status'] == 'P':
                status = LinkStatus.PLANNED
            elif response['status'] == 'R':
                status = LinkStatus.REPLAY
            elif response['status'] == 'L':
                status = LinkStatus.LIVE
            elif response['status'] == 'E':
                status = LinkStatus.BUGGED
            else:
                Script.log(f'Unknown link status identifier: "{response["status"]}".', lvl = Script.WARNING)
            # Premium flavor
            premium_flavor = None
            if Auth.is_premium():
                flavors = response.get('flavors', [])
                if len(flavors) > 0:
                    premium_flavor = flavors[0].get('unique_id', None)
            return Link(id=response['id'], content_id=response['content_id'], url=url, status=status, provider=provider, datetime=dt, game=game, premium_flavor=premium_flavor)
        except:
            Script.log(f'Unable to parse the following link:', lvl = Script.ERROR)
            Script.log(f'{json.dumps(response, indent=4)}', lvl = Script.ERROR)
            traceback.print_exc()
            return None




