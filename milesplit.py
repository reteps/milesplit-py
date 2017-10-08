#!/usr/bin/env python3

import urllib.request
from bs4 import BeautifulSoup as soup
CATEGORIES = ["","article","athlete","meet","team","video"]
MILESPLIT = "http://milesplit.com"
SEARCH_URL = "http://{}milesplit.com/search?q={}&category={}"
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
    print(SEARCH_URL.format(parsed_state,parsed_item,parsed_category))
    page = soup(urllib.request.urlopen(SEARCH_URL.format(parsed_state,parsed_item,parsed_category)).read(),"lxml")
    raw_results = page.find("div",{"class":"searchResults"}).find("ul").findAll("li")
    results = []
    for raw_result in raw_results:
        link = raw_result.find("a")
        results.append({link.text.strip():{"link":MILESPLIT + link["href"]},"id":link["href"].split("/")[-1],"description":raw_result.find("div",{"class":"description"}).text.strip(),"type":raw_result.find("span",{"class":"type"}).text.strip()})
    return results

results = search_for("hough",category="",state="nc")
for result in results:
    print(result)
