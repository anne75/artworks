#!/usr/bin/python3
"""
This is module make_tweet
In this module I load a json file of urls to request to make a tweet
"""
import requests
import json
import random
import tweepy
import os
from twitter_api import ck, cs, at, ats

def met(r):
    """get image url, title and name from Met request"""
    image_url = r.get("image")
    if image_url is None:
        if r.get("source") is not None:
            image_url = r.get("source").get("href")
    image_name = r.get("name")
    image_artist = r.get("Who")
    return image_url, image_name, image_artist

def tate(r):
    """get image url, title and name from Tate request"""
    image_name = r.get("title")
    image_artist = r.get("all_artists")
    if r.get("thumbnailUrl") is not None:
        return (r.get("thumbnailUrl"), image_name, image_artist)
    if r.get("image") is not None:
            return (r.get("image"), image_name, image_artist)
    if loaded.get("url") is not None:
        return (r.get("url"), image_name, image_artist)

def get_content():
    """
    grabs valid image url, title and name from file.
    if an image url is missing, the url is removed from the list
    """
    with open("url_list.json", mode="r", encoding="utf-8") as f:
        urls = json.load(f)
    image_url = None
    to_remove = False
    while image_url is None:
        if to_remove:
            urls.remove(to_read)
        else:
            to_remove = True
        to_read = urls[random.randrange(0, len(urls))]
        print(to_read)
        r = requests.get(to_read[1]).json()
        if to_read[0] == "Met":
            image_url, image_name, image_artist = met(r)
        else:
            image_url, image_name, image_artist = tate(r)
    with open("url_list.json", mode="w", encoding="utf-8") as f:
        json.dump(urls, f)
    return to_read[0], image_url, image_name, image_artist

def make_content(museum, image_url, image_name, image_artist, filename):
    """
    makes a message and download an image
    """
    message = "From the " + museum
    # if image_name is not None:
    #    message += " with title " + image_name
    if image_artist is not None:
        message += " by " + image_artist

    r = requests.get(image_url)
    if r.status_code == 200:
        with open(filename, mode="wb") as image:
            for chunk in r:
                image.write(chunk)
    else:
        return None
    return (message)


if __name__ == "__main__":
    filename = "image.jpg"
    message = make_content(*get_content(), filename)
    auth = tweepy.OAuthHandler(ck, cs)
    auth.set_access_token(at, ats)
    api = tweepy.API(auth)
    print("ERROR")
    try:
        api.update_with_media(filename, status=message)
    except tweepy.error.TweepError as e:
        api.update_status(e.message)
    finally:
        os.remove(filename)
