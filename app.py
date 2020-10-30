from flask import Flask, jsonify,request
import time
import os
from selenium import webdriver

op = webdriver.ChromeOptions()
op.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
op.add_argument("--headless")
op.add_argument("--no-sandbox")
op.add_argument("--disable-dev-sh-usage")

channelIds = [
    'UCSJ4gkVC6NrvII8umztf0Ow',
    'UCzMxEa-lDX2AfgotszScOFg',
    'UCsIg9WMfxjZZvwROleiVsQg',
    # 'UChs0pSaEoNLV4mevBFGaoKA'
    'UC1opHUrw8rvnsadT-iGp7Cg', #aqua
    'UC-hM6YJuNYVAmUWxeIr9FeA', # miko
    'UC1DCedRgGHBdm81E1llLhOQ', # pekora
    'UCvzGlP9oQwU--Y0r9id_jnA', # subaru
    'UCqm3BQLlJfvkTsX_hvm0UmA', # watame
    'UCCzUftO8KOVkV4wQG1vkUvg', # marine
    'UCMwGHR0BTZuLsmjY_NT5Pwg', #ninomae
    'UCD-miitqNY3nyukJ4Fnf4_A', #tsukino
]

remaining_channelIds = channelIds
baseUrl = 'https://www.youtube.com'

class Channel():
    def __init__(self, name, profileUrl):
        self.name = name
        self.profileUrl = profileUrl

    def getName(self):
        return self.name
    def getVideos(self):
        return self.videos
    def serialize(self):
        return {
            'name': self.name,
            'profileUrl': self.profileUrl,
        }

channel_list = []

app = Flask(__name__)
@app.route('/bot', methods=["POST"])
def response():
    query = dict(request.form)['query']
    res = query + " " + time.ctime()
    return jsonify({"response" : res})

@app.route('/fetchchannel', methods=["GET"])
def getChannel():
    driver = webdriver.Chrome(executable_path = os.environ.get("CHROMEDRIVER_PATH"), chrome_options= op)
    for channelId in channelIds:
        if (len(channel_list) < 5):
            driver.get('{}/channel/{}'.format(baseUrl, channelId))
            content = driver.page_source.encode('utf-8').strip()
            # Channel details
            name = driver.find_element_by_xpath('//*[@id="text-container"]/yt-formatted-string').text
            profileUrl = driver.find_element_by_xpath('//*[@id="avatar"]/img').get_attribute('src')

            channel = Channel(name, profileUrl)
            channel_list.append(channel)
            print(channel.getName())
        else:
            break

    results = []
    for j in channel_list :
        results.append(j.serialize())
    driver.quit()
    return jsonify({"channels": results})

if __name__== '__main__':
    app.run(host="0.0.0.0",)