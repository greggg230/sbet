Sure, I'll regenerate the README to include the necessary context without all the code. Here's a revised version:

---

# sbet

## Project Overview

sbet is a sports betting analysis tool that leverages historical data to predict outcomes for NBA games and evaluate betting strategies. The project uses Python with type annotations and ensures type consistency using `mypy`.

## Data Sources

The project uses three main CSV files:
1. `nba_teams_all.csv` - Contains a list of NBA teams.
2. `nba_games_all.csv` - Contains a list of all NBA games.
3. `nba_betting_money_line.csv` - Contains the money line odds offered by various sportsbooks on NBA games.

## Dependencies

- Python 3.8+
- pandas
- mypy

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/greggg230/sbet.git
   cd sbet
   ```

2. Install the required Python packages:
   ```bash
   pip install pandas mypy
   ```

3. Run `mypy` to check type consistency:
   ```bash
   mypy .
   ```

## Data Class Definitions

The following data classes are used to represent the data from the CSV files:

- `Team`: Represents a team.
- `Game`: Represents a game.
- `MoneyLineBettingOdds`: Represents money line betting odds.

## Usage Examples

Example functions to read the CSV files and convert the rows into instances of the respective data classes can be found in the project files.

### Reading Teams
Use the `read_teams` function to read the `nba_teams_all.csv` file.

### Reading Games
Use the `read_games` function to read the `nba_games_all.csv` file.

### Reading Betting Odds
Use the `read_betting_odds` function to read the `nba_betting_money_line.csv` file.

## Development Notes

- All Python code should use typing annotations.
- Use `mypy` to ensure type consistency.
- Separate the example usage into its own code block to facilitate easy copying into files.
- Maintain two newlines between the import statements and the first top-level object, and between every top-level object in the file.

## Future Plans

- Add support for different types of betting odds.
- Implement predictive models for calculating the probabilities of game outcomes.
- Develop a tool to analyze and validate betting strategies based on historical data and generated probabilities.

---

This README should provide a clear overview of the project without including all the code. If there's anything else you'd like to add or modify, please let me know!