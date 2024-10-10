from __future__ import annotations
from .team import Team
from typing import Optional, List
from enum import Enum
from codequick import Script
from ...common.labels import labels
from .link import Link
from .utils import get_stateshot
from datetime import datetime
from codequick import Script
from codequick.utils import bold, color, italic
from ...platforms.thesportsdb.schedule import get_game
from ...platforms.thesportsdb.tvevents import get_tv_events
from ...common.thumbnails import get_thumbnail_url
import json, traceback



class GameStatus(Enum):
    UNKNOWN = 0
    PREGAME = 1
    LIVE = 2
    FINAL = 3


class Game:

    def __init__(self, id: int, datetime: datetime, away_team: Team, home_team: Team, status: GameStatus, content_ids: List[str] = [], winner: Optional[Team] = None):
        self.id = id
        self.datetime = datetime
        self.status = status
        self.away_team = away_team
        self.home_team = home_team
        self.content_ids = content_ids
        self.winner = winner
        self.thumbnail = get_thumbnail_url(self.home_team.abbreviation, self.away_team.abbreviation)
        self._tsdb_game_event = None
        self._tsdb_tv_events = None


    def get_links(self, skip_cache: bool = False) -> List[Link]:
        stateshot = get_stateshot(skip_cache)
        links: list[Link] = []
        for i in stateshot['links']:
            link: Link = Link.from_response(i, self)
            if link is not None and link.content_id in self.content_ids:
                links.append(link)
        Script.log(f'{str(len(links))} links found.', lvl = Script.DEBUG)
        return links
    
    @property
    def tsdb_game_event(self):
        if self._tsdb_game_event is not None:
            return self._tsdb_game_event
        try:
            self._tsdb_game_event = get_game(self.datetime, self.home_team.abbreviation, self.away_team.abbreviation)
        except:
            pass
        return self._tsdb_game_event
    
    @property
    def tsdb_tv_events(self):
        if self._tsdb_tv_events is not None:
            return self._tsdb_tv_events
        try:
            if self.tsdb_game_event is not None:
                self._tsdb_tv_events = get_tv_events(self.tsdb_game_event)
        except:
            pass
        return self._tsdb_tv_events
    
    @property
    def label(self) -> str:
        # Label
        label = f'{self.away_team.full_name} @ {self.home_team.full_name} - {italic(self.datetime.astimezone().strftime("%Y/%m/%d - %H:%M"))}'
        if self.status == GameStatus.PREGAME:
            label = f'{color(bold(Script.localize(labels.get("pregame"))), "deeppink" )} - {label}'
        if self.status == GameStatus.LIVE:
            label = f'{color(bold(Script.localize(labels.get("live"))),    "limegreen")} - {label}'
        if self.status == GameStatus.FINAL:
            label = f'{color(bold(Script.localize(labels.get("final"))),   "gold"     )} - {label}'
        return label
        

    @classmethod
    def from_id(cls, id: int, skip_cache: bool = False) -> Optional[Game]:
        stateshot = get_stateshot(skip_cache)
        for i in stateshot['games']:
            game = Game.from_response(i)
            if game.id == id:
                return game
        return None


    @classmethod
    def from_response(cls, response):
        try:
            # Datetime
            dt = datetime.fromisoformat(response['start_datetime'].replace('Z','+00:00'))
            # Get teams
            away_team = Team.from_abbreviation(response['away_abr'])
            home_team = Team.from_abbreviation(response['home_abr'])
            if away_team is None:
                Script.log('Unable to parse home team.', lvl = Script.ERROR)
                raise
            elif home_team is None:
                Script.log('Unable to parse away team.', lvl = Script.ERROR)
                raise
            # Get the winner
            winner = None
            if response['winner'] == 'A':
                winner = away_team
            elif response['winner'] == 'H':
                winner = home_team
            # Get the status
            status = GameStatus.UNKNOWN
            if response['status'] == 'P':
                status = GameStatus.PREGAME
            elif response['status'] == 'I':
                status = GameStatus.LIVE
            elif response['status'] == 'F':
                status = GameStatus.FINAL
            else:
                Script.log(f'Unknown game status identifier: "{response["status"]}".', lvl = Script.WARNING)

            # Get content ids
            return Game(
                id=response['id'], 
                datetime=dt,
                away_team=away_team, 
                home_team=home_team,
                status=status,
                content_ids=response['content_id_list'],
                winner=winner
            )
        except:
            Script.log(f'Unable to parse the following game:', lvl = Script.ERROR)
            Script.log(f'{json.dumps(response, indent=4)}', lvl = Script.ERROR)
            traceback.print_exc()
            return None



