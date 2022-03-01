#import needed libraries
import pandas as pd
import json
import numpy as np
import requests
from datetime import datetime
#from wordpress_xmlrpc import Client, WordPressPost
#from wordpress_xmlrpc.methods.posts import NewPost
from wordpress_xmlrpc.methods import media, posts
from wordpress_xmlrpc.compat import xmlrpc_client
import time
import copy


def add_follow_twitter(twitterHandle="openneurosci"):

    addTwitter = '<!-- wp:html -->\n'+ \
              '<div align="center">\n'+ \
              '<a href="https://twitter.com/'+\
              '{twitterHandle}?ref_src=twsrc%5Etfw" class="twitter-follow-button" data-show-count="true">'.format(twitterHandle=twitterHandle)+ \
              'Follow {twitterHandle}</a><script async=""'.format(twitterHandle=twitterHandle)+\
              'src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>\n'+ \
              '</div>\n'+ \
              '<!-- /wp:html -->\n'
    
    
    return addTwitter

def author(authorText="Charles Darwin"):
    authorString = '<!-- wp:group -->\n'+\
                        '<div class="wp-block-group"><!-- wp:heading {"level":3} -->\n'+\
                        '<h3 id="authors">Authors</h3>\n'+\
                        '<!-- /wp:heading -->\n\n'+\
                        '<!-- wp:paragraph {"fontSize":"medium"} -->\n'+\
                        '<p class="has-medium-font-size">{authorText}</p>\n'.format(authorText=authorText)+\
                        '<!-- /wp:paragraph --></div>\n'+\
                        '<!-- /wp:group -->\n'
    return authorString

def download_url_image(imageURL,imageName = "image"):
    imageFormats = ("image/png", "image/jpeg", "image/jpg","image/gif","image/svg")
    r = requests.head(imageURL)
    print( "image type: "+ r.headers["content-type"])
    #print(r.headers["content-type"])
    if r.headers["content-type"] in imageFormats:
        imgData = requests.get(imageURL).content
        if r.headers["content-type"]=="image/png":
            extension = ".png"
            iFormat = "image/png"
        elif r.headers["content-type"]=="image/jpeg" or r.headers["content-type"]=="image/jpg":
            extension = ".jpg"
            iFormat = "image/jpg"
        elif r.headers["content-type"]=="image/gif":
            extension = ".gif"
            iFormat = "image/gif"
        elif r.headers["content-type"]=="image/svg":
            extension = ".svg"
            iFormat = "image/svg"
        with open(imageName+extension, 'wb') as handler:
            handler.write(imgData)
    else:
        imageName = "logo_blue"
        extension = ".png"
        iFormat = "image/png"
    
    return imageName+extension,iFormat

def embed_video(videoURL):
    embedString = '<!-- wp:group -->\n'+\
                  '<div class="wp-block-group"><!-- wp:heading {"level":3} -->\n'+\
                  '<h3 id="video">video</h3>\n'+\
                  '<!-- /wp:heading -->\n'+\
                  '<!-- wp:embed /--></div>\n'+\
                  '<!-- /wp:group -->\n'
    return embedString

def project_links(url,urlText):
    linkString = '<!-- wp:group -->\n'+\
                     '<div class="wp-block-group"><!-- wp:heading {"level":3} -->\n'+\
                     '<h3 id="links">links</h3>\n'+\
                     '<!-- /wp:heading -->\n\n'+\
                     '<!-- wp:html -->\n'+\
                     '<a href="{url}"> {urltext}</a>\n'.format(url=url,urltext=urlText)+\
                     '<!-- /wp:html --></div>\n'+\
                     '<!-- /wp:group -->\n'
    return linkString

def post_creator(creatorText = "charles Darwin"):
    creatorString = '<!-- wp:group -->\n'+\
                    '<div class="wp-block-group"><!-- wp:heading {"level":3} -->\n'+\
                    '<h3 id="generated-by">This post was created by:</h3>\n'+\
                    '<!-- /wp:heading -->\n'+\
                    '<!-- wp:paragraph {"fontSize":"medium"} -->\n'+\
                    '<p class="has-medium-font-size">{creatorText}</p>\n'.format(creatorText=creatorText)+\
                    '<!-- /wp:paragraph --></div>\n'+\
                    '<!-- /wp:group -->\n'
    return creatorString
        
def spacer():
    spacerString =  '<!-- wp:spacer {"height":45} -->\n'+\
                        '<div style="height:45px" aria-hidden="true" class="wp-block-spacer"></div>\n'+\
                        '<!-- /wp:spacer -->\n\n'
    return spacerString
    
def summary(summaryText="lorem ipsum"):
    summaryString = '<!-- wp:group -->\n'+\
                         '<div class="wp-block-group"><!-- wp:heading {"level":3} -->\n'+\
                         '<h3 id="summary">Summary</h3>\n'+\
                         '<!-- /wp:heading -->\n\n'+\
                         '<!-- wp:paragraph {"fontSize":"medium"} -->\n'+\
                         '<p class="has-medium-font-size">{summaryText}</p>\n'.format(summaryText=summaryText)+\
                         '<!-- /wp:paragraph --></div>\n'+\
                         '<!-- /wp:group -->\n'
    return summaryString



def twitter_embed(twitterHandleList):
    links = []
    embedString = '<!-- wp:html -->\n'+\
                  '<div align="right">\n'
    for item in twitterHandleList:
        embedString+\
        '<a href="https://twitter.com/{twitterHandle1}}?ref_src=twsrc%5Etfw" class="twitter-follow-button" data-show-count="false">Follow {twitterHandle2}</a><script async="" src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>\n'.format(twitterHandle1=item, twitterHandle2=item)
    
    embedString+\
    '</div>\n'+\
    '<!-- /wp:html -->\n'
    
    return embedString

def thumbnail():
    pass

def upload_image_wp(imageName,iFormat,client):

    # prepare metadata
    data = {
        'name': imageName,
        'type': iFormat,  # mimetype
    }

    # read the binary file and let the XMLRPC library encode it into base64
    with open(imageName, 'rb') as img:
        data['bits'] = xmlrpc_client.Binary(img.read())

    response = client.call(media.UploadFile(data))
    
    return response


def replace_text(stringIn,oldText,newText):
    start = stringIn.find(oldText)
    end = start+len(oldText)
    output = stringIn[:start]+newText+stringIn[end:]
    return output
