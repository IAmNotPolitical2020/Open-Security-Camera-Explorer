from flask import Flask
from flask import Flask, redirect, url_for, render_template, request, flash
import os
import random

app = Flask(__name__)

global links
links = []

@app.route("/", methods=['GET', 'POST'])
def index():
    os.chdir('linksbot')
    os.chdir('linksbot')
    os.system('scrapy crawl linkspider')

    with open('links.txt','r') as f:
        lines = f.readlines()
        for line in lines:
            links.append(line)

    return redirect(url_for('urllookup'))

@app.route("/url/", methods=['GET', 'POST'])
def urllookup():
    urlchosen = random.choice(links)
    links.remove(urlchosen)
    return render_template('home.html', video_feed=urlchosen)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port='5000', debug=True)
