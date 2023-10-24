from .game import Game
from codequick import Script
from typing import List
from .utils import get_stateshot

class NHL66:

    @staticmethod
    def get_schedule(skip_cache: bool = False) -> List[Game]:
        stateshot = get_stateshot(skip_cache)
        games: list[Game] = []
        Script.log(f'{str(len(stateshot["games"]))} games found.', lvl = Script.DEBUG)
        for i in stateshot['games']:
            game = Game.from_response(i)
            if game is not None:
                games.append(game)
        return games