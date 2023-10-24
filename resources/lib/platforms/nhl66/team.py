from dataclasses import dataclass

@dataclass
class Team:
    abbreviation: str
    name: str
    city: str
    country: str
    tsdb_id: str
    logo_light_url: str
    logo_dark_url: str

    @property
    def full_name(self):
        return f'{self.city} {self.name}'
    
    @classmethod
    def from_abbreviation(cls, abbreviation: str):
        from .consts import TEAMS
        for team in TEAMS:
            if team.abbreviation.lower() == abbreviation.lower():
                return team
        return None
    
    @classmethod
    def from_name(cls, name: str):
        from .consts import TEAMS
        for team in TEAMS:
            if team.name.lower() == name.lower():
                return team
        return None
    
    @classmethod
    def from_city(cls, city: str):
        from .consts import TEAMS
        for team in TEAMS:
            if team.city.lower() == city.lower():
                return team
        return None
    
    @classmethod
    def from_tsdb(cls, tsdb_id: str):
        from .consts import TEAMS
        for team in TEAMS:
            if team.tsdb_id == tsdb_id:
                return team
        return None

    

