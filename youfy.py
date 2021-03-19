from youtubesearchpython import VideosSearch
import pafy
import vlc
from tqdm import tqdm
from pytube import YouTube , Playlist
import time
from urllib.request import urlopen
from bs4 import BeautifulSoup
from threading import Thread
import os, sys

count = 0
count2 = 0
idlink = []
pidlink = []
namelist = []
name = []
nextsong = []
new = []
url = []
stop = False

def main2(media,url):    
    global stop 
    print("<1> Stop  <2> Next Song  <3> Find Song <4> Check Status  <5> Download Song  <6> Save to Playlist")
    a2 = (input("Choose -->  "))
    if a2 == "1":
        if stop == False:
            stop = True
            main2(media,url)             
        if stop == True:      
            stop = False
            main2(media,url)                
    if a2 == "2":                
        if stop == False:
            stop = True
            media.stop()
            play(-1,0,1)  
        if stop == True:      
            stop = False
            media.stop()
            play(-1,0,1)  
    if a2 == "3":
        if stop == False:
            stop = True
            t1 = Thread(target=search)    
            t1.start()
            time.sleep(8)
            media.stop()
            main2(media,url)
        if stop == True:      
            stop = False
            t1 = Thread(target=search)    
            t1.start()
            time.sleep(8)
            media.stop()
            main2(media,url)           
    if a2 == "4":
        countdown(media)
        main2(media,url)
    if a2 == "5":
        print(YouTube(url).title +" is downloading")
        t1 = Thread(target=download,args=(url,))    
        t1.start()   
        main2(media,url)
    if a2 == '6':
        save = open("Playlist.txt","a+")            
        save.writelines(url+"\n")
        save.writelines(YouTube(url).title + "\n")   
        save.close()            
        main2(media,url)
    else:
        print("Typo")
        main2(media,url)

def main():
    while True:
        idlink.clear()
        pidlink.clear()
        url.clear()
        namelist.clear()
        name.clear()
        print("<1> Find  <2> Show Playlist")
        a = (input("Choose -> "))
        if a.isdigit() == True:
            if int(a) == 1:
                search()
            if int(a) == 2:
                if os.path.exists("Playlist.txt"):
                    read = open("Playlist.txt","r") 
                    savelist = [(line.strip()).split() for line in read]
                    for i in savelist:
                        a = (''.join(i))
                        if "https" in a:
                            pass
                        else:
                            print(a)
                else:
                    os.system("touch Playlist.txt")
                    print("It is empty")
                    continue   
            else:
                print("Out of Range")
                continue
        else:
            print("Number only")     
            continue   

def search():
    a1 = input("Find --> ")
    search = VideosSearch(a1.replace(" ","+"))    
    a = list((search.result().items()))
    b = (''.join(str(e) for e in a))
    c = b.split(',')
    get(c,search)

def get(c,search):
    global count
    global count2
    for i in c:
        if "id':" not in c[count]:  
            pass
        else:
            idlink.append(c[count])      
        if ("title" not in c[count]):  
            pass
        else:
            namelist.append(c[count])          
        count += 1
    count = 0
    for i in range(int(len(idlink)/2)):   
        a = idlink[count].split("id")        
        pidlink.append(a[1].replace("': ",""))
        count += 2        
    for i in pidlink:    
        url.append("https://www.youtube.com/watch?v="+i.replace("'",""))        
    count = 0
    for i in range(int(len(namelist)/2)):   
        a = namelist[count2].split("title")       
        print(str(count+1)+ "  " + a[1])     
        name.append(a[1])
        count2 += 2
        count += 1
    print("N  Next Page")
    print("B  Back to search")
    count2 = 0
    count = 0
    select(search)

def select(search):
    a = input("Select --> ")
    if a == "N":
        nextpage(search)
    if a == "B":
        main()    
    if a.isdigit() == True:
        if int(a) > 20:
            pass
        else:
            play(int(a),1,0)
    else:
        print("typo")
        pass

def nextpage(search):
    idlink.clear()
    pidlink.clear()
    url.clear()
    namelist.clear()
    name.clear()
    search.next()
    a = list((search.result().items()))
    b = (''.join(str(e) for e in a))
    c = b.split(',')
    get(c,search)

def play(a,b,c):    
    if b == 1:
        url1 = url[a-1]       
        video = pafy.new(url1)
        audio = video.getbestaudio().url
        media = vlc.MediaPlayer(audio)
        print("Now Playing --> " + YouTube(url1).title)
        media.play()   
        time.sleep(1)  
        new.clear()       
        next(url1,media)
    if c == 1: 
        url1 = nextsong[0]        
        video = pafy.new(url1)
        audio = video.getbestaudio().url
        media = vlc.MediaPlayer(audio)
        print("Now Playing --> " + YouTube(url1).title)
        media.play()           
        time.sleep(1)      
        new.clear()   
        next(url1,media)
        

def countdown(media):             
    bar = int(media.get_length()/1000)-round(int(media.get_time()/1000))
    print("Still have " + str(bar) +"sec")

def next(url,media):
    count = 0         
    page = urlopen((url))    
    soup =  BeautifulSoup(page, "html.parser" )
    b = (''.join(str(e) for e in soup))
    c = b.split(',')
    for i in c:
        if "https://i.ytimg.com" not in i:
            pass
        else:        
            new.append("https://www.youtube.com/watch?v="+i.split("/")[4])               
        count += 1    
    check(url,media,url)              

def check(name,media,url):              
    count = 0
    nextsong.clear()
    for i in new:        
        count +=  1
        if count >= 6:
            if len(i) == 43:            
                if i == name:                
                    continue
                else:                                
                    nextsong.append(i)                
                break   
            else:
                continue
    nextplay(media,url)         

def nextplay(media,url):
    global stop
    length = int(media.get_length()/1000)-round(int(media.get_time()/1000))
    t1 = Thread(target=main2,args=(media,url,))    
    t1.start()
    if stop == False:
        wait(length,media)    
    if stop == True:
        wait2(length,media)    
    
def wait(length,media):  
    global stop      
    for i in range(length):  
        length -= 1
        if stop == True:
            sys.exit()
        time.sleep(1)
        if length != 0:
            pass
        else:                        
            play(-1,0,1)

def wait2(length,media):  
    global stop      
    for i in range(length):  
        length -= 1
        if stop == False:
            sys.exit()
        time.sleep(1)
        if length != 0:
            pass
        else:                        
            play(-1,0,1)

def download(url):
    os.system("mkdir Music > /dev/null 2>&1")
    music = YouTube(url).streams.filter(audio_codec="mp4a.40.2").desc().first().download(filename="naudio")                            
    rname= YouTube(url).title.replace("/","")                                              
    os.rename("naudio.mp4","Music/"+rname+".mp3")
    print(YouTube(url).title +" is downloaded") 

main()
