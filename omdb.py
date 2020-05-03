#!/usr/bin/env python

import requests

API_KEY = "9895477a"
API_URL = "http://www.omdbapi.com"

def find_by_title(title, type_="series", plot="full"):
    """
    finds by title
    """
    response = requests.get(url="%s?t=%s&type=%s&plot=%s&apikey=%s" % (API_URL, title, type_, plot, API_KEY))

    if response.status_code != 200:
        raise NotImplementedError

    body = response.json()    
    data = {}

    if body["Response"] != "True":
        return {}

    data["title"] = body["Title"]
    data["released"] = body["Released"]
    data["genre"] = body["Genre"].split(",")
    data["actors"] = body["Actors"].split(",")
    data["plot"] = body["Plot"]
    data["language"] = body["Language"]
    data["country"] = body["Country"]
    data["awards"] = body["Awards"]

    data["imdb"] = {
        "rating": body["imdbRating"],
        "votes": body["imdbVotes"],
        "imdb_id": body["imdbID"] 
    }

    data["type"] = body["Type"]

    if data["type"].lower() == "series":
        try:
            data["num_of_seasons"] = int(body["totalSeasons"])
        except:
            # if i can't get # of seasons, I won't return the result for now
            return {}

        data["episodes"] = get_episodes(data["title"], data["num_of_seasons"])

        if not data["episodes"]:
            # if i can't get # of seasons, I won't return the result for now
            return {}

    return data

def get_episodes(title, num_of_seasons):
    """
    get all episodes for a given show or series
    """
    episodes = []

    for i in range(num_of_seasons):
        response = requests.get(url="%s?t=%s&Season=%s&apikey=%s" % (API_URL, title, str(i+1), API_KEY))

        if response.status_code != 200:
            return []

        body = response.json()

        if body["Response"] != "True":
            return []

        print(body)

        for episode in body["Episodes"]:
            if episode["imdbRating"].lower() == "n/a":
                continue

            episodes.append({
                "title": episode["Title"],
                "released": episode["Released"],
                "episode": episode["Episode"],
                "imdb": {
                    "rating": episode["imdbRating"],
                    "imdb_id": episode["imdbID"]
                },
                "season": i+1
            })

    return episodes