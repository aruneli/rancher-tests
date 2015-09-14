#!/usr/bin/python

import os
import sys
import getopt
import requests, json
from time import sleep

# usage help message
def usage(msg = None):
        if not msg == None:
                print msg
                print
        print "Usage: new_host [--url=<RANCHER_URL> --key=<RANCHER_ACCESS_KEY> --secret=<RANCHER_SECRET_KEY>]"
        print
        print "Adds this host to Rancher using the credentials supplied or defined as environment vars"

# get credentials form args or env
rancher_url = os.environ.get("RANCHER_URL",None)
rancher_key = os.environ.get("RANCHER_ACCESS_KEY",None)
rancher_secret = os.environ.get("RANCHER_SECRET_KEY",None)

opts, args = getopt.getopt(sys.argv[1:],"hu:k:s:",["help","url=","key=","secret="])
for o,a in opts:
        if o in ("-h","--help"):
                usage()
                sys.exit(1)
        elif o in ("-u","--url"):
                rancher_url = a
        elif o in ("-k","--key"):
                rancher_key = a
        elif o in ("-s","--secret"):
                rancher_secret = a

if rancher_url == None:
        usage("Rancher URL not specified")
        sys.exit(1)
if rancher_key == None:
        usage("Rancher key not specified")
        sys.exit(1)
if rancher_secret == None:
        usage("Rancher secret not specified")
        sys.exit(1)

# split url to protocol and host
rancher_protocol,rancher_host = rancher_url.split("://")

# get environment we're in
url = "%s://%s:%s@%s/v1/projects" % (rancher_protocol,rancher_key,rancher_secret,rancher_host)
response = requests.get(url)
data = json.loads(response.text)
rancher_environment = data['data'][0]['name']
print "rancher_environment is %s" % rancher_environment

# now ask for a new registration key and wait until it becomes active
url = "%s://%s:%s@%s/v1/registrationtokens" % (rancher_protocol,rancher_key,rancher_secret,rancher_host)
response = requests.post(url,json={})
key_active = False
while not key_active:
        url = "%s://%s:%s@%s/v1/registrationtokens/%s" % (rancher_protocol,rancher_key,rancher_secret,rancher_host,response.json()['id'])
        print url
        if response.json()['state'] == 'active':
                key_active = True
                command = response.json()['command']
        else:
                sleep(0.1)
                response = requests.get(url)

print command
os.system(command)