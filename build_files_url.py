#!/usr/bin/python3
"""
This is module build_files_url.
This module creates lists of urls redirecting to json files containing art work
metadata.
Then, it takes those lists and dumps them in a json file
"""
import os
import json


def met_list():
    """
    Met open data.
    Create a list of urls from a base url and cloned repo
    """
    base_url = "https://raw.githubusercontent.com/metmuseum-medialab/\
collections-data/master/data/"
    path = "/home/anne/Pictures/Met_data/data"
    files = os.listdir(path)
    met_list = [["Met", "{}{}".format(base_url, x)] for x in files]
    return met_list

def tate_list():
    """
    Tate open data.
    Create a list of urls from a base url and cloned repo.
    """
    base_url = "https://raw.githubusercontent.com/tategallery/\
collection/master/artworks/" # like d/242/d24201-51538.json
    path = "/home/anne/Pictures/Tate_data/artworks"
    paths = []
    for root, dirs, files in os.walk(path):
        paths += [["Tate", "{}{}/{}".format(
            base_url, root.split("artworks/")[1], x)] for x in files]
    return paths

def moma_list():
    """
    MOMA open data
    The MOMA open data is in a unique json file. This file is
    parsed to return ("MOMA", <artist>, <thumbnail_url>)
    """
    all = []
    with open("/home/anne/Pictures/MOMA_Artworks.json") as f:
        data = json.load(f)
    for dico in data:
        if dico.get("ThumbnailURL") is not None:
            print(dico)
            all.append(["MOMA", dico.get("ThumbnailURL"),
                        dico.get("Title"), dico.get("Artist")])
    return all

if __name__ == "__main__":
    with open("url_list.json", mode="w", encoding="utf-8") as f:
        json.dump(met_list() + tate_list() + moma_list(), f)
