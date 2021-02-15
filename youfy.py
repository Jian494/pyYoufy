from youtubesearchpython import VideosSearch
import string
import pafy
import vlc
from tqdm import tqdm
from pytube import YouTube , Playlist
import time

count = 1
songcount = 0
titlecount = 0
musiclist = []
musiclink = []
nmusiclink = []
url = []
loop = True

def links(c):
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
        #print(str(count)+ "  " + a[1].replace("': ",""))
        nmusiclink.append(a[1].replace("': ",""))
        titlecount += 2
        count += 1
    for i in nmusiclink:    
        url.append("https://www.youtube.com/watch?v="+i.replace("'",""))    
    count = 1
    songcount = 0
    titlecount = 0

def mlist(c):
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
    count = 1
    songcount = 0
    titlecount = 0

def play(select):
    global loop
    video = pafy.new(url[int(select)-1])
    best = video.getbest()
    playurl = best.url
    Instance = vlc.Instance("--no-video")
    player = Instance.media_player_new()
    Media = Instance.media_new(playurl)
    Media.get_mrl()
    player.set_media(Media)
    if loop == True:
        player.play()  
        size = YouTube(url[int(select)-1]).length
        ab = YouTube(url[int(select)-1]).title
        bc = tqdm(range(int(size)-3),desc="Playing "+ ab)
        for i in range(int(size)-3):
            bc.update(1)
            time.sleep(1)
    else:
        player.stop()


def main():
    a1 = input("Find -> ")
    search = VideosSearch(a1.replace(" ","+"))
    a = list((search.result().items()))
    b = (''.join(str(e) for e in a))
    c = b.split(',')
    links(c)
    mlist(c)
    select = int(input("Select -> "))
    if select > 20:        
        pass
    else:
        play(select)
    
while True:
    main()
