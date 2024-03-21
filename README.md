# pff_physical_metrics_api
PFF Physical Metrics API is a Python library developed by PFF FC. It provides convenient access to our physical metrics from applications written in Python. 

## Getting Your Questions Answered
If you have a question that is not addressed here, there are several ways to get in touch:
- Open a [GitHub Issue](https://github.com/pro-football-focus/pff_physical_metrics_api/issues)
- [Request a Feature](https://github.com/pro-football-focus/pff_physical_metrics_api/issues)
- Drop us a note at fchelp@pff.com 

## Documentation
TO DO: Upload documentation

## Installation
Use your unique PFF FC API key or request an API key by emailing fchelp@pff.com.
```
pip install git+https://github.com/pro-football-focus/pff_physical_metrics_api.git
```
To uninstall, use:
```
pip uninstall pff_physical_metrics_api
```

## Usage
After successfully installing the package, import it:
```
from pff_physical_metrics_api import functions
```
Make sure to use the URL and key that your are provided with.

In order to retrieve all competitions available to you, run:
```
functions.get_competitions(url, key)
```
In order to retrieve all teams available to you, run:
```
functions.get_teams(url, key)
```
In order to retrieve all games from a specific competition, run:
```
functions.get_games(url, key, competition_id)
```
In order to retrieve all players from a specific competition, run:
```
functions.get_players_competition(url, key, competition_id)
```

After retrieving PFF FC's unique identifiers, you can retrieve physical metrics using the functions below with the following parameters:
  • clock_filter: a string to select periods of games, e.g. "" for whole games, "00:00 - 15:00" for the first 15 minutes of games only, "15:01 - 45:00+" for the last 30 minutes of each first half only, etc.
  • vis_filter: an integer to filter out games with low visibilty for a team: 0 for all games, 10 to filter out when teams are below 10% visibility.

To retrieve physical metrics for all players in a game, use:
```
functions.physicalMetricsGameReport(url, key, game_id, clock_filter = "")
```
To retrieve physical metrics per game for a single player in a given season of a competition, use:
```
functions.physicalMetricsPlayerReport(url, key, competition_id, season, player_id, clock_filter = "", vis_filter = 10)
```
To retrieve aggregated physical metrics for all players in a given season of a competition, use:
```
functions.physicalMetricsPositionReport(url, key, competition_id, season, clock_filter = "", vis_filter = 10)
```
To retrieve aggregated physical metrics for teams in a given season of a competition, use:
```
functions.physicalMetricsTeamReport(url, key, competition_id, season, teams, clock_filter = "", vis_filter = 10)
```
Where teams is a list of team identifiers.

## GraphQL Resources
GraphQL is the query language for PFF FC’s APIs and provides an alternative to REST and ad-hoc webservice architectures. It allows clients to define the structure of the data required, and exactly the same structure of the data is returned from the server. It is a strongly typed runtime which allows clients to dictate what data is needed.
- [Introduction to GraphQL](https://graphql.org/learn/)
- [How to GraphQL](https://www.howtographql.com/)
- [GraphQL Specification](https://spec.graphql.org/)
- [GraphQL FAQ](https://graphql.org/faq/)
