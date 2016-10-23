#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, sys, re, json
import argparse
import logging
import requests

def checkParam(parm):
    "Return a valid parameter"
    if parm:
        return ''.join(parm)
    return None

def isAccessible(url):
    "Check if linke is accessible"
    logging.debug('checking url: ' + url)

    if requests.get(url).status_code == 404:
        return False
    return True

def configLog(debug):
    "Configure logging"
    logfile = os.path.basename(__file__).replace('.py', '.log') if debug == True else None
    loglevel = logging.DEBUG if logfile is not None else None
    logging.basicConfig(format='%(asctime)s [%(levelname)8s][%(module)18s][Line %(lineno)3d] %(message)s', filename=logfile, level=loglevel)

def generateLuckyName(url):
    "Generate an available name randomly"
    while True:
        luckyName = requests.get('http://www.shittyusernames.com/api/get-username').text
        logging.debug('luckyName: ' + luckyName)
        if not isAccessible(url + luckyName):
            if len(luckyName) <= 15:
                print('No available username according to your inputs. But don\'t be sad...')
                print('Found a lucky name for you: ' + luckyName)
                sys.exit(1)

# Setup parameter
#   run script with -d, active debug mode (log file will be created)
parser = argparse.ArgumentParser()
parser.add_argument('-n',   '--name',     default=None, help='your name')
parser.add_argument('-s',   '--surname',  default=None, help='your surname')
parser.add_argument('-nn',  '--nickname', default=None, help='your nickname')
parser.add_argument('-l',   '--like',     default=None, help='what are you like')
parser.add_argument('-w',   '--word',     default=None, help='important word')
parser.add_argument('-num', '--number',   default=None, help='your fav number')
parser.add_argument('-d',   '--debug',    action='store_true', dest="debug", help='active debug log')
args = parser.parse_args()

# Config logging
configLog(args.debug)

# Define variable
#   url: name generator url
#   turl: twitter url
#   params: Post parameters
url    = 'http://twitternamegenerator.com/generate'
turl   = 'https://twitter.com/'
params = {
    'inputInfo[name]'     : checkParam(args.name),
    'inputInfo[surname]'  : checkParam(args.surname),
    'inputInfo[nickname]' : checkParam(args.nickname),
    'inputInfo[like]'     : checkParam(args.like),
    'inputInfo[word]'     : checkParam(args.word),
    'inputInfo[number]'   : checkParam(args.number)
}
#   remove None value item
params = dict((k, v) for k, v in params.items() if v)
logging.debug('url: ' + url)
logging.debug('twitter url: ' + turl)
logging.debug('params: ' + str(params))

# Create http request
r = requests.post(url, data=params)
if r.status_code != 200:
    generateLuckyName(turl)

nameList = []
for n in json.loads(r.text):
    if 'str' in str(type(n)):
        if not isAccessible(turl + n):
            if n not in nameList:
                nameList.append(n)

# Print results
print('\n'.join(nameList)) if len(nameList) > 0 else generateLuckyName(turl)
