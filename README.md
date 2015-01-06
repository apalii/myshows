## myshows

python3+requests

This script shows all unwached episodes sorted by date if they are exist. Othewise, it will show upcoming 

#### Usage :

```bash
python3 myshows.py -l mylogin -p mypassword
```

#### Requirements :
1) It is necessary to have accounts in the following social networks :

`myshows.me` - for shows information <br>
`vk.com`  or `twitter.com` - for sms purposes

2) python3 and requests module

```bash
sudo apt-get install python3-pip
sudo pip3 install requests
```

#### Typical output :
```
$ python3 myshows.py -l mylogin -p mupasswd
New episodes are:
Физрук Физрук: серия 31 25.11.2014
Физрук Физрук: серия 30 24.11.2014
The Walking Dead Crossed 23.11.2014

Comming soon:
The Walking Dead | s:5 | e:9 | 08.02.2015
Vikings | s:3 | e:1 | 19.02.2015
Game of Thrones | s:5 | e:1 | 31.03.2015
The Strain | s:2 | e:1 | 30.06.2015

```

But the main purpose is to get a SMS on mobile phone about new episodes, so script also sends a message to the needed accounts in vk.com. 
Twitter functionality is implemented as well but not commited.

