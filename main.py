#Opens dependencies
from flask import Flask
from flask import Flask, redirect, url_for, render_template, request, flash
import os
import random
import json
import requests
import re
import webview
import sys
import threading
import keyboard


app = Flask(__name__)

global links
links = []

#Route for directory
@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('index.html')

#Route for initial web scraping and redirect to first random security camera
@app.route("/data/", methods=['GET', 'POST'])
def index():
    for i in range(1):
        os.chdir('linksbot')
        os.chdir('linksbot')
        os.system('scrapy crawl linkspider')
        with open('links.txt','r') as f:
            lines = f.readlines()
            for line in lines:
                links.append(line)
        return redirect(url_for('urllookup'))
    return 'loading data'

#Route picks a random security camera from web scraping data and displays it on the screen
@app.route("/url/", methods=['GET', 'POST'])
def urllookup():
    urlchosen = random.choice(links)
    links.remove(urlchosen)
    if request.method == 'POST':
        favorite = request.form['favorite']
        print(favorite)
    start = '//'
    end = ':'
    s = urlchosen
    urlforlookup = s[s.find(start)+len(start):s.rfind(end)]
    print(urlforlookup)
    getinfourl = 'https://ipapi.co/' + urlforlookup + '/json'
    response = requests.get(getinfourl)
    data = response.json()
    print(data)
    country=data['country_name']
    region=data['region']
    city=data['city']
    with open("viewed.txt", "a") as viewedtxt:
        viewedtxt.write(urlchosen)
    return render_template('home.html', video_feed=urlchosen, Country=country, Region=region, City=city)

#Route for adding a new favorite security camera
@app.route("/addfavorite/", methods=['GET', 'POST'])
def addfavorite():
    favorite = request.form['favorite']
    print(favorite)
    with open("favorites.txt", "a") as favoritestxt:
        favoritestxt.write(favorite + '\n')
    return render_template('home.html', video_feed=favorite)

#Route for viewing favorite security cameras
@app.route("/favorites/", methods=['GET', 'POST'])
def viewfavorite():
    favorites = []
    with open('favorites.txt','r') as favoritestxt:
        linksintxt = favoritestxt.readlines()
        for line in linksintxt:
            favorites.append(line)
    currentchoice = random.choice(favorites)
    print(currentchoice)
    return render_template('favorites.html', video_feed=currentchoice)

@app.route("/back/", methods=['GET', 'POST'])
def urlback():
    with open('viewed.txt', 'r') as websitetxtread:
        urlchosen = websitetxtread.readlines()[-2]
        print('URL', urlchosen)
    if request.method == 'POST':
        favorite = request.form['favorite']
        print(favorite)
    start = '//'
    end = ':'
    s = urlchosen
    urlforlookup = s[s.find(start)+len(start):s.rfind(end)]
    print(urlforlookup)
    getinfourl = 'https://ipapi.co/' + urlforlookup + '/json'
    response = requests.get(getinfourl)
    data = response.json()
    #print(data)
    country=data['country_name']
    region=data['region']
    city=data['city']
    with open("viewed.txt", "a") as viewedtxt:
        viewedtxt.write(urlchosen)
    return render_template('home.html', video_feed=urlchosen, Country=country, Region=region, City=city)


#Runs the server
def start_server():
    app.run(host='127.0.0.1', port='5000', debug=False)

def keyboard_input():
    while True:
        if keyboard.read_key() == "d":
            window.load_url('http://127.0.0.1:5000/url/')
        elif keyboard.read_key() == "a":
            window.load_url('http://127.0.0.1:5000/back/')
        elif keyboard.read_key() == "f":
            window.load_url('http://127.0.0.1:5000/favorites/')
        else:
            print('No Refresh')    
    
if __name__ == '__main__':
    t = threading.Thread(target=start_server)
    t.daemon = True
    t.start()
    m = threading.Thread(target=keyboard_input)
    m.daemon = True
    m.start()
    window = webview.create_window('Open Security Cameras Explorer', 'http://127.0.0.1:5000/data/', fullscreen=False)
    webview.start()
