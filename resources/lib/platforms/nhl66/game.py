from __future__ import annotations
from .team import Team
from typing import Optional, List, Union
from enum import Enum
from codequick import Script
from ...common.labels import labels
from .media_event import MediaEvent
from .utils import get_stateshot
from datetime import datetime
from codequick import Script
from codequick.utils import bold, color, italic
from ...platforms.thesportsdb.schedule import get_game
from ...platforms.thesportsdb.tvevents import get_tv_events
from ...common.thumbnails import get_thumbnail_url, get_poster_url, get_square_url
import json, traceback



class GameStatus(Enum):
    UNKNOWN = 0
    PLANNED = 1
    LIVE = 2
    FINAL = 3


class Game:

    def __init__(self, id: int, external_id: str, datetime: datetime, start_datetime: Union[datetime, None], final_datetime: Union[datetime, None], away_team: Team, home_team: Team, status: GameStatus, winner: Optional[Team] = None):
        self.id = id
        self.external_id = external_id
        self.datetime = datetime
        self.start_datetime = start_datetime
        self.final_datetime = final_datetime
        self.status = status
        self.away_team = away_team
        self.home_team = home_team
        self.winner = winner
        self.thumbnail = get_thumbnail_url(self.home_team.abbreviation, self.away_team.abbreviation)
        self.poster    = get_poster_url   (self.home_team.abbreviation, self.away_team.abbreviation)
        self.square    = get_square_url   (self.home_team.abbreviation, self.away_team.abbreviation)
        self._tsdb_game_event = None
        self._tsdb_tv_events = None


    def get_media_events(self, skip_cache: bool = False) -> List[MediaEvent]:
        stateshot = get_stateshot(skip_cache)
        media_events: list[MediaEvent] = []
        for i in stateshot['media_events']:
            if i['game_id'] == self.id:
                media_event: MediaEvent = MediaEvent.from_response(i, self)
                if media_event is not None:
                    media_events.append(media_event)
        Script.log(f'{str(len(media_events))} media events found.', lvl = Script.DEBUG)
        return media_events
    
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
        if self.status == GameStatus.PLANNED:
            label = f'{color(bold(Script.localize(labels.get("planned"))), "deeppink" )} - {label}'
        if self.status == GameStatus.LIVE:
            label = f'{color(bold(Script.localize(labels.get("live"))),    "limegreen")} - {label}'
        if self.status == GameStatus.FINAL:
            label = f'{color(bold(Script.localize(labels.get("final"))),   "gold"     )} - {label}'
        return label
        

    @classmethod
    def from_id(cls, id: int, skip_cache: bool = False) -> Optional[Game]:
        stateshot = get_stateshot(skip_cache)
        for i in stateshot['games']:
            game = Game.from_response(i, stateshot['teams'])
            if game.id == id:
                return game
        return None


    @classmethod
    def from_response(cls, game_response, teams_response):
        try:
            # Datetime
            dt = datetime.fromisoformat(game_response['datetime'].replace('Z','+00:00'))
            st_dt = None
            if game_response['start_datetime']:
                st_dt = datetime.fromisoformat(game_response['start_datetime'].replace('Z','+00:00'))
            fn_dt = None
            if game_response['final_datetime']:
                fn_dt = datetime.fromisoformat(game_response['final_datetime'].replace('Z','+00:00'))
            # Get teams
            away_team = Team.from_id(game_response['away_team_id'], teams_response)
            home_team = Team.from_id(game_response['home_team_id'], teams_response)
            if away_team is None:
                Script.log('Unable to parse home team.', lvl = Script.ERROR)
                raise
            elif home_team is None:
                Script.log('Unable to parse away team.', lvl = Script.ERROR)
                raise
            # Get the winner
            winner = None
            if game_response['winner'] == 'A':
                winner = away_team
            elif game_response['winner'] == 'H':
                winner = home_team
            # Get the status
            status = GameStatus.UNKNOWN
            if game_response['status'] == 'S':
                status = GameStatus.PLANNED
            elif game_response['status'] == 'I':
                status = GameStatus.LIVE
            elif game_response['status'] == 'F':
                status = GameStatus.FINAL
            else:
                Script.log(f'Unknown game status identifier: "{game_response["status"]}".', lvl = Script.WARNING)

            # Get content ids
            return Game(
                id=game_response['id'],
                external_id=game_response['external_id'],
                datetime=dt,
                start_datetime=st_dt,
                final_datetime=fn_dt,
                away_team=away_team, 
                home_team=home_team,
                status=status,
                winner=winner
            )
        except:
            Script.log(f'Unable to parse the following game:', lvl = Script.ERROR)
            Script.log(f'{json.dumps(game_response, indent=4)}', lvl = Script.ERROR)
            traceback.print_exc()
            return None



