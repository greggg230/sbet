from dataclasses import dataclass
from sbet.data.historical.models.transform.nba_team import NbaTeam


@dataclass(frozen=True)
class NbaGameOutcome:
    home_team: NbaTeam
    away_team: NbaTeam
    did_home_team_win: bool
