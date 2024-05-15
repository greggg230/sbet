sbet
Project Overview
sbet is a sports betting analysis tool that leverages historical data to predict outcomes for NBA games and evaluate betting strategies. The project uses Python with type annotations and ensures type consistency using mypy.

Data Sources
The project uses three main CSV files:

nba_teams_all.csv - Contains a list of NBA teams.
nba_games_all.csv - Contains a list of all NBA games.
nba_betting_money_line.csv - Contains the money line odds offered by various sportsbooks on NBA games.
Dependencies
Python 3.8+
pandas
mypy
unittest
Setup Instructions
Clone the repository:

bash
Copy code
git clone https://github.com/greggg230/sbet.git
cd sbet
Install the required Python packages:

bash
Copy code
pip install pandas mypy
Run mypy to check type consistency:

bash
Copy code
mypy .
Data Class Definitions
The following data classes are used to represent the data from the CSV files and the derived models:

CSV Models
Located in sbet/data/models/csv_models:

Team: Represents a team.
Game: Represents a game.
MoneyLineBettingOdds: Represents money line betting odds.
Derived Models
Located in sbet/data/models:

NbaTeam: Enum representing NBA team abbreviations.
NbaGame: Represents a derived model of an NBA game with enriched data.
Usage Examples
Example functions to read the CSV files and convert the rows into instances of the respective data classes can be found in the project files.

Reading Teams
Use the read_teams function to read the nba_teams_all.csv file.

Reading Games
Use the read_games function to read the nba_games_all.csv file.

Reading Betting Odds
Use the read_betting_odds function to read the nba_betting_money_line.csv file.

Transforming Data
Use the transform_to_nba_games function to transform parsed game and team data into instances of NbaGame.

Unit Tests
Unit tests for the parsing functions and transformation functions can be found in the sbet/tests directory. The tests ensure that every field in the CSV data is being parsed correctly and that the transformation functions work as expected.

Running Unit Tests
To run the unit tests, navigate to the project root and execute:

bash
Copy code
python -m unittest discover sbet/tests
Development Notes
All Python code should use typing annotations.
Use mypy to ensure type consistency.
Separate the example usage into its own code block to facilitate easy copying into files.
Maintain two newlines between the import statements and the first top-level object, and between every top-level object in the file.
Do not include the if __name__ == '__main__' block in test files.
Future Plans
Add support for different types of betting odds.
Implement predictive models for calculating the probabilities of game outcomes.
Develop a tool to analyze and validate betting strategies based on historical data and generated probabilities.