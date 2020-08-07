import yaml
import shelve
import config
from gif import Gif
import datetime

def backup():
  reactions = {}
  with shelve.open(config.dbPath) as db:
    reactions = db["gifs"]
  x = datetime.datetime.now()
  with open(config.backupPath + x.strftime("%m-%d-%y") + ".yml", "w") as file:
    yaml.dump(reactions, file)
  return config.backupPath + x.strftime("%m-%d-%y") + ".yml"

def reload(fileName):
  reactions = {}
  with open(config.backupPath + fileName, "r") as file:
    reactions = yaml.full_load(file)


def main():
  backup()

if __name__ == "__main__":
  main()


