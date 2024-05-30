from enum import Enum


class NbaTeam(Enum):
    ATL = "ATL"
    BOS = "BOS"
    BKN = "BKN"
    CHA = "CHA"
    CHI = "CHI"
    CLE = "CLE"
    DAL = "DAL"
    DEN = "DEN"
    DET = "DET"
    GSW = "GSW"
    HOU = "HOU"
    IND = "IND"
    LAC = "LAC"
    LAL = "LAL"
    MEM = "MEM"
    MIA = "MIA"
    MIL = "MIL"
    MIN = "MIN"
    NOP = "NOP"
    NYK = "NYK"
    OKC = "OKC"
    ORL = "ORL"
    PHI = "PHI"
    PHX = "PHX"
    POR = "POR"
    SAC = "SAC"
    SAS = "SAS"
    TOR = "TOR"
    UTA = "UTA"
    WAS = "WAS"
    SEA = "SEA"

    @staticmethod
    def from_csv_name(name: str) -> 'NbaTeam':
        name_map = {
            "portland_trail_blazers": NbaTeam.POR,
            "san_antonio_spurs": NbaTeam.SAS,
            "utah_jazz": NbaTeam.UTA,
            "golden_state_warriors": NbaTeam.GSW,
            "houston_rockets": NbaTeam.HOU,
            "los_angeles_lakers": NbaTeam.LAL,
            "philadelphia_76ers": NbaTeam.PHI,
            "toronto_raptors": NbaTeam.TOR,
            "washington_wizards": NbaTeam.WAS,
            "indiana_pacers": NbaTeam.IND,
            "milwaukee_bucks": NbaTeam.MIL,
            "orlando_magic": NbaTeam.ORL,
            "chicago_bulls": NbaTeam.CHI,
            "brooklyn_nets": NbaTeam.BKN,
            "new_jersey_nets": NbaTeam.BKN,  # historical reference for New Jersey Nets
            "newjersey": NbaTeam.BKN,
            "dallas_mavericks": NbaTeam.DAL,
            "cleveland_cavaliers": NbaTeam.CLE,
            "memphis_grizzlies": NbaTeam.MEM,
            "sacramento_kings": NbaTeam.SAC,
            "new_orleans_pelicans": NbaTeam.NOP,
            "new_orleans_hornets": NbaTeam.NOP,  # historical reference for New Orleans Hornets
            "seattle_supersonics": NbaTeam.SEA,  # Adding Seattle SuperSonics for historical data
            "seattle": NbaTeam.SEA,
            "denver_nuggets": NbaTeam.DEN,
            "detroit_pistons": NbaTeam.DET,
            "miami_heat": NbaTeam.MIA,
            "new_york_knicks": NbaTeam.NYK,
            "minnesota_timberwolves": NbaTeam.MIN,
            "charlotte_hornets": NbaTeam.CHA,
            "atlanta_hawks": NbaTeam.ATL,
            "phoenix_suns": NbaTeam.PHX,
            "los_angeles_clippers": NbaTeam.LAC,
            "boston_celtics": NbaTeam.BOS,
            "oklahoma_city_thunder": NbaTeam.OKC,
        }
        # Normalize name (replace spaces and underscores, and make lowercase)
        normalized_name = name.lower().replace(' ', '_')
        if normalized_name in name_map:
            return name_map[normalized_name]
        raise ValueError(f"Unknown team name: {name}")
