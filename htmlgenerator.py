import os
import time
from datetime import datetime
from dataclasses import dataclass
from typing import List

from jinja2 import Environment, FileSystemLoader, select_autoescape
from datamodels import car
from glob import glob

env = Environment(
    loader=FileSystemLoader('templates'),
    autoescape=select_autoescape(['html', 'xml'])
)
menu_template = env.get_template('menu.html')
delta_template = env.get_template('delta.html')

def epoch2timestamp(ts):
    return datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")

def diffString(changes: List[car]):
    diffStr = "_a" + str(len(changes))
    diffStr += "_n" + str(len([x for x in changes if x.reason == 'new']))
    diffStr += "_c" + str(len([x for x in changes if x.reason == 'changed']))
    diffStr += "_d" + str(len([x for x in changes if x.reason == 'deleted']))
    return diffStr

def generateDelta(dirpath: str, changes: List[car], results: List[car]):
    dfilename = dirpath + "/" + str(time.time()) + diffString(changes) + ".html"

    with open(dfilename[:-5] + ".full.html", "w+", encoding="utf-8") as full_delta_file:
        full_delta_file.write(delta_template.render(changes=results))

    with open(dfilename, 'w+', encoding='utf-8') as delta_file:
        delta_file.write(delta_template.render(changes=changes))

def decodeDiffStr(i):
    chArr = list(map(lambda x: x[1:], i.split("_")))
    retStr = ""
    if int(chArr[1]) > 0: retStr += chArr[1] + " new, "
    if int(chArr[2]) > 0: retStr += chArr[2] + " changed, "
    if int(chArr[3]) > 0: retStr += chArr[3] + " deleted, "
    if len(retStr) > 0: retStr = " (" + retStr[:-2] + ")"
    return chArr[0] + " items" + retStr

@dataclass
class ChangeSet:
    def __init__(self, file_path: str) -> None:
        self.delta_path = file_path
        self.full_path = f'{file_path[:-5]}.full.html'
        nameStr = file_path[file_path.find("data_") :].split("\\")[-1][:-5]
        self.link_text = epoch2timestamp(float(nameStr.split("_", 1)[0]))
        self.diff_text = decodeDiffStr(nameStr.split("_", 1)[1])

@dataclass
class MenuItem:
    query: str
    htmls: List[ChangeSet]


def get_menu_items() -> List[MenuItem]:
    dirs = glob("data_*/")
    menu_items: List[MenuItem] = []
    for directory in dirs:
        query_name = directory.split("data_")[-1][:-1]

        allhtmls = glob(directory + "*.html")[::-1]
        htmls = sorted(filter(lambda h: not h.endswith("full.html"), allhtmls))
        change_sets: List[ChangeSet] = list(map(ChangeSet, htmls))
        menu_items.append(MenuItem(query_name, change_sets))

    return menu_items


def generateMenu():
    menu_items = get_menu_items()

    with open(os.getcwd() + "/menu.html", "w+", encoding="utf-8") as menu_file:
        menu_file.write(
            menu_template.render(menu_items=menu_items)
        )
