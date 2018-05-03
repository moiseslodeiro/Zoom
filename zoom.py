#!/usr/bin/env python

# Required modules
import argparse
import requests
import re
import json

# Just some colors and shit bro
white = '\033[97m'
green = '\033[1;32m'
red = '\033[1;31m'
yellow = '\033[1;33m'
end = '\033[1;m'
info = '\033[1;33m[!]\033[1;m'
que =  '\033[1;34m[?]\033[1;m'
bad = '\033[1;31m[-]\033[1;m'
good = '\033[1;32m[+]\033[1;m'
run = '\033[1;97m[~]\033[1;m'

parser = argparse.ArgumentParser() # defines the parser
parser.add_argument('-u', '--url', help='Target wordpress website') # Adding argument to the parser
args = parser.parse_args() # Parsing the arguments

print ('''%s  ____                
 /_  / ___  ___  ____ 
  / /_/ %s_ \/ _%s \/    \\
 /___/\___%s/\%s___/_/_/_/%s\n''' % (yellow, white, yellow, white, yellow, end))

usernames = [] # List for storing found usernames

def metagenerator(url):
    response = requests.get(url).text
    match = re.search(r'<meta name="generator" content="WordPress .*" />', response)
    if match:
        version_dec = match.group().split('<meta name="generator" content="WordPress ')[1][:-4]
        return [version_dec.replace('.', ''), version_dec]
    else:
        print ('%s Target doesn\'t seem to use WordPress' % bad)

def version_vul(version, version_dec):
    response = requests.get('https://wpvulndb.com/api/v3/wordpresses/%s' % version, headers={'Authorization': 'Token token=pTs1OAhcDTJxOVjava5usL9lGpDHbIanuluU1CpoXzs'}).text
    jsoned = json.loads(response)
    if not jsoned[version_dec]['vulnerabilities']:
        print ('%s No vulnerabilities found' % bad)
        quit()
    for vulnerability in jsoned[version_dec]['vulnerabilities']:
        print ('%s %s' % (good, vulnerability['title']))
        for reference in vulnerability['references']['url']:
            print ('    ' + reference)
        print ('')


def manual(url):
    print ('%s Extracting usernames' % run)
    for number in range(1, 9999):
        response = requests.get(url + '/?d3v=x&author=' + str(number), headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'} ).text # Makes request to webpage
        match = re.search(r'/author/(.*?)"', response) # Regular expression to extract username
        if match:
            username = match.group(1).split('/')[0] # Taking what we need from the regex match
            print (username.replace('/feed', '')) # Print the username without '/feed', if present
            usernames.append(username) # Appending the username to usernames list
        else:
            if number - len(usernames) > 20: # A simple logic to be on the safe side
                if len(usernames) > 0:
                    print ('%s Looks like Zoom has found all the users. Exiting...' % info)
                    quit()
                else:
                    print ('%s Looks like there\'s some security measure in place. Exiting...' % bad)
                    quit()

if args.url:
    url = args.url # args.url contains value of -u option
    if 'http' not in url:
        url = 'http://' + url
    if url.endswith('/'):
        url = url[:-1]
    version = metagenerator(url)
    version_vul(version[0], version[1])
    manual(url)
else:
    parser.print_help()

if usernames:
    for username in usernames:
        requests.get()
