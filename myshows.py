#!/usr/bin/python3

import hashlib
import sys
import time
try :
    import requests
except ImportError:
    print 'Please install requests module'
    sys.exit(1)

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
    return dict(PHPSESSID=sesid)

def id_to_title(showid):
    return shows_list[showid]

def unwatched(cook):
    # method http://api.myshows.ru/profile/episodes/unwatched/
    unwatched = 'http://api.myshows.ru/profile/episodes/unwatched/'
    r2 = requests.get(unwatched, cookies=cook)
    data = r2.json()
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
    print(data)
    print('Comming soon :')
    for i in data.values():
        print('Show: {}\t| s:{} | e:{} | Date:{}'.format(id_to_title(i['showId']), i['seasonNumber'], 
                                                         i['episodeNumber'],i['airDate']))
                                                         
if __name__ == "__main__":
    login = ''
    password = ''
    cook = get_ses_id(login,password)
    print(cook)
    r3 = requests.get('http://api.myshows.me/profile/shows/', cookies=cook)
    x = r3.json() 
    shows_list = {i['showId']:i['title'] for i in x.values()}
    print(shows_list)
    unwatched(cook)
    watch_soon(cook)                                                       
