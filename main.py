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
import time

app = Flask(__name__)

global links
links = []

@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('index.html')

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
    try:
        country=data['country_name']
        region=data['region']
        city=data['city']
    except:
        country = ''
        region = ''
        city = ''
    with open("viewed.txt", "a") as viewedtxt:
        viewedtxt.write(urlchosen)
    return render_template('home.html', video_feed=urlchosen, Country=country, Region=region, City=city)

@app.route("/addfavorite/", methods=['GET', 'POST'])
def addfavorite():
    favorite = request.form['favorite']
    print(favorite)
    with open("favorites.txt", "a") as favoritestxt:
        favoritestxt.write(favorite + '\n')
    return render_template('home.html', video_feed=favorite)

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
    try:
        country=data['country_name']
        region=data['region']
        city=data['city']
    except:
        country = ''
        region = ''
        city = ''
    with open("viewed.txt", "a") as viewedtxt:
        viewedtxt.write(urlchosen)
    return render_template('home.html', video_feed=urlchosen, Country=country, Region=region, City=city)


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

def toggle_fullscreen(window):
    window.hide()
    time.sleep(8)
    window.show()
    window.toggle_fullscreen()

if __name__ == '__main__':
    t = threading.Thread(target=start_server)
    t.daemon = True
    t.start()
    m = threading.Thread(target=keyboard_input)
    m.daemon = True
    m.start()
    window = webview.create_window('Open Security Cameras Explorer', 'http://127.0.0.1:5000/data/', text_select=False, minimized=True, resizable=False)
    webview.start(toggle_fullscreen, window)
