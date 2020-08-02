import shelve
from gif import Gif

path = input("What text file? ")

f = open(path, "r")

reactions = {}
with shelve.open("gifs.db") as db:
    if ("gifs" in db):
        reactions = db["gifs"]
    else:
        db["gifs"] = reactions

for line in f:
    split = line.split(" ")
    if (split[0] not in reactions):
        reactions[split[0]] = []
    newGif = Gif()
    newGif.url = split[1]
    for i in range (2, len(split)):
        newGif.tags.append(split[i].strip())
    reactions[split[0]].append(newGif)




with shelve.open("gifs.db") as db:
    db["gifs"] = reactions
