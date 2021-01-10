import json, requests
from myigbot import MyIGBot
import os, sys
from PIL import Image
import time
from random import randint

#Instagram Username and Password

username = 'USERNAME'
password = 'PASSWORD'

#Reddit Username and Password

ruser = 'USERNAME'
rpass = 'PASSWORD'


def get_image():
    req = requests.get('http://www.reddit.com/r/memes/top.json?t=day&limit=5', #replace the subreddit here
    headers={'user-agent':'Mozilla/5.0'},
    auth=(ruser,rpass),
    )
    url = req.json()['data']['children'][0]['data']['url_overridden_by_dest']
    title = req.json()['data']['children'][0]['data']['title']
    print(url, title)
    img_data = requests.get(url).content
    with open('post.jpg', 'wb') as handler:
        handler.write(img_data)
    text = title + '\r\n' + 'ADD HASHTAGS HERE'
    bot = MyIGBot(username, password)
    story = bot.upload_story('./post.jpg')
    print(story)
    basewidth = 1080
    img = Image.open('post.jpg')
    wpercent = (basewidth / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))
    img = img.resize((basewidth, hsize), Image.ANTIALIAS)
    img.save('resized.jpg')
    response = bot.upload_post("./resized.jpg", caption=text)
    print(response)  # if the response code is 200 that means ok


def like_post():
    bot = MyIGBot(username, password)
    response = bot.hashtag_posts('memes', limit=27) #replace the hashtag to look up the post by
    for post in response:
        bot.like(post)
        value = randint(0, 10)
        if value > 8:
            bot.comment(post, comment_text='😂😂😂') #replace the comment
        time.sleep(47)

while True:
    get_image()
    print("Image and story posted")
    like_post()
    print("like/comment alg done")
    time.sleep(21600)

