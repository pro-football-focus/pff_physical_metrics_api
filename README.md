# PFF FC Physical Metrics API
PFF FC Physical Metrics API is a Python library developed by PFF FC. It provides convenient access to our physical metrics from applications written in Python. 

## Getting Your Questions Answered
If you have a question that is not addressed here, there are several ways to get in touch:
- Open a [GitHub Issue](https://github.com/pro-football-focus/pff_physical_metrics_api/issues)
- [Request a Feature](https://github.com/pro-football-focus/pff_physical_metrics_api/issues)
- Drop us a note at fchelp@pff.com

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
Make sure to use the URL and key that you are provided with.

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
To retrieve visibility information per team for all games available in a given competition and season, run:
```
functions.get_visibility(url, key, competition_id, season)
```
In order to retrieve all players from a specific competition for a given season, run:
```
functions.get_players_competition(url, key, competition_id, season)
```
Or alternatively, to retrieve all players from a specific competition for all seasons, run:
```
functions.get_players_competition_all(url, key, competition_id)
```
Or alternatively, to retrieve player information for a specific player, run:
```
functions.get_player(url, key, player_id)
```

After retrieving PFF FC's unique identifiers, you can retrieve physical metrics using the functions below with the following parameters:
- clock_filter: a string to select periods of games, e.g. "" for whole games, "00:00 - 15:00" for the first 15 minutes of games only, "15:01 - 45:00+" for the last 30 minutes of each first half only, etc.
- vis_filter: an integer to filter out games with low visibilty for a team: 0 for all games, 10 to filter out when teams are below 10% visibility.
- possession_filter: a string to select possession type, i.e. "all" for all, "I" for in-possession, "O" for out-possession or "N" for ball out of play

To retrieve physical metrics for all players in a game, use:
```
functions.physicalMetricsGameReport(url, key, game_id, clock_filter = "", possession_filter = "all")
```
To retrieve physical metrics per game for a single player in a given season of a competition, use:
```
functions.physicalMetricsPlayerReport(url, key, competition_id, season, player_id, clock_filter = "", vis_filter = 10, possession_filter = "all")
```
To retrieve aggregated physical metrics for all players in a given season of a competition, use:
```
functions.physicalMetricsPositionReport(url, key, competition_id, season, clock_filter = "", vis_filter = 10, possession_filter = "all")
```
To retrieve aggregated physical metrics for teams in a given season of a competition, use:
```
functions.physicalMetricsTeamReport(url, key, competition_id, season, teams, clock_filter = "", vis_filter = 10, possession_filter = "all")
```
Where teams is a list of team identifiers.

## GraphQL Resources
GraphQL is the query language for PFF FC’s APIs and provides an alternative to REST and ad-hoc webservice architectures. It allows clients to define the structure of the data required, and exactly the same structure of the data is returned from the server. It is a strongly typed runtime which allows clients to dictate what data is needed.
- [Introduction to GraphQL](https://graphql.org/learn/)
- [How to GraphQL](https://www.howtographql.com/)
- [GraphQL Specification](https://spec.graphql.org/)
- [GraphQL FAQ](https://graphql.org/faq/)
