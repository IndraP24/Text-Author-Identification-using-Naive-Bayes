import requests
import pandas as pd
from bs4 import BeautifulSoup
import re

# Create a test set 
# To evaluate the performance of our classifier, scrape dialogues of Cap and Iron Man from Captain America: Civil War
endgameURL = "https://transcripts.fandom.com/wiki/Avengers:_Endgame"
endgamePage = requests.get(endgameURL)
endgameParsedPage = BeautifulSoup(endgamePage.text, "html.parser")

endgameDialogues = endgameParsedPage.find_all("p")
endgame_dialogues = []

for dialogue in endgameDialogues:

    t = dialogue.find("b")

    if t:
        if t.text in ["TONY STARK:"]:
            dialg = dialogue.text.replace("TONY STARK:", "").strip()
            dialg = re.sub(pattern = r"\[.+\]", repl = "", string = dialg)
            endgame_dialogues.append([dialg, "Iron Man"])
        elif t.text in ["STEVE ROGERS:"]:
            dialg = dialogue.text.replace("STEVE ROGERS:", "").strip()
            dialg = re.sub(pattern = r"\[.+\]", repl = "", string = dialg)
            endgame_dialogues.append([dialg, "Captain America"])
            
df = pd.DataFrame(endgame_dialogues, columns = ["Dialogue", "Speaker"])
df.to_csv("../../data/test.csv", index = False)
print("File is saved in Data folder!")