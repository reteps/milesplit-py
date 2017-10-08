#!/usr/bin/env python3

import urllib.request
from bs4 import BeautifulSoup as soup
CATEGORIES = ["","article","athlete","meet","team","video"]
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
        results.append({raw_result.find("a").text.strip():{"link":raw_result.find("a")["href"]},"description":raw_result.find("div",{"class":"description"}).text.strip(),"type":raw_result.find("span",{"class":"type"}).text.strip()})
    return results
results = search_for("x",category="athlete",state="nc")
print(results)
