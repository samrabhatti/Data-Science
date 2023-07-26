from flask import Flask, jsonify, render_template, url_for
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

@app.route('/')
def cricket():
    html_text = requests.get('https://sports.ndtv.com/cricket/live-scores').text
    soup = BeautifulSoup(html_text, "html.parser")
    sections = soup.find_all('div', class_='sp-scr_wrp')

    results = []

    for section in sections:
        try:
            description = section.find('span', class_='description').text
            location = section.find('span', class_='location').text
            title = section.find('a', class_='sp-scr_lnk').text
            current = section.find('div', class_='scr_dt-red').text
            link = "https://sports.ndtv.com/" + section.find('a', class_='scr_ful-sbr-txt').get('href')

            status = section.find_all('div', class_="scr_dt-red")[1].text
            block = section.find_all('div', class_='scr_tm-wrp')
            team1_block = block[0]
            team1_name = team1_block.find('div', class_='scr_tm-nm').text
            team1_score = team1_block.find('span', class_='scr_tm-run').text
            team2_block = block[1]
            team2_name = team2_block.find('div', class_='scr_tm-nm').text
            team2_score = team2_block.find('span', class_='scr_tm-run').text

            # Check if any of the required details is missing for the current section
            if not (description and location and title and current and link and status and team1_name and team1_score and team2_name and team2_score):
                raise ValueError("Data not available for this section")

            result = {
                "Title": description.split(',')[0],
                "Description": description,
                "Location": location,
                "Status": status,
                "Current": current,
                "Team A": team1_name.strip(),
                team1_name.strip() + " Score": team1_score.strip(),
                "Team B": team2_name.strip(),
                team2_name.strip() + " Score": team2_score.strip().split(' ')[0],
                "Overs": team2_score.strip().split(' ')[1].strip().strip('()'),
                "Full Scoreboard": link,
                "Credits": "NDTV Sports"
            }

            results.append(result)
        except Exception as e:
            print(f"Skipping section - {e}")
    
    return render_template('cricket.html', results=results)

if __name__ == "__main__":
    app.run(debug=True)
