import requests
import json
import os
from dotenv import load_dotenv

# STEP 0: Load our url token from somewhere safe
load_dotenv()
ESPN_API_URL = os.getenv('ESPN_API_URL')

def nfl_game_scores():
    # ESPN API URL for NFL scoreboard
    url = ESPN_API_URL
    score_str = "Score(Away-Home): "

    # Get request to ESPN Football Stats API
    r = requests.get(url)
    if r.status_code == 200:
        data = r.json()
        events = data["events"]

        print('=' * 50)
        print(f"Week: {data['week']['number']}")
        print('=' * 50)
        # traverse thru events
        for i, event in enumerate(events, 1):
            print(f"Game {i}: {event['shortName']}")
            for competition in event["competitions"]:
                # print(f"{competition['date']}")
                for competitor in competition["competitors"]:
                    score_str += competitor['score']
                    score_str += " - "
                
                print(f"{reformat_date(event['date'])}") # print out date for each game
                score_str = score_str[:-1]
                print(score_str[:-1]) # omitting the extra '-'. For some reason, I need the splice for both lines or else it doesn't work. Why?
                score_str = "Score(Away-Home): "




        # print(json.dumps(events, indent=4))
    else:
        print(f"Request failed with status code: {r.status_code}")


# Reformat the date from isoString format to MM/DD/YYYY
def reformat_date(date):
    extract_date = date.split('T')[0]
    year_date = extract_date.split('-')[0]
    month_date = extract_date.split('-')[1]
    day_date = extract_date.split('-')[2]
   
    match month_date:
        case '09':
            month_date = 'Sep'
        case '10':
            month_date = 'Oct'
        case '11':
            month_date = 'Nov'
        case '12':
            month_date = 'Dec'
        case '01':
            month_date = 'Jan'
    
    return f'Date: {month_date}. {day_date}, {year_date}'