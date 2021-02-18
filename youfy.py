from youtubesearchpython import VideosSearch
import pafy
import vlc
from tqdm import tqdm
from pytube import YouTube , Playlist
import time
from urllib.request import urlopen
from bs4 import BeautifulSoup
from threading import Thread
import os

count = 1
songcount = 0
titlecount = 0
musiclist = []
musiclink = []
nmusiclink = []
savemusic = []
savename = []
new = []
nextsong = []
url = []
answer = None

def timing():
    time_limit = 5
    while True:
        time_taken = time.time() - start_time
        if answer is not None:            
            os._exit(1)
        if time_taken > time_limit:                        
            break
        time.sleep(0.001)
        
def main():
    global start_time, answer
    start_time = time.time()
    musiclist.clear()
    musiclink.clear()
    nmusiclink.clear()        
    a1 = input("Find -> ")
    search = VideosSearch(a1.replace(" ","+"))    
    a = list((search.result().items()))
    b = (''.join(str(e) for e in a))
    c = b.split(',')
    links(c,search)
    mlist(c,search)
    time.sleep(0.001)

def links(c,search):
    global count
    global songcount
    global titlecount
    for i in c:
        if ("id':" not in c[songcount]):  
            pass
        else:
            musiclink.append(c[songcount])        
        songcount += 1

    for i in range(int(len(musiclink)/2)):   
        a = musiclink[titlecount].split("id")        
        nmusiclink.append(a[1].replace("': ",""))
        titlecount += 2
        count += 1
    for i in nmusiclink:    
        url.append("https://www.youtube.com/watch?v="+i.replace("'",""))    
    count = 1
    songcount = 0
    titlecount = 0    

def mlist(c,search):
    global count
    global songcount
    global titlecount
    for i in c:
        if ("title" not in c[songcount]):  
            pass
        else:
            musiclist.append(c[songcount])        
        songcount += 1

    for i in range(int(len(musiclist)/2)):   
        a = musiclist[titlecount].split("title")
        print(str(count)+ "  " + a[1].replace("': ",""))        
        titlecount += 2
        count += 1
    print("N  Next Page" )    
    count = 1
    songcount = 0
    titlecount = 0
    select(search)

def select(search):
    select = (input("Select -> "))
    if select == "N":  
        musiclist.clear()
        musiclink.clear()
        nmusiclink.clear()        
        url.clear()
        search.next()
        a = list((search.result().items()))
        b = (''.join(str(e) for e in a))
        c = b.split(',')
        links(c,search)
        mlist(c,search)          
    elif int(select) > 20:
        pass
    else:
        play(select)

def play(select):    
    video = pafy.new(url[int(select)-1])
    best = video.getbest()
    playurl = best.url
    Instance = vlc.Instance("--no-video")
    player = Instance.media_player_new()
    Media = Instance.media_new(playurl)
    Media.get_mrl()
    player.set_media(Media)    
    player.play()          
    ab = YouTube(url[int(select)-1]).title        
    print("Now playing " + ab)           
    next(url[int(select)-1],int(player.get_length()/1000)-round(int(player.get_time()/1000)))
    
def next(url,status):
    count = 0        
    new.clear()
    nextsong.clear()
    page = urlopen((url))    
    soup =  BeautifulSoup(page, "html.parser" )
    b = (''.join(str(e) for e in soup))
    c = b.split(',')
    for i in c:
        if "https://i.ytimg.com" not in i:
            pass
        else:        
            new.append(i)
        count += 1
    count = 0        
    nextsong.append("https://www.youtube.com/watch?v="+new[14].split("/")[4])       
    playnext(nextsong,status)

def playnext(song,status):    
    video = pafy.new(song[0])
    best = video.getbest()
    playurl = best.url
    Instance = vlc.Instance("--no-video")
    player = Instance.media_player_new()
    Media = Instance.media_new(playurl)
    Media.get_mrl()
    player.set_media(Media)   
    print("Next Song is "+YouTube(song[0]).title )
    t1 = Thread(target=main)
    t2 = Thread(target=timing)
    t1.start()
    t2.start()        
    while status-14> 0:                   
        time.sleep(1)     
        status -= 1        
    player.play()          
    ab = YouTube(song[0]).title        
    print("Now playing " + ab)       
    next(song[0],YouTube(song[0]).length)

def download(url):
    os.system("mkdir Music > /dev/null 2>&1")
    music = YouTube(url).streams.filter(audio_codec="mp4a.40.2").desc().first().download(filename="naudio")                            
    rname= YouTube(url).title.replace("/","")                                              
    os.rename("naudio.mp4","Music/"+rname+".mp3")          

while True:
    main()
