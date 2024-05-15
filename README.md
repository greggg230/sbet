SBET
Project Overview
SBET is a Python project aimed at developing predictive models for calculating the probabilities of outcomes for sporting events, starting with NBA games. The project uses historical play-by-play logs to generate simulations of future games and estimate the chances of a team winning or losing. It also includes tools for analyzing and validating sports prediction models by comparing generated probabilities with historical betting odds to determine profitable strategies.

Repository Structure
plaintext
Copy code
sbet/
├── data/
│   ├── models/
│   │   ├── __init__.py
│   │   ├── csv_models/
│   │   │   ├── __init__.py
│   │   │   ├── team.py
│   │   │   ├── game.py
│   │   │   ├── money_line_betting_odds.py
│   │   ├── nba_team.py
│   │   ├── nba_game.py
│   │   ├── nba_money_line_betting_opportunity.py
│   ├── parsing.py
│   ├── transform.py
├── tests/
│   ├── __init__.py
│   ├── test_parsing.py
│   ├── test_transform.py
├── README.md
├── requirements.txt
Data Models
CSV Models
These models directly map the columns in the CSV files:

Team: Represents NBA teams with fields like team_id, abbreviation, etc.
Game: Represents NBA games with fields like game_id, team_id, game_date, etc.
MoneyLineBettingOdds: Represents betting odds with fields like game_id, book_name, team_id, etc.
Derived Models
These models are derived from the CSV models to provide more useful representations:

NbaTeam: An enum representing NBA teams using their abbreviations.
NbaGame: Represents an NBA game with fields like game_id, game_date, home_team, away_team, etc.
NbaMoneyLineBettingOpportunity: Represents a betting opportunity with fields like game, book_name, away_odds, home_odds.
Parsing and Transformation
parsing.py: Contains functions to parse CSV files into Team, Game, and MoneyLineBettingOdds data classes.
transform.py: Contains functions to transform parsed data into NbaGame and NbaMoneyLineBettingOpportunity objects.
Testing
test_parsing.py: Tests for parsing CSV data into data classes.
test_transform.py: Tests for transforming data classes into derived models. Includes a test case to verify error handling when a game cannot be found.
Installation
Install the required packages using:

sh
Copy code
pip install -r requirements.txt
Usage
Parsing CSV Data:

python
Copy code
from sbet.data.parsing import read_teams, read_games, read_money_line_betting_odds
from sbet.data.models.csv_models import Team, Game, MoneyLineBettingOdds

teams = read_teams('nba_teams_all.csv')
games = read_games('nba_games_all.csv')
money_line_betting_odds = read_money_line_betting_odds('nba_betting_money_line.csv')
Transforming Data:

python
Copy code
from sbet.data.transform import transform_to_nba_games, transform_to_nba_money_line_betting_opportunities
from sbet.data.models import NbaGame, NbaMoneyLineBettingOpportunity

nba_games = transform_to_nba_games(games, teams)
opportunities = transform_to_nba_money_line_betting_opportunities(money_line_betting_odds, nba_games)
Project Guidelines
Code Style: Use typing hints with the typing module. Ensure type consistency using mypy.
File Naming: Test files should be prefixed with test_.
Formatting: Ensure two newlines between imports and top-level objects (functions, classes).