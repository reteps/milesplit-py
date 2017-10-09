#!/usr/bin/env python3

import requests, sys
from bs4 import BeautifulSoup as soup
CATEGORIES = ["","article","athlete","meet","team","video"]
MILESPLIT = "http://milesplit.com"
SEARCH_URL = "http://{}milesplit.com/search?q={}&category={}"
ATHLETE_URL = "http://milesplit.com/athletes/pro/{}/stats"
PERFORMANCE_URL = "http://milesplit.com/athletes/{}/performances/{}"
class NotValid(Exception):
    pass


def search_for(item, category="",state=None):
    parsed_item = item.replace(" ","+")
    parsed_category = category.lower()
    if parsed_category not in CATEGORIES:
        raise NotValid("invalid search category")
    if item == "":
        raise NotValid("invalid search term")
    if type(state) == str:
        if len(state) != 2:
            raise NotValid("invalid state")
    if state == None:
        parsed_state = ""
    else:
        parsed_state = state + "."
    page = soup(session.get(SEARCH_URL.format(parsed_state,parsed_item,parsed_category)).content,"html.parser")
    raw_results = page.find("div",{"class":"searchResults"}).find("ul").findAll("li")
    results = []
    for raw_result in raw_results:
        raw_link = raw_result.find("a",{"class":"title"})
        link = MILESPLIT + raw_link["href"]
        id = raw_link["href"].split("/")[-1]
        descrip = raw_result.find("div",{"class":"description"}).text.strip()
        result_type = raw_result.find("span",{"class":"type"}).text.strip()
        result = raw_link.text.strip()
        results.append({"result":result,"link":link,"id":id,"description":descrip,"type":result_type})
    return results

def lookup_athlete(id,prefix="time"):
    info = {}
    page = soup(session.get(ATHLETE_URL.format(id)).content,"html.parser")

    team_data = page.find("div",{"class":"team"})
    name = page.find("h1").text.strip().replace("\n"," ")
    try:
        class_of = team_data.find("span",{"class":"grade"}).text.strip().split("Class of ")[1]
    except AttributeError:
        class_of = 'N/A'
    city = team_data.find("span",{"class":"city"}).text.strip()
    school = team_data.find("a").text.strip()
    school_link = team_data.find("a")["href"]
    info["about"] = {"name":name,"class":class_of,"city":city,"school":school,"school_link":school_link}
    info["records"] = {}
    for record in page.find("div",{"class":"bests"}).find("ul").findAll("li"):
        pr = record.text.strip().split(" - ")
        info["records"][pr[0]] = pr[1]

    info["events"] = {}
    races = page.find("table",{"class":"performances"}).find("tbody").findAll("tr")
    current_section = ""
    for race in races:
        if "thead" in race["class"]:
            if race["class"] == ["thead"]:
                current_section = race.find("th",{"class":"event"}).text.strip()
                info["events"][current_section] = []
        else:
            when = race.find("time",{"class":"start"}).text.strip()
            place = race.find("td",{"class":"place"}).text.strip()
            name = race.find("td",{"class":"meet"}).text.strip()
            page_time = race.findAll("a")[-1]["href"]
            page = soup(session.get(MILESPLIT+page_time).content,"html.parser")
            score = page.find("div",{"class":"mark"}).find("span").text.strip()
            info["events"][current_section].append({"name":name,"date":when,"place":place,prefix:score})
    return info

if __name__ == '__main__':
    session = requests.Session()
    results = search_for(' '.join(sys.argv[1:]))
    if results[0]["type"] == "athlete":
        about = lookup_athlete(results[0]["id"])
        import json
        print(json.dumps(about, indent=2))
    else:
        print("Not an Athlete.")
