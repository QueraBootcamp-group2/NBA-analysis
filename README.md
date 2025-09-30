# WEB SCRAPING SECTION
This section consists of three files
* MJP 
* BEST PLAYER 
* League champion players

## MJP file(mini-basketball)
there are some libraries. I set header due to sometimes this site block ip that do crawling. 
```python

import requests
from bs4 import BeautifulSoup
import time, random
import re

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Referer": "https://www.google.com/",
    "DNT": "1",
    "Connection": "keep-alive",
}
```

I define some variables for year , url , 
and break from "for" -->"count"
```python
year=2026
count=0
list_href_vote=[]
list_href_player=[]
base_url = "https://www.basketball-reference.com"
mvp_url="/awards/mvp.html"
full_url=base_url+mvp_url

```
i get response from site and after that I get vote link from site , because there are best players for each years in this link
and i store link in this variable "list_href_vote" 
```python

response = requests.get(full_url, headers=headers)
response.encoding = "utf-8"
print(response.status_code)
soup = BeautifulSoup(response.text, "html.parser")
player_rows =soup.find("tbody").find_all("tr")



for player_row in player_rows:
    if count== 7:
        break
    cells = player_row.find_all("td")
    third_td = cells[2]
    link_tag = third_td.find("a")
    list_href_vote.append(link_tag["href"])
    count += 1
```

we extract link for all player that exist in MJP and append some info for players in "list_href_player"
```python

for best_mvp_each_year_url in list_href_vote:
    full_url_mvp_each_year = base_url + best_mvp_each_year_url

    response = requests.get(full_url_mvp_each_year, headers=headers)
    response.encoding = "utf-8"
    print(response.status_code)
    time.sleep(random.uniform(3,5))
    soup_mvp_person = BeautifulSoup(response.text, "html.parser")

    players = soup_mvp_person.select("#div_mvp tbody tr")
    year=year-1

    for player in players:
        player_cell = player.select("td")
        url_info_player = player_cell[0].select_one("a")

        age=player_cell[1].text
        age_int=int(age)

        rank = player.select("th")
        player_rank = rank[0].text
        numbers = "".join(re.findall(r"\d+", player_rank))
        number_int = int(numbers)
        list_href_player.append({"year": year, "url_player": url_info_player["href"], "age": age_int, "player_rank": number_int})
```
finally i extract info for each player that include player name, positions , team name ,experience_years, height_cm,weight_kg

```python
import pandas as pd
positions = []
records=[]
height_cm=0
weight_kg=0
experience_years=0
cleaned=None
player_name=None
team_name=None

for player in list_href_player:
    response = requests.get(base_url+player["url_player"],headers=headers)
    response.encoding = "utf-8"
    info_player_soup = BeautifulSoup(response.text, "html.parser")


    url = player["url_player"]
    player_id = re.search(r'([^/]+)\.html$', url).group(1)


    player_name_elem = info_player_soup.select_one("#meta h1")
    player_name = player_name_elem.get_text(strip=True) if player_name_elem else None

    final_clean_positions = []
    position_elem = info_player_soup.select_one("#meta p:has(strong:-soup-contains('Position'))")

    text = position_elem.get_text(" ", strip=True)
    position = text.split("Shoots:")[0].replace("Position:", "").strip()
    clean_position = position.replace(", and", ",")
    clean2_position = clean_position.replace(" and ", ",")
    positions = [p.strip() for p in clean2_position.split(",") if p.strip()]
    for p in positions:
        cleaned = p.strip()
        cleaned = cleaned.replace("▪", "")
        cleaned = cleaned.strip()
        final_clean_positions.append(cleaned)

    team_strong = info_player_soup.select_one("#meta strong:-soup-contains('Team')")
    if team_strong:
        team_link_tag = team_strong.find_next("a")
        if team_link_tag:
            team_name = team_link_tag.get_text(strip=True)
    else:
        team_name = None



    exp_strong = info_player_soup.select_one("#meta strong:-soup-contains('Experience')")
    if exp_strong:
        experience_text = exp_strong.next_sibling.strip()
        match = re.search(r"\d+", experience_text)
        experience_years = int(match.group(0))

    else:
        exp_strong = info_player_soup.select_one("#meta strong:-soup-contains('Career Length')")
        experience_text = exp_strong.next_sibling.strip()
        match = re.search(r"\d+", experience_text)
        experience_years = int(match.group(0))




    height_weight_elems = info_player_soup.select_one("#meta p:has(span:-soup-contains('lb'))")
    text = height_weight_elems.get_text(" ", strip=True)
    match = re.search(r"\((\d+)cm,\s*(\d+)kg\)", text)
    height_cm = int(match.group(1))
    weight_kg = int(match.group(2))
```
we add to "records" for create dataframe 
```python
    records.append({
        "player_id": player_id,
        "player_name": player_name,
        "age": player["age"],
        "rank": player["player_rank"],
        "season": player["year"],
        "height_cm": height_cm,
        "weight_kg": weight_kg,
        "experience_years": experience_years,
        "positions": final_clean_positions,
        "team": team_name,
        "total_point": None,
        "groupName":"MJT"
    })
```
we create data frame
```python
df = pd.DataFrame(records)
print(df.head())
```





