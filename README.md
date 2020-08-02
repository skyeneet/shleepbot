# Shleep Bot

A replacement for Kawaii Bot, 100% homegrown and organic!

## How to Setup

The first thing you have to do is place your bot token into the config
file, which is ``config.py``. Then, you'll want to add discord ID to the
``admins`` array within that config file, you can get this by turning on
Developer Mode under "Appearance" in discord, and then just right
clicking your profile and choosing "copy ID."

## How to Run

Shleep Bot requires python 3, as well as discord.py to run. Once you
have those, simply run the ``run.py`` file and you're good to go!

If you're interested in running it via docker, a Dockerfile is provided,
and a docker-compose file is available below. If you don't use the
provided docker-compose, make sure your volumes are setup correctly, as
/shleepbot/storage has data that must be kept persistently.

## How to Use

Most Shleep Bot commands can be found by sending the message:

```
@Shleep Bot help
```

While Shleep Bot is running.

### Verbs

Most Shleep Bot commands will be "verbs," which can be accessed with the
command:
```
+<verb> <@Recipient> [tags]
```
This will post a gif associated with the verb, along with a message.

#### Setup

By default, Shleep Bot does not have any verbs. Instead, an admin must
add verbs and gifs with the following command:

```
@Shleep Bot add <verb> <url> [tags]
```

They can also be removed with these commands:
```
@Shleep Bot delete verb <verb>
@Shleep Bot delete gif <verb> <url>
```
The first will delete ALL gifs in a verb, so it will ask for
confirmation before doing anything.

### Tags

Any gif can be "tagged," which allows you to add identifiers to any gif.
For example, you might add "yuri," "yaoi," "fun," "sad," or "comforting," to a hug
gif. Any gif can have any number of emotes, separated with a space at
the end of the add command.

To use a given tag, simply add it to the end of a verb command, like so:
```
+hug @skyenet fun yuri
```
Only gifs with the "fun" and "yuri" tags will be chosen.

## Example docker-compose.yml

```
version: "2"
services:
  shleepbot:
    image: shleepbot
    container_name: shleep
    environment:
      - PUID = 1000
      - PGID = 1000
    volumes:
      - /srv/shleepbot:/shleepbot/storage
    restart: unless-stopped
    build: /path/to/repo
```
