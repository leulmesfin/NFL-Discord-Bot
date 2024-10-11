import requests
import json
import os
from dotenv import load_dotenv
import itertools

# STEP 0: Load our url token from somewhere safe
load_dotenv()
ESPN_API_URL = os.getenv("ESPN_API_URL")

def sort_by_yards(leaderboard):
    return sorted(leaderboard, key=lambda player: int(player.split("-")[1].split(',')[1].split(' ')[1]), reverse=True) # sort in descending order
    # for player in leaderboard:
    #     # extract the player's rushing yards
    #     stats = player.split("-")[1] # [n CAR, n YDS, n TD]
    #     yards = stats.split(',')[1].split(' ')[1] # [n], removed YDS (isolated n)
    #     print(yards)

# works for passing and receiving yards since they both exist @ index 0
def sort_by_yards_passing(leaderboard):
    return sorted(leaderboard, key=lambda player: int(player.split("-")[1].split(',')[0].split(' ')[1]), reverse=True) # sort in descending order
    # for player in leaderboard:
    #     # extract the player's rushing yards
    #     stats = player.split("-")[1] # [n CAR, n YDS, n TD]
    #     yards = stats.split(',')[1].split(' ')[1] # [n], removed YDS (isolated n)
    #     print(yards)

# Passing yards leaderboard
def passing_yards():
    # ESPN API URL for NFL scoreboard
    url = ESPN_API_URL

    # Get request to ESPN Football Stats API
    r = requests.get(url)
    if r.status_code == 200:
        data = r.json()
        pass_yards_lst = []

        for event in data['events']:
            for competition in event['competitions']:
                for category in competition['leaders']:
                    if category['name'] == 'passingYards':
                        for player in category['leaders']:
                            pass_yards_lst.append(f"{player['athlete']['fullName']} - {player['displayValue']}")

        pass_yards_lst = sort_by_yards_passing(pass_yards_lst) # sort list by passing yards
        pass_yards_str = ""
        pass_yards_str += "=" * 50 + "\n"
        pass_yards_str += "Passing Yards Leaderboard: " + "\n"
        pass_yards_str += "=" * 50 + "\n"
        for i, player in enumerate(pass_yards_lst, 1):
            pass_yards_str += f"{i}. {player}\n"

        return pass_yards_str
    else:
        return f"Request failed with status code: {r.status_code}"
    
# Rushing yards leaderboard
def rushing_yards():
    # ESPN API URL for NFL scoreboard
    url = ESPN_API_URL

    # Get request to ESPN Football Stats API
    r = requests.get(url)
    if r.status_code == 200:
        data = r.json()
        rush_yards_lst = []

        for event in data['events']:
            for competition in event['competitions']:
                for category in competition['leaders']:
                    if category['name'] == 'rushingYards':
                        for player in category['leaders']:
                            rush_yards_lst.append(f"{player['athlete']['fullName']} - {player['displayValue']}")

        rush_yards_lst = sort_by_yards(rush_yards_lst) # sort list by rushing yards
        rush_yards_str = ""
        rush_yards_str += "=" * 50 + "\n"
        rush_yards_str += "Rushing Yards Leaderboard: " + "\n"
        rush_yards_str += "=" * 50 + "\n"
        for i, player in enumerate(rush_yards_lst, 1):
            rush_yards_str += f"{i}. {player}\n"

        return rush_yards_str
    else:
        return f"Request failed with status code: {r.status_code}"

# Receiving yards leaderboard
def receiving_yards():
    # ESPN API URL for NFL scoreboard
    url = ESPN_API_URL

    # Get request to ESPN Football Stats API
    r = requests.get(url)
    if r.status_code == 200:
        data = r.json()
        receiving_yards_lst = []

        for event in data['events']:
            for competition in event['competitions']:
                for category in competition['leaders']:
                    if category['name'] == 'receivingYards':
                        for player in category['leaders']:
                            receiving_yards_lst.append(f"{player['athlete']['fullName']} - {player['displayValue']}")

        receiving_yards_lst = sort_by_yards_passing(receiving_yards_lst) # sort list by receiving yards
        receiving_yards_str = ""
        receiving_yards_str += "=" * 50 + "\n"
        receiving_yards_str += "Receptions Leaderboard: " + "\n"
        receiving_yards_str += "=" * 50 + "\n"
        for i, player in enumerate(receiving_yards_lst, 1):
            receiving_yards_str += f"{i}. {player}\n"

        return receiving_yards_str
    else:
        return f"Request failed with status code: {r.status_code}"
    
def bye_week_teams():
    # ESPN API URL for NFL scoreboard
    url = ESPN_API_URL
    bye_week_teams = ''
    bye_week_teams += "=" * 50 + "\n"
    bye_week_teams += "Teams on Bye Week: " + "\n" 
    bye_week_teams += "=" * 50 + "\n"

    # Get request to ESPN Football Stats API
    r = requests.get(url)
    if r.status_code == 200:
        data = r.json()
        teamsOnBye = data["week"]["teamsOnBye"]
        for team in teamsOnBye:
            bye_week_teams += f"{team['displayName']}\n"
    else:
        return f"Request failed with status code: {r.status_code}"

    return bye_week_teams


def nfl_game_scores():
    # ESPN API URL for NFL scoreboard
    url = ESPN_API_URL
    score_str = "Score (Away-Home): "
    game_channels = []
    scores = ""

    # Get request to ESPN Football Stats API
    r = requests.get(url)
    if r.status_code == 200:
        data = r.json()
        events = data["events"]

        scores += "=" * 50 + "\n"
        scores += f"Week: {data['week']['number']}" + "\n"
        scores += "=" * 50 + "\n"

        # traverse thru events
        for i, event in enumerate(events, 1):
            scores += f"Game {i}: {event['shortName']}" + "\n"
            for competition in event["competitions"]:
                for broadcast in competition["broadcasts"]:
                    game_channels.append(broadcast["names"])

                for competitor in competition["competitors"]:
                    score_str += competitor["score"]
                    score_str += " - "
                scores += f"{reformat_date(event['date'])}" + "\n"  # print out date for each game
                score_str = score_str[:-1]
                scores += (score_str[:-1]) + "\n"  # omitting the extra '-'. For some reason, I need the splice for both lines or else it doesn't work. Why?
                channels = ", ".join(flatten_list(game_channels))
                scores += f"Broadcast: {channels}" + "\n"

                score_str = "Score (Away-Home): "
                game_channels = []
                scores += "\n"
        return scores
    else:
        return f"Request failed with status code: {r.status_code}"


# Reformat the date from isoString format to MM/DD/YYYY
def reformat_date(date):
    extract_date = date.split("T")[0]
    year_date = extract_date.split("-")[0]
    month_date = extract_date.split("-")[1]
    day_date = extract_date.split("-")[2]

    match month_date:
        case "09":
            month_date = "Sep"
        case "10":
            month_date = "Oct"
        case "11":
            month_date = "Nov"
        case "12":
            month_date = "Dec"
        case "01":
            month_date = "Jan"

    return f"Date: {month_date}. {day_date}, {year_date}"


# optimized this function by using itertools.chain
# itertools.chain is memory-efficient bc it flattents the list using lazy eval: it doesn't create immediate lists
# also this one-liner is cleaner/more readable
def flatten_list(lst):
    # O(n) time
    # new_lst = []
    # for elt in lst:
    #     for item in elt:
    #         new_lst.append(item)
    # return new_lst
    return list(itertools.chain(*lst))  # O(n) time
