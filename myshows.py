#!/usr/bin/python3
# -*- coding: utf-8 -*-

from datetime import date
from datetime import time
from datetime import datetime
from datetime import timedelta
from urllib.request import quote
import time
import hashlib
import sys
import time
import argparse
try :
    import requests
except ImportError:
    print('Please install requests module')
    sys.exit(1)

parser = argparse.ArgumentParser(description='myshows watcher')
parser.add_argument("--login", "-l", type=str, help="Login")
parser.add_argument("--password", "-p", type=str, help="Password")
parser.add_argument("--debug", action='store_true', help="Debug")
args = parser.parse_args()


def computeMD5hash(password):
    m = hashlib.md5()
    m.update(password.encode('utf-8'))
    return m.hexdigest()
 

def get_ses_id(login,password):
    # method 'http://api.myshows.ru/profile/login?login=dezz&password=' + MD5 of the password
    url = 'http://api.myshows.ru/profile/login?login=' + login + '&password=' + computeMD5hash(password)
    r = requests.get(url)
    if r.status_code in (403, 404):
        print('Required proper authrization !')
        sys.exit(1)   
    sesid = r.cookies['PHPSESSID']
    if args.debug:
        print(r.cookies)
    return dict(PHPSESSID=sesid)


def id_to_title(showid):
    return shows_list[showid]


def unwatched(cook):
    # method http://api.myshows.ru/profile/episodes/unwatched/
    unwatched = 'http://api.myshows.ru/profile/episodes/unwatched/'
    unwatched_list = ['Unwatched :',]
    r2 = requests.get(unwatched, cookies=cook)
    data = r2.json()
    if args.debug:
        print(data)
    if not len(data) == 0:
        for i in sorted(data.values(), key=lambda x:datetime.strptime(x['airDate'], '%d.%m.%Y').date()): # a bit weird code
            line = '{} | s:{} | e:{} | {}'.format(id_to_title(i['showId']), i['seasonNumber'], 
                                                              i['episodeNumber'],i['airDate'])
            unwatched_list.append(line)
        return unwatched_list
    else: 
        return []


def watch_soon(cook):
    # method http://api.myshows.ru/profile/episodes/unwatched/
    method = 'http://api.myshows.me/profile/episodes/next/'
    watch_soon_list = ['Comming soon:',]
    r = requests.get(method, cookies=cook)
    data = r.json()
    if args.debug:
        print(data)
    if not len(data) == 0:
        for i in sorted(data.values(), key=lambda x:datetime.strptime(x['airDate'], '%d.%m.%Y').date()): # a bit weird code
            line = '{} | s:{} | e:{} | {}'.format(id_to_title(i['showId']), i['seasonNumber'], 
                                                              i['episodeNumber'],i['airDate'])
            watch_soon_list.append(line)
        return watch_soon_list
    else: 
        return []


def message_send(userid, message):
    ''' This func sends message to an appropriate user via vk.com '''
    user = str(userid)
    url = 'https://api.vk.com/method/messages.send?user_id={}&message={}&access_token={}'.format(user, quote(message), token)
    if args.debug:
        print(url)
    response = requests.get(url).json()


if __name__ == "__main__":

    token = 'decb1101f64a66241544771c10934efa666e9e0e8c' # vk access tocken
    users = [111111111,] # list of the IDs 

    if not len(sys.argv) == 1:
        cook = get_ses_id(args.login,args.password)
        r3 = requests.get('http://api.myshows.me/profile/shows/', cookies=cook).json() 
        shows_list = {i['showId']:i['title'] for i in r3.values()}
        unwatched_list = unwatched(cook)
        watch_soon_list = watch_soon(cook)
        if len(unwatched_list) > 1:
            to_send = '\n'.join(i for i in unwatched_list)
            for i in users:
                message_send(i,to_send)
                time.sleep(5)
        else:
            if len(watch_soon_list) > 1:
                to_send = '\n'.join(i for i in watch_soon_list)
                for i in users:
                    message_send(i,to_send)
                    time.sleep(5)
            watch_soon(cook)
    else:
        print('Use --help for more detail')


'''
What next :

# http://api.myshows.ru/profile/episodes/check/291461
# http://api.myshows.ru/profile/episodes/uncheck/291461

'''
 
