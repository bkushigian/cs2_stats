"""
Parse a demo into rounds
"""

from demoparser2 import DemoParser

def parse_rounds(parser: DemoParser):
    round_start = parser.parse_event("round_start")
    round_end = parser.parse_event("round_end")
    rounds = []
    for (_, s), (_, e) in zip(round_start.iterrows(), round_end.iterrows()):
        round_number = s["round"]
        start_tick = s["tick"]
        end_tick = e["tick"]
        end_reason = e["reason"]
        winner = e["winner"]
        rounds.append(Round(round_number, start_tick, end_tick, end_reason, winner))
        pass
    ticks = parser.parse_ticks(["health", "score", "balance"])
    player_death = parser.parse_event("player_death", player=["X", "Y", "Z"])
    rounds_iter = iter(rounds)
    round = next(rounds_iter)
    return rounds


class Player:
    def __init__(self, name, team_number, steamid):
        self.name = name
        self.team_number = team_number
        self.steamid = steamid


class Game:
    def __init__(self, parser: DemoParser):
        player_info = parser.parse_player_info()
        teams = {}
        for row in player_info:
            name = row[1]["name"]
            team_number = row[1]["team_number"]
            steamid = row[1]["steamid"]
            player = Player(name, team_number, steamid)
            teams.setdefault(team_number, [])
            teams[team_number].append(player)
        self.teams = teams


class Round:
    def __init__(
        self,
        round_number: int,
        start_tick: int,
        end_tick: int,
        end_reason: str,
        winner: str,
    ):
        self.round_number = round_number
        self.start_tick = start_tick
        self.end_tick = end_tick
        self.end_reason = end_reason
        self.winner = winner
        self.deaths = []

    def round_info_str(self):
        return f"(Round {self.round_number}) Start Tick: {self.start_tick} | End Tick: {self.end_tick} | Winner: {self.winner}"


class Team:
    def __init__(self, players):
        self.players = tuple(players)
