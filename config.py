dbPath = "storage/storage.db"
backupPath = "storage/"
token = "token"
admins = [156903320945033216]

message = "**RECIEVER**, you got a VERB from **SENDER**"

selfMessage = "**SENDER**, please don't do that to yourself..."
selfImage = "https://wallpapercave.com/wp/wp2098611.jpg"
selfHarmVerbs = ["kill", "slash", "punch", "stab", "shoot", "murder", "smack", "bonk"]

noGifFound = "https://wallpapercave.com/wp/wp2098611.jpg"


hearts = ["heart", "purple_heart", "white_heart", "green_heart", "yellow_heart", "black_heart", "brown_heart", "blue_heart", "orange_heart", "heartpulse", "sparkling_heart", "gift_heart", "cupid"]

helpMessage = "Mention Commands:\n\
```\n\
@Shleep Bot help\n\
    - Posts this message\n\
@Shleep Bot verbs\n\
    - Lists all verbs\n\
@Shleep Bot tags <verb>\n\
    - List all tags within a verb\n\
@Shleep Bot choose <choice> | <choice> | <choice>\n\
    - Choose from any number of choices!\n\
@Shleep Bot eightball <question>\n\
    - Let Shleep Bot answer all your toughest inquiries\n\
@Shleep Bot convertc2f <num>\n\
    - Convert Celsius to Farenheit\n\
@Shleep Bot convertf2c <num>\n\
    - Convert Farenheit to Celsius\n\
```\n\
Admin Commands:\n\
```\n\
@Shleep Bot add <verb> <url> [all tags]\n\
    - Adds an image, connected to a verb and tags\n\
@Shleep Bot delete verb <verb>\n\
    - Deletes a verb and all images contained within!\n\
@Shleep Bot delete gif <verb> <url>\n\
    - Deletes a gif with the given verb + url\n\
@Shleep Bot synonym: <verb1> <verb2>\n\
    - Creates a \"synonym\" of verb1, verb2\n\
@Shleep Bot dump\n\
    - Posts a yaml file of the current database\n\
@Shleep Bot prune\n\
    - Deletes any duplicate gifs, and merges tags!\n\
```\n\
\n\
You can run any verb command with:\n\
```\n\
+<verb> @Recipient [all tags]\n\
```\n\
\n\
Special Commands:\n\
```\n\
+f <@Recipient>\n\
    - Pays your respect to someone\n\
```\n\
\n\
[] means optional"


eightballMessages = [ "Senpai, pls no ;-;", "Take a wild guess...",
        "Without a doubt", "No", "Yes", "You'll be the judge", "Sure",
        "Of course", "No way", "No... (╯°□°）╯︵ ┻━┻", "Very doubtful",
        "Most likely", "Might be possible" ]
eightballMessage = ":8ball: **Question:** QUESTION\n\
**Answer:** ANSWER"
