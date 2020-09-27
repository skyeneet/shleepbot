import asyncio
import discord
import shelve
import config
import random
import copy
import datetime
import re
import backup
from gif import Gif

global reactions
reactions = {}

global synonyms
synonyms = {}

global idnumber
idnumber = 0

client = discord.Client()

global deletion
deletion = [False, None]

def getGif(verb, tags):
    global reactions
    gifs = reactions[verb]
    if (verb in reactions.keys()):
        if (tags != []):
            newGifs = []
            for i in gifs:
                if (all(item in i.tags for item in tags)):
                    newGifs.append(i)
            gifs = newGifs

        if (len(gifs) == 0):
            out = Gif()
            out.url = config.noGifFound
            return out
        else:
            return gifs[random.randint(0, len(gifs) - 1)]

def getMessage(sender, reciever, verb, gif):
    out = discord.Embed()
    senderName = sender.display_name
    recieverName = reciever.display_name
    msg = config.message
    msg = msg.replace("RECIEVER", recieverName)
    msg = msg.replace("SENDER", senderName)
    msg = msg.replace("VERB", verb)
    out.description = msg
    out.set_image(url=gif.url)

    return out

@client.event
async def on_ready():
    global reactions
    global synonyms
    print('Logged in as')
    print(client.user.name)
    print('---------')
    with shelve.open(config.dbPath) as db:
        if ("gifs" in db.keys()):
            reactions = db["gifs"]
        else:
            db["gifs"] = reactions
    global idnumber
    idnumber = client.user.id

def verbCommand(message, splitMessage):
    cmd = splitMessage[0][1:]
    if (len(message.mentions) != 0):
        if (message.mentions[0].id == message.author.id and
                cmd in config.selfHarmVerbs):
            out = discord.Embed()
            out.description = config.selfMessage.replace("SENDER",
                    message.author.display_name)
            out.set_image(url=config.selfImage)
            return None, out
        else:
            if (cmd in reactions):
                tags = []
                if (len(splitMessage) >= 3):
                    for i in range(2, len(splitMessage)):
                        tags.append(splitMessage[i])

                send = getMessage(message.author, message.mentions[0], cmd,
                        getGif(cmd, tags))
                return None, send

def fCommand(message, splitMessage):
    if (len(message.mentions) != 0):
        out = "**SENDER** has paid their respects for **RECIEVER** :"
        out = out.replace("RECIEVER",
                message.mentions[0].display_name)
        out = out.replace("SENDER", message.author.display_name)
        out = out + config.hearts[random.randint(0,len(config.hearts))]
        out += ":"
        return out, None
    else:
        if (len(splitMessage) > 1):
            out = "**SENDER** has paid their respects for **RECIEVER** :"
        else:
            out = "**SENDER** has paid their respects :"
        reciev = ""
        for i in range(1,len(splitMessage)):
            reciev += splitMessage[i] + " "
        out = out.replace("RECIEVER",
                reciev)
        out = out.replace("SENDER", message.author.display_name)

        out = out + config.hearts[random.randint(0,len(config.hearts))]

        out += ":"
        return out, None

def verbsCommand(message, splitMessage):
    if (len(reactions.keys()) == 0):
        return "No verbs found! Add some!", None
    else:
        out = "List of verbs:\n```\n"

        allFound = []

        for category in reactions.keys():

            found = False
            for i in allFound:
                if (i[0] is reactions[category]):
                    i[1].append(category)
                    found = True
                    break

            if (not found):
                allFound.append([reactions[category], [category]])

        lines = []
        for nm in allFound:
            line = ""
            for i in nm[1]:
                line += "+" + i +  "   "

            line += "\n"
            lines.append(line)
        lines.sort()
        for i in lines:
            out += i

        out+="```"
        snd = discord.Embed()
        snd.description = out

        return None, snd

def tagsCommand(message, splitMessage):
    gifs = reactions[splitMessage[2]]
    tags = {}
    for i in gifs:
        for x in i.tags:
            if (x not in tags):
                tags[x] = 1
            else:
                tags[x] = tags[x] + 1
    out = "Availble tags for " + splitMessage[2] + ":\n```\n"
    for i in tags.keys():
        num = 4 - len(str(tags[i]))
        for n in range(0,num):
            out+=" "
        out+="("
        out+=str(tags[i])
        out+=")  " + i + "\n"
    out+="```"
    return out, None

def helpCommand(message, splitMessage):
    out = discord.Embed()
    out.description = config.helpMessage
    return None, out

def chooseCommand(message, splitMessage):
    unsplit = message.content
    if (len(splitMessage[0]) == len("<@!" + str(idnumber) + ">")):
        unsplit = unsplit[len("<@!" + str(idnumber) + "> choose "):]
    else:
        unsplit = unsplit[len("<@" + str(idnumber) + "> choose "):]
    split = unsplit.split("|")
    choice = split[random.randint(0, len(split) - 1)]
    out = ("**" + message.author.display_name + "**" +
    ", **" + choice.strip() + "** is the best choice")

    return out, None

def altChooseCommand(message, splitMessage):
    unsplit = message.content
    if (len(splitMessage[0]) == len("<@!" + str(idnumber) + ">")):
        unsplit = unsplit[len("<@!" + str(idnumber) + ">"):]
    else:
        unsplit = unsplit[len("<@" + str(idnumber) + ">"):]
    split = unsplit.split("|")
    choice = split[random.randint(0, len(split) - 1)]
    out = ("**" + message.author.display_name + "**" +
    ", **" + choice.strip() + "** is the best choice")

    return out, None


def eightballCommand(message, splitMessage):
    question = ""
    for i in range (2, len(splitMessage)):
        question += splitMessage[i] + " "
    answer = config.eightballMessages[random.randint(0,len(config.eightballMessages))]
    out = config.eightballMessage
    out = out.replace("QUESTION", question)
    out = out.replace("ANSWER", answer)
    return out, None

def addCommand(message, splitMessage):
    if (message.author.id not in config.admins):
        out = "You are not an admin!"
        return out, None

    else:
        newGif = Gif()

        newGif.url=splitMessage[3]
        for i in range(4, len(splitMessage)):
            newGif.tags.add(splitMessage[i])
        if (splitMessage[2] in reactions.keys()):
            reactions[splitMessage[2]].append(newGif)
            out = "Added the image!"
        else:
            reactions[splitMessage[2]] = [newGif]
            out = "Created the verb and added the image!"
        with shelve.open(config.dbPath) as db:
            db["gifs"] = reactions
        return out, None

def deleteCommand(message, splitMessage):
    global deletion
    if (message.author.id not in config.admins):
        out = "You are not an admin!"
    else:
        if (splitMessage[2] == "verb"):
            out = "Are you sure you want to \
delete the verb? Respond with ```\n@Shleep Bot I'm \
sure!\n```"
            deletion = [True, splitMessage[3]]
        if (splitMessage[2] == "gif"):
            count = 0
            shad = copy.deepcopy(reactions[splitMessage[3]])
            for i in range(0,len(shad)):
                if (shad[i].url ==
                        splitMessage[4]):
                    del reactions[splitMessage[3]][i - count]
                    count += 1
            if (count > 0):
                out = "Succesfully deleted the \
image!"
            else:
                out = "No such image \
found!"

        with shelve.open(config.dbPath) as db:
            db["gifs"] = reactions
    return out, None

def deleteVerify(message, splitMessage):
    global deletion
    reactions.pop(deletion[1], None)
    out = "Deleted the " + deletion[1] + " verb!"
    deletion = [False, None]

    with shelve.open(config.dbPath) as db:
        db["gifs"] = reactions

    return out, None

def pruneCommand(message, splitMessage):
    global reactions
    totalCount = 0
    for i in reactions:
        allUrls = {}
        dups = []
        for x in range(0,len(reactions[i])):
            if (type(reactions[i][x].tags) is list):
                reactions[i][x].tags = set(reactions[i][x].tags)

            if (reactions[i][x].url not in allUrls.keys()):
                allUrls[reactions[i][x].url] = x
            else:
                totalCount += 1
                dups.append([x,reactions[i][x].tags])

        tempCount = 0
        for x in dups:
            og = allUrls[reactions[i][x[0] - tempCount].url]
            reactions[i][og].tags = reactions[i][og].tags.union(
                    reactions[i][x[0] - tempCount].tags)
            del reactions[i][x[0] - tempCount]
            tempCount += 1

    with shelve.open(config.dbPath) as db:
        db["gifs"] = reactions

    out = "I deleted COUNT duplicates and merged tags!"
    out = out.replace("COUNT", str(totalCount))
    return out, None

def convertc2f(message, splitMessage):
    out = "**CEL**°C, in a reasonable temperature scale, is **FAR**°F"
    cel = int(splitMessage[2])
    far = 9.0/5.0 * cel + 32
    out = out.replace("CEL", str(cel))
    out = out.replace("FAR", str(far))

    return out, None

def convertf2c(message, splitMessage):
    out = "**FAR**°F, in a less reasonable temperature scale, is **CEL**°C"
    far = int(splitMessage[2])
    cel = (far - 32) * 5.0/9.0
    out = out.replace("CEL", str(cel))
    out = out.replace("FAR", str(far))

    return out, None

def synonymCommand(message, splitMessage):
    global reactions
    out = "Succesfully made a synonym of **OG**, **NEW**!"
    reactions[splitMessage[3]] = reactions[splitMessage[2]]
    out = out.replace("OG", splitMessage[2])
    out = out.replace("NEW", splitMessage[3])
    with shelve.open(config.dbPath) as db:
        db["gifs"] = reactions
    return [out, None]


@client.event
async def on_message(message):
    global reactions
    global deletion
    global idnumber
    out = tuple([None, None])
    messageContent = message.content
    messageContent = re.sub(r'\s+',' ',messageContent)
    splitMessage = messageContent.split(" ")
    if (message.content.startswith("+")):
        if (splitMessage[0] == "+f"):
            out = fCommand(message, splitMessage)
        else:
            out = verbCommand(message, splitMessage)

    elif (message.content.startswith("<@!" + str(idnumber) + ">") or
            message.content.startswith("<@" + str(idnumber) + ">")):
        if (splitMessage[1] == "verbs"):
           out = verbsCommand(message, splitMessage)

        elif(splitMessage[1] == "tags"):
            out = tagsCommand(message, splitMessage)

        elif(splitMessage[1] == "help"):
            out = helpCommand(message, splitMessage)

        elif(splitMessage[1] == "choose"):
            out = chooseCommand(message, splitMessage)

        elif (splitMessage[1] == "eightball"):
           out = eightballCommand(message, splitMessage)

        elif (splitMessage[1] == "convertc2f"):
           out = convertc2f(message, splitMessage)

        elif (splitMessage[1] == "convertf2c"):
           out = convertf2c(message, splitMessage)

        elif(splitMessage[1] == "add"):
            out = addCommand(message, splitMessage)

        elif(splitMessage[1] == "delete"):
            out = deleteCommand(message, splitMessage)

        elif(splitMessage[1] == "synonym"):
            out = synonymCommand(message, splitMessage)

        elif(splitMessage[1] == "prune"):
            out = pruneCommand(message, splitMessage)

        elif(splitMessage[1] == "dump"):
            if (message.author.id not in config.admins):
                out = "You are not an admin!"
            else:
                path = backup.backup()
                with open(path, "r") as f:
                    wrap = discord.File(f)
                    await message.channel.send(file=wrap)

    if ((message.content == "<@!" + str(idnumber) + "> I'm sure!" or
          message.content == "<@" + str(idnumber) + "> I'm sure!")  and
            deletion[0]):
            out = deleteVerify(message, splitMessage)

    if (out != None and (out[0] == None and out[1] == None and
            "|" in  message.content)):

        if (message.content.startswith("<@!" + str(idnumber) + ">") or
            message.content.startswith("<@" + str(idnumber) + ">")):
            out = altChooseCommand(message,splitMessage)

    if (out != None and (out[0] != None or out[1] != None)):
        try:
            await message.channel.send(out[0], embed = out[1])
        except IndexError:
            pass

client.run(config.token)
