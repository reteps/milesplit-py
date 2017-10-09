#!/usr/bin/env python3

import urllib.request
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
    if state == None:
        parsed_state = ""
    else:
        parsed_state = state + "."
    page = soup(urllib.request.urlopen(SEARCH_URL.format(parsed_state,parsed_item,parsed_category)).read(),"lxml")
    raw_results = page.find("div",{"class":"searchResults"}).find("ul").findAll("li")
    results = []
    for raw_result in raw_results:
        link = raw_result.find("a")
        results.append({link.text.strip():{"link":MILESPLIT + link["href"]},"id":link["href"].split("/")[-1],"description":raw_result.find("div",{"class":"description"}).text.strip(),"type":raw_result.find("span",{"class":"type"}).text.strip()})
    return results

def lookup_athlete(id):
    info = {}
    page = soup(urllib.request.urlopen(ATHLETE_URL.format(id)).read(),"lxml")

    team_data = page.find("div",{"class":"team"})
    info["about"] = {"name":page.find("h1").text.strip().replace("\n"," "),"class":team_data.find("span",{"class":"grade"}),"city":team_data.find("span",{"class":"city"}),"school":team_data.find("a").text.strip(),"school_link":team_data.find("a").href}
    
    info["records"] = {}
    for record in page.find("div",{"class":"bests"}).find("ul").findAll("li"):
        pr = record.text.strip().split(" - ")
        info["records"][pr[0]] = pr[1]
     
    races = page.find("table",{"class":"performances"}).find("tbody").findAll("tr")
    for race in races:
        if not "thead" in race["class"]:
            # time class=start
            # td class=place
            
    # races - event - name, date, place, time

results = search_for("ben ebert",category="",state="nc")
lookup_athlete(results[0]["id"])
