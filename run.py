import asyncio
import discord
import shelve
import config
import random
import copy
import re
from gif import Gif

global reactions
reactions = {}

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
    print('Logged in as')
    print(client.user.name)
    print('---------')
    with shelve.open(config.dbPath) as db:
        if ("gifs" in db):
            reactions = db["gifs"]
        else:
            db["gifs"] = reactions
    global idnumber
    idnumber = client.user.id




@client.event
async def on_message(message):
    global reactions
    global deletion
    global idnumber
    messageContent = message.content
    messageContent = re.sub('\s+',' ',messageContent)
    splitMessage = messageContent.split(" ")
    if (message.content.startswith("+")):
        if (message.content.startswith("+f ")):
            if (len(message.mentions) != 0):
                out = "**SENDER** has paid their respects for **RECIEVER** :"
                out = out.replace("RECIEVER",
                        message.mentions[0].display_name)
                out = out.replace("SENDER", message.author.display_name)
                out = out + config.hearts[random.randint(0,len(config.hearts))]
                out += ":"
                await message.channel.send(out)
            else:
                out = "**SENDER** has paid their respects for **RECIEVER** :"
                reciev = ""
                for i in range(1,len(splitMessage)):
                    reciev += splitMessage[i]
                out = out.replace("RECIEVER",
                        reciev)
                out = out.replace("SENDER", message.author.display_name)
                out = out + config.hearts[random.randint(0,len(config.hearts))]
                out += ":"
                await message.channel.send(out)


        cmd = message.content.split()[0][1:]
        if (len(message.mentions) != 0):
            if (message.mentions[0].id == message.author.id):
                out = discord.Embed()
                out.description = config.selfMessage.replace("SENDER",
                        message.author.display_name)
                out.set_image(url=config.selfImage)
                await message.channel.send(embed=out)
            else:
                if (cmd in reactions):
                    tags = []
                    if (len(splitMessage) >= 3):
                        for i in range(2, len(splitMessage)):
                            tags.append(splitMessage[i])

                    send = getMessage(message.author, message.mentions[0], cmd,
                            getGif(cmd, tags))
                    await message.channel.send(embed=send)

    if (message.content.startswith("<@!" + str(idnumber) + ">") or
            message.content.startswith("<@" + str(idnumber) + ">")):
        if (splitMessage[1] == "verbs"):
            if (len(reactions.keys()) == 0):
                await message.channel.send("No verbs found! Add some!")
            else:
                out = "List of verbs:\n```\n"
                for key in reactions.keys():
                    out+= "+" + key + "\n"
                out+="```"
                snd = discord.Embed()
                snd.description = out

                await message.channel.send(embed=snd)

        if(splitMessage[1] == "tags"):
            gifs = reactions[splitMessage[2]]
            tags = {}
            for i in gifs:
                for x in i.tags:
                    print ("|" + x + "|")
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

            await message.channel.send(out)

        if(splitMessage[1] == "help"):
            out = discord.Embed()
            out.description = config.helpMessage
            await message.channel.send(embed=out)
        if(splitMessage[1] == "choose"):
            unsplit = message.content
            unsplit = unsplit[len("<@!" + str(idnumber) + "> choose "):]
            print(unsplit)
            split = unsplit.split("|")
            choice = split[random.randint(0, len(split) - 1)]
            await message.channel.send("**" +
                    message.author.display_name + "**" +
            ", **" + choice.strip() + "** is the best choice")


        if(splitMessage[1] == "add"):
            if (message.author.id not in config.admins):
                await message.channel.send("You are not an admin!")

            else:
                newGif = Gif()

                newGif.url=splitMessage[3]
                for i in range(4, len(splitMessage)):
                    newGif.tags.append(splitMessage[i])
                if (splitMessage[2] in reactions.keys()):
                    reactions[splitMessage[2]].append(newGif)
                    await message.channel.send("Added the image!")
                else:
                    reactions[splitMessage[2]] = [newGif]
                    await message.channel.send("Created the verb and added the image!")
                with shelve.open(config.dbPath) as db:
                    db["gifs"] = reactions
        if(splitMessage[1] == "delete"):
            if (message.author.id not in config.admins):
                await message.channel.send("You are not an admin!")
            else:
                if (splitMessage[2] == "verb"):
                    await message.channel.send("Are you sure you want to \
delete the verb? Respond with ```\n@Shleep Bot I'm \
sure!\n```")
                    deletion = [True, splitMessage[3]]
                if (splitMessage[2] == "gif"):
                    count = 0
                    shad = copy.deepcopy(reactions[splitMessage[3]])
                    print(len(shad))
                    for i in range(0,len(shad)):
                        print(i)
                        if (shad[i].url ==
                                splitMessage[4]):
                            del reactions[splitMessage[3]][i - count]
                            count += 1
                    if (count > 0):
                        await message.channel.send("Succesfully deleted the \
image!")
                    else:
                        await message.channel.send("No such image \
found!")

                with shelve.open(config.dbPath) as db:
                    db["gifs"] = reactions


    if ((message.content == "<@!" + str(idnumber) + "> I'm sure!" or
          message.content == "<@" + str(idnumber) + "> I'm sure!")  and
            deletion[0]):
        reactions.pop(deletion[1], None)
        await message.channel.send("Deleted the " +
            deletion[1] + " verb!")
        deletion = [False, None]
        with shelve.open(config.dbPath) as db:
            db["gifs"] = reactions

client.run(config.token)
