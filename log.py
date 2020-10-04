import config
import sys
import time

def log(message):
    current = time.localtime(time.time())
    with open(config.backupPath + 'log.txt', 'a') as f:
        text = str(current.tm_hour) + ":" + str(current.tm_min) + " | " + message
        f.write(text)
        f.write('\n')
