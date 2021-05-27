import requests
import pandas as pd
from bs4 import BeautifulSoup
import re

# Create train dataset
# Extract all dialogues of Steve Rogers from Captain America: The First Avenger

# Get the html body of the transcript page from fandom
capURL = "https://transcripts.fandom.com/wiki/Captain_America:_The_First_Avenger"
capPage = requests.get(capURL)

# Parse the html through beautiful soup and find the tag which contains dialogues
capParsedPage = BeautifulSoup(capPage.text, "html.parser")
dialogues = capParsedPage.find_all("dd")

# Parse through all dialogues and only pick those dialogues which are spoken by Captain America
captain_dialogues = []
for dialogue in dialogues:
    t = dialogue.find("b")
    if t:
        if t.text in ["Steve Rogers", "Steve Rogers:"]:
            dialg = dialogue.text.replace("Steve Rogers:", "").strip()
            dialg = re.sub(pattern = r"\[.+\]", repl = "", string = dialg)
            captain_dialogues.append(dialg)

# Repeat the process above for Iron Man transcripts
starkURL = "https://transcripts.fandom.com/wiki/Iron_Man"
starkPage = requests.get(starkURL)
starkParsedPage = BeautifulSoup(starkPage.text, "html.parser")

starkDialogues = starkParsedPage.find_all("p")
stark_dialogues = []

for dialogue in starkDialogues:
    t = dialogue.find("b")
    if t:
        if t.text in ["Tony Stark", "Tony Stark:"]:
            dialg = dialogue.text.replace("Tony Stark:", "").strip()
            dialg = re.sub(pattern = r"\[.+\]", repl = "", string = dialg)
            stark_dialogues.append(dialg)

# Create a dataframe to bunch the data and keep it together
all_dialogues = captain_dialogues + stark_dialogues
target_variable = ["Captain America"] * len(captain_dialogues) + ["Iron Man"] * len(stark_dialogues)

df = pd.DataFrame({"Dialogue": all_dialogues, "Speaker": target_variable})
df.to_csv("../../data/train.csv", index = False)
print("Train file is saved under the data folder!")