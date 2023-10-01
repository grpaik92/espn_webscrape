print('hello')

import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from flask import Flask, Response
import io
from datetime import datetime

user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"

teams =['ari','atl','bal','bos','chc','chw','cin','cle','col','det','hou','kc','laa','lad','mia','mil','min','nym','nyy','oak','phi','pit','sd','sf','sea','stl','tb','tex','tor','wsh']

#empty DataFrame 
all_data = []

for team in teams:
    headers = {'User-Agent': user_agent}

    url1 = f'https://www.espn.com/mlb/team/schedule/_/name/{team}/seasontype/2/half/1'

    imgurl1 = f'http://a.espncdn.com/combiner/i?img=/i/teamlogos/mlb/500/{team}.png'

    response1 = requests.get(url1, headers=headers)
    soup1 = BeautifulSoup(response1.text, 'html.parser')

    tbody = soup1.find('tbody', {'class': 'Table__TBODY'})

    print('Team Name:' + team)
    if tbody:
        tr_tags = tbody.find_all('tr')

        col_widths = [11, 18, 11, 5, 11, 15, 15]

        # Initialize streak variables
        win_streak = 0
        loss_streak = 0
        current_streak = 0
        current_type = None  # 'W' for win, 'L' for loss

        for tr_tag in tr_tags:
            td_tags = tr_tag.find_all('td')

            if td_tags:
                first_td_value = td_tags[0].text
                second_td_value = td_tags[1].text
                third_td_value = td_tags[2].text if len(td_tags) > 2 else "N/A"
                fourth_td_value = td_tags[3].text if len(td_tags) > 3 else "N/A"
                fifth_td_value = td_tags[4].text if len(td_tags) > 4 else "N/A"
                sixth_td_value = td_tags[5].text if len(td_tags) > 5 else "N/A"

                # Convert 'Fri, Mar 30' to 'mm-dd-yyyy' with year '2023'
                date_parts = first_td_value.split(', ')
                if len(date_parts) == 2:
                    date_str = date_parts[1] + ' 2023'
                    formatted_date = datetime.strptime(date_str, '%b %d %Y').strftime('%m-%d-%Y')

                # calculate run differential
                numbers = re.findall(r'\d+', third_td_value)
                if len(numbers) >= 2:
                    difference = int(numbers[0]) - int(numbers[1])
                else:
                    difference = "N/A"

                if third_td_value.startswith('L'):
                    difference = f"({difference})"

                # Extract the result (W or L) from the score    
                result = third_td_value[0]

                # Calculate win and loss streaks
                if result == 'W':
                    if current_type == 'W':
                        current_streak += 1
                    else:
                        current_type = 'W'
                        current_streak = 1
                    streak = f'W{current_streak}'
                elif result == 'L':
                    if current_type == 'L':
                        current_streak += 1
                    else:
                        current_type = 'L'
                        current_streak = 1
                    streak = f'L{current_streak}'
                else:
                    current_streak = 0
                    streak = "N/A"

                if re.match(r'^\d', fourth_td_value):
                    data = {
                        "Team": team,
                        "Date": formatted_date,
                        "Opponent": second_td_value,
                        "Score": third_td_value,
                        "W or L": result,
                        "Streak": streak,
                        "Differential": difference,
                        "Team Record": fourth_td_value,
                        "Winning Pitcher": fifth_td_value,
                        "Losing Pitcher": sixth_td_value,
                        "Team Logo": imgurl1
                    }
                    all_data.append(data)

    else:
        print(f"No data found for team: {team}")

    # Now process and print data for tr_tags2
    url2 = f'https://www.espn.com/mlb/team/schedule/_/name/{team}/seasontype/2/half/2'

    imgurl2 = f'http://a.espncdn.com/combiner/i?img=/i/teamlogos/mlb/500/{team}.png'


    response2 = requests.get(url2, headers=headers)
    soup2 = BeautifulSoup(response2.text, 'html.parser')

    tbody2 = soup2.find('tbody', {'class': 'Table__TBODY'})

    if tbody2:
        tr_tags2 = tbody2.find_all('tr')

        # Initialize streak variables
        win_streak2 = 0
        loss_streak2 = 0
        current_streak2 = 0
        current_type2 = None  # 'W' for win, 'L' for loss

        for tr_tag2 in tr_tags2:
            td_tags2 = tr_tag2.find_all('td')

            if td_tags2:
                first_td_value2 = td_tags2[0].text
                second_td_value2 = td_tags2[1].text
                third_td_value2 = td_tags2[2].text if len(td_tags2) > 2 else "N/A"
                fourth_td_value2 = td_tags2[3].text if len(td_tags2) > 3 else "N/A"
                fifth_td_value2 = td_tags2[4].text if len(td_tags2) > 4 else "N/A"
                sixth_td_value2 = td_tags2[5].text if len(td_tags2) > 5 else "N/A"

                # Convert 'Fri, Mar 30' to 'mm-dd-yyyy' with year '2023'
                date_parts2 = first_td_value2.split(', ')
                if len(date_parts2) == 2:
                    date_str2 = date_parts2[1] + ' 2023'
                    formatted_date2 = datetime.strptime(date_str2, '%b %d %Y').strftime('%m-%d-%Y')

                numbers2 = re.findall(r'\d+', third_td_value2)
                if len(numbers2) >= 2:
                    difference2 = int(numbers2[0]) - int(numbers2[1])
                else:
                    difference2 = "N/A"

                if third_td_value2.startswith('L'):
                    difference2 = f"({difference2})"

                # Extract result from score
                result2 = third_td_value2[0]

                # Calculate win and loss streaks
                if result2 == 'W':
                    if current_type2 == 'W':
                        current_streak2 += 1
                    else:
                        current_type2 = 'W'
                        current_streak2 = 1
                    streak2 = f'W{current_streak2}'
                elif result2 == 'L':
                    if current_type2 == 'L':
                        current_streak2 += 1
                    else:
                        current_type2 = 'L'
                        current_streak2 = 1
                    streak2 = f'L{current_streak2}'
                else:
                    current_streak2 = 0
                    streak2 = "N/A"

                if re.match(r'^\d', fourth_td_value2):
                    data2 = {
                        "Team": team,
                        "Date": formatted_date2,
                        "Opponent": second_td_value2,
                        "Score": third_td_value2,
                        "W or L": third_td_value2[0],
                        "Streak": streak2,
                        "Differential": difference2,
                        "Team Record": fourth_td_value2,
                        "Winning Pitcher": fifth_td_value2,
                        "Losing Pitcher": sixth_td_value2,
                        "Team Logo": imgurl2
                    }
                    all_data.append(data2)

                    # print("{:<{width1}} {:<{width2}} {:<{width3}} {:<{width4}} {:<{width5}} {:<{width6}} {:<{width7}}".format(
                    #     first_td_value2, second_td_value2, third_td_value2, difference2, fourth_td_value2, fifth_td_value2, sixth_td_value2,
                    #     width1=col_widths[0], width2=col_widths[1], width3=col_widths[2], width4=col_widths[3], width5=col_widths[4], width6=col_widths[5], width7=col_widths[6]))

    else:
        print(f"No data found for team: {team}")

df = pd.DataFrame(all_data)
# Export the DataFrame to a CSV file (in-memory)
csv_output = io.StringIO()
df.to_csv(csv_output, index=False)
csv_content = csv_output.getvalue()

# Create a Flask web application
app = Flask(__name__)

@app.route('/')
def index():
    return '''
    <h1>MLB Schedule Data</h1>
    <p><a href="/download_csv">Download CSV</a></p>
    '''

@app.route('/download_csv')
def download_csv():
    response = Response(csv_content, content_type='text/csv')
    response.headers['Content-Disposition'] = 'attachment; filename=mlb_data.csv'
    return response

if __name__ == '__main__':
    app.run(debug=True)
    # print("\n\n")  # Add a newline between teams