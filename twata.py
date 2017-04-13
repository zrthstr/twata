import os
import sys
import time
import wget
import qrcode
import tweepy
import zbarlight
import configparser
from PIL import Image



class Twata:

    def __init__(self ):
        self.IMG_IN_DIR = "img_in"
        self.IMG_OUT_DIR = "img_out"
        self.CONFIG_FILE = "config"
        self.CONFIG_SECTION = "DEFAULT"
        print("auth")
        self.api = self.auth()
        print("auth success")


    def auth(self):
        self.read_config()
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_token, self.access_token_secret)
        api = tweepy.API(auth)
        return api


    def read_config(self, CONFIG_FILE="config", CONFIG_SECTION="DEFAULT"):
        config_file = sys.path[0] + "/" + CONFIG_FILE
        config = configparser.ConfigParser()
        config.read(config_file)

        self.consumer_key = config[CONFIG_SECTION]['consumer_key']
        self.consumer_secret = config[CONFIG_SECTION]['consumer_secret']
        self.access_token = config[CONFIG_SECTION]['access_token']
        self.access_token_secret = config[CONFIG_SECTION]['access_token_secret']


    def get_files(self, folder="img_in"): 
        urls = self.get_img_urls()
        counter = 0
        os.chdir(folder)
        for url in urls:
            filename = url.rsplit('/',1)[-1]
            print("fetching: ", url, filename)
            if os.path.exists(filename):
                print("file allready present, skipping: ", url)
            else:
                wget.download(url)
                counter +=1
        os.chdir("..")
        return counter
        

    def get_img_urls(self):
        tweets = self.api.user_timeline(count=200, include_rts=False, exclude_replies=True)
        media_files = set(status.entities.get('media', [])[0]['media_url'] for status in tweets if len(status.entities.get('media', [])) > 0)
        return media_files


    def read_image(self):
        os.chdir(self.IMG_IN_DIR)   ## we should allready be here
        for filename in os.listdir('.'):
            if filename.startswith('.'):
                continue
            image = Image.open(filename)
            image.load()
            codes = zbarlight.scan_codes('qrcode', image)
            print('QR found in file:%s --> %s' % (filename, codes))


    def mk_image(self, message):
        img = qrcode.make(message)
        filename = 'img_out/'+ str(time.time()) +'.png'
        img.save(filename) # should be md5
        print("file wirtten:", filename)
        return filename


    def send_image(self, filename):
        self.api.update_with_media(filename)


lorem = """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec vitae ornare purus, quis facilisis diam. Proin pharetra ornare egestas. Phasellus venenatis neque eget sem rutrum, vel faucibus mauris varius. Curabitur mattis posuere velit. Praesent convallis ac justo id iaculis. Pellentesque iaculis pretium mauris sed congue. Vivamus tempor cursus feugiat. Donec vel nunc luctus, tincidunt nulla in, venenatis felis. Proin pharetra euismod lectus, ut malesuada arcu dignissim id.

Proin vitae nibh ut mauris blandit bibendum. Suspendisse scelerisque gravida urna, eu tincidunt nisl bibendum ac. In ut volutpat mauris. Sed in pretium diam. Suspendisse potenti. Proin placerat justo at justo varius, a dictum erat vulputate. Curabitur viverra turpis vitae nisl rhoncus, in facilisis arcu luctus. Mauris semper porta odio, faucibus faucibus sem porttitor vitae. Fusce at faucibus magna, eu fringilla nibh. Aliquam sagittis sollicitudin nibh sit amet vehicula.

Sed accumsan posuere neque at malesuada. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Cras tristique consequat quam, ut malesuada felis auctor vitae. Pellentesque ut vulputate urna, eu ornare risus. Donec velit risus, rutrum non dolor vitae, ullamcorper efficitur turpis. Nam scelerisque dictum est, id ultrices nisl. Suspendisse quis malesuada sapien. Vestibulum non semper nisi, a porta sapien. Ut finibus suscipit ex quis efficitur. Vestibulum in ligula orci. Praesent ac odio id ipsum euismod rhoncus vitae tempor libero. Integer nec diam nulla. Proin accumsan a neque non euismod."""


lorem_small = """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec vitae ornare purus, quis facilisis diam. Proin pharetra ornare egestas. Phasellus venenatis neque eget sem rutrum, vel faucibus mauris varius. Curabitur mattis posuere velit. Praesent convallis ac justo id iaculis. Pellentesque iaculis pretium mauris sed congue. Vivamus tempor cursus feugiat. Donec vel nunc luctus, tincidunt nulla in, venenatis felis. Proin pharetra euismod lectus, ut malesuada arcu dignissim id."""

