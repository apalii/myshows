#!/usr/bin/python3

import hashlib
import sys
import time
import datetime
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

'''class Login(object):
    """docstring for Login"""
    def __init__(self, login, passwd):
        self.login = login
        self.passwd = passwd
        self.myhash = hashlib.md5()
        self.myhash.update(self.passwd.encode('utf-8'))
        self.url = 'http://api.myshows.ru/profile/login?login=' + self.login + '&password=' + self.myhash.hexdigest()
        
    def get_ses_id(self):
        return self.url

        r = requests.get(self.url)
        if r.status_code in (403, 404):
            print('Required proper authrization !')
            sys.exit(1)   
        sesid = r.cookies['PHPSESSID']
        return dict(PHPSESSID=sesid)'''

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
    r2 = requests.get(unwatched, cookies=cook)
    data = r2.json()
    if args.debug:
        print(data)
    if not len(data) == 0:
        print('New episodes are:')
        for i in data.values():
            print(id_to_title(i['showId']), i['title'], i['airDate'])
    else : print('No new episodes')

def watch_soon(cook):
    # method http://api.myshows.ru/profile/episodes/unwatched/
    method = 'http://api.myshows.me/profile/episodes/next/'
    r = requests.get(method, cookies=cook)
    data = r.json()
    if args.debug:
        print(data)
    print('Comming soon :')
    for i in sorted(data.values(), key=lambda x:datetime.datetime.strptime(x['airDate'], '%d.%m.%Y').date()): # a bit weird code
        print('Show: {:<18} | s:{} | e:{:<2} | Date:{}'.format(id_to_title(i['showId']), i['seasonNumber'], 
                                                         i['episodeNumber'],i['airDate']))

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print('Use --help for more detail')
    else:
        cook = get_ses_id(args.login,args.password)
        r3 = requests.get('http://api.myshows.me/profile/shows/', cookies=cook)
        x = r3.json() 
        shows_list = {i['showId']:i['title'] for i in x.values()}
        unwatched(cook)
        watch_soon(cook)

'''
    r3 = requests.get('http://api.myshows.me/profile/shows/', cookies=cook)
    print(r3.text)
    print('  ') 
    # y = {i['showId']:i['title'] for i in x.values()}

    #r4 = requests.get('http://api.myshows.me/profile/episodes/next/', cookies=cook)
    #print(r4.text)

# http://api.myshows.ru/profile/episodes/check/291461
# http://api.myshows.ru/profile/episodes/uncheck/291461


dd = {'2423018': {'episodeNumber': 7, 'airDate': '23.11.2014', 'title': 'Crossed', 'showId': 5317, 'episodeId': 2423018, 'seasonNumber': 5}, 
'2423019': {'episodeNumber': 8, 'airDate': '30.11.2014', 'title': 'Coda', 'showId': 5317, 'episodeId': 2423019, 'seasonNumber': 5}, 
'2436084': {'episodeNumber': 10, 'airDate': '27.11.2014', 'title': 'Физрук: серия 33', 'showId': 36931, 'episodeId': 2436084, 'seasonNumber': 2}, 
'2230182': {'episodeNumber': 1, 'airDate': '31.03.2015', 'title': 'Season 5, Episode 1', 'showId': 11945, 'episodeId': 2230182, 'seasonNumber': 5}}


print('Comming soon :')
for i in nnext.values():
    print('Show: {}\t| s:{} | e:{} | Date:{}'.format(i['showId'], i['seasonNumber'], i['episodeNumber'],i['airDate']))'''



 
