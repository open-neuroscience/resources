#import needed libraries
import pandas as pd
import json
import numpy as np
import requests
from datetime import datetime
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import NewPost
from wordpress_xmlrpc.methods import media, posts, taxonomies
from wordpress_xmlrpc.compat import xmlrpc_client
from wordpress_xmlrpc import WordPressTerm

import time
import copy
import py2wp

#from wordpress_xmlrpc import Client, WordPressPost
#from wordpress_xmlrpc.methods.posts import GetPosts, NewPost
#from wordpress_xmlrpc.methods.users import GetUserInfo



# create connection to website, download the project post template and make a copy

# website_name.txt is a file that contains username and password to access the website. This is put as gitignore, so that 
# this sensitive information is not shared openly accross the web
with open("website_credentials.txt") as fid:
    username = fid.readline()
    password = fid.readline()
    

websiteName = "https://open-neuroscience-60fc93.ingress-baronn.easywp.com"
url = websiteName+"/xmlrpc.php"


wp = Client(url, username, password)


#get template post for projects:
allProjects = wp.call(posts.GetPosts({"post_type": "project"}))
for item in allProjects:
    if item.title=="project template2":
        template=item
time.sleep(30)
print ("done")



#google sheet information
with open("sheet_id.txt") as fid:
    sheetId = fid.readline()
    

#pull data from the sheet into a pandas dataframe
allPosts = pd.read_csv('https://docs.google.com/spreadsheets/d/' + 
                   sheetId +
                   '/export?format=csv',
                   # Set first column as rownames in data frame
                   index_col=0,
                  )



import py2wp



#run a loop to go through all post entries and create posts as needed
for index in allPosts.index:
    if index ==3 and allPosts[allPosts.index==index]["posted"][index]get_ipython().getoutput("=True:")
    #if allPosts[allPosts.index==index]["posted"][index]get_ipython().getoutput("=True:")
        print("start post ... ")
        entry = allPosts[allPosts.index==index]
        #print(index)
        
        createdDate = entry["Marca temporal"][index]            
        title = entry["Project Title"][index]
        projectVideoURL = entry["Link to video for your project"][index]
        projectImageURL = entry["Link to raw image of your project"][index]
        summary = entry["Description of the project"][index]
        projectAuthor = entry["Project Author"][index]
        projectURL = entry["Link to Project Website or GitHub repository"][index]
        postCreator = entry["Post Author"][index]
        entryTags = list()
        wpTags = wp.call(taxonomies.GetTerms('post_tag'))
        for i in range(4):
            tagTemp = entry["Project categories (please select at most one per row) [Category {number}]".format(number=i+1)]
            #print(type(tagTemp.values[0]))
            if type(tagTemp.values[0]) is not float:
                for wpEntry in wpTags:
                    if wpEntry.name == tagTemp.values[0]:
                        entryTags.append(wpEntry)
                #postTags.append("<WordPressTerm: b'term'>".format(term=tagTemp.values[0]))
                #entryTags.append(tagTemp.values[0])
        
        #postTags = list()
        #for item in entryTags:
            #if item=="Software":
                #tag = WordPressTerm()
                #tag.taxonomy = 'post_tag'
                #tag.name = item
                #postTags.append(tag)
                #del(tag)
        tag = WordPressTerm()
        tag.taxonomy = 'post_tag'
        tag.name = item
        postTags = tag
        #'terms': [<WordPressTerm: b'neuroscience'>, <WordPressTerm: b'open source'>],
        #newPost.date = datetime.strptime(creationDate, 'get_ipython().run_line_magic("Y-%m-%d", " %H:%M:%S')")
        
        #create content
        postString = sumText = py2wp.summary(summaryText=summary)+\
            py2wp.spacer()+\
            py2wp.author(authorText=projectAuthor)+\
            py2wp.spacer()+\
            py2wp.project_links(projectURL,projectURL)+\
            py2wp.spacer()


        #acheck all uploaded media
        allMedia = wp.call(media.GetMediaLibrary({"parent_id":""}))
        
        #download media
        imageName = title.replace(" ","_")
        imageName,iFormat = py2wp.download_url_image(projectImageURL,imageName = imageName.lower())
        print("imagename "+imageName)
        imageFlag = 0
        for item in allMedia:
            #print(item.title)
            if item.title == imageName:
                imageFlag = 1
                image = item
                print("image already uploaded")

        if imageFlag == 1:
            imageID = image.id
            imageTitle = image.title
            imageLink = image.link
        else:
            response = py2wp.upload_image_wp(imageName,iFormat,wp)
            imageID = response["id"]
            imageTitle = response["title"]
            imageLink = response["link"]
        #replace video URL
        if type(projectVideoURL) is not float:
            postString = postString+ py2wp.embed_video(projectVideoURL)+py2wp.spacer()

        postString = postString+py2wp.post_creator(creatorText = postCreator)+py2wp.spacer()
        newPost = copy.deepcopy(template)
        newPost.title = title
        newPost.content = postString
        newPost.thumbnail = imageID
        newPost.date = datetime.strptime(createdDate, 'get_ipython().run_line_magic("Y-%m-%d", " %H:%M:%S')")
        newPost.author = "python-bot"
        newPost.slug = title
        newPost.terms = entryTags
        newPost.id = wp.call(posts.NewPost(newPost))

        #del(newPost)
        print("ready to wait")
        time.sleep(60)    
        print("done")


vars(newPost)


#len(tags = wp.call(taxonomies.GetTerms('post_tag')))
vars(tags[0])



#google sheet information
with open("sheet_id.txt") as fid:
    sheetId = fid.readline()
    

#pull data from the sheet into a pandas dataframe
allPosts = pd.read_csv('https://docs.google.com/spreadsheets/d/' + 
                   sheetId +
                   '/export?format=csv',
                   # Set first column as rownames in data frame
                   index_col=0,
                  )


#run a loop to go through all post entries and create posts as needed
for index in allPosts.index:
    if index ==1:
        
        newPost = copy.deepcopy(template)
        
        entry = allPosts[allPosts.index==index]
        print(index)
        if entry["posted"][index]get_ipython().getoutput("=True:")
            


                
                
            entryCreateData = entry["Marca temporal"][index]            
            title = entry["Project Title"][index]
            #title to be recognized in wordpress
            newPost.title = title
            #URL for wordpress
            newPost.slug = title
            # creation date
            creationDate = entry["Marca temporal"][index]
            newPost.date = datetime.strptime(creationDate, 'get_ipython().run_line_magic("Y-%m-%d", " %H:%M:%S')")

            
            #projectImageURL = entry["Link to raw image of your project"][index]
            
            #oldImageURL = 'https://open-neuroscience-60fc93.ingress-baronn.easywp.com/wp-content/uploads/2022/02/openneuroscience_blue_1600by400_border-1024x232.png'
            
            #imageName,iFormat = py2wp.download_url_image(projectImageURL,imageName = title.lower())
            #print("imagename "+imageName)
            #if imageName get_ipython().getoutput("= "logo_blue.png":")
            #    response = py2wp.upload_image_wp(imageName,iFormat,wp)
            #    time.sleep(2)
            #else:
                
            #    response = {"id":419,"link":oldImageURL}
            #print("image uploaded link: " +str(response["link"]))
            
            time.sleep(2)
            
            #attachmentId = response['id']
            #newPost.thumbnail = attachmentId
            
            postContent = replace_text(stringIn = postContent,
                                       oldText = '<img src='+oldImageURL,
                                       newText = '<img src='+response["link"])
            
            postContent = replace_text(stringIn = postContent,
                                       oldText = 'wp-image-419',
                                       newText = 'wp-image-'+str(response["id"]))
            
            
            #replace summary
            summary = entry["Description of the project"][index]
            print(summary)
            postContent = replace_text(stringIn = postContent,
                                       oldText = '<p class="has-medium-font-size">Project Summary</p>',
                                       newText = '<p class="has-medium-font-size">'+summary+'</p>')
            
            #replace project author
            projectAuthor = entry["Project Author"][index]
            postContent = replace_text(stringIn = postContent,
                                       oldText = '<p class="has-medium-font-size">Project Authors</p>', 
                                       newText = '<p class="has-medium-font-size">'+projectAuthor+'</p>')
            
            
            
            
            projectAuthorTwitter = entry["Project Author Twitter handle"][index]
            if type(projectAuthorTwitter) is not float:
                pass
            
            
            
            
            # replace project URL
            projectURL = entry["Link to Project Website or GitHub repository"][index]
            postContent = replace_text(stringIn = postContent,
                                       oldText = '<a href="hyperlink">', 
                                       newText = '<a href="'+projectURL+'">')
            
            
            postContent = replace_text(stringIn = postContent,
                                       oldText = " hyperlink1</a>", 
                                       newText = projectURL+"</a>")
            
            
            
            #replace video URL
            projectVideoURL = entry["Link to video for your project"][index]
            if type(projectVideoURL) is not float:
                postContent = replace_text(stringIn = postContent,
                                           oldText = 'https://www.youtube.com/watch?v=82Vhe9iPVQc',
                                           newText = projectVideoURL)
                
                postContent = replace_text(stringIn = postContent,
                                           oldText = 'https://www.youtube.com/watch?v=82Vhe9iPVQc', 
                                           newText = projectVideoURL)
            else:
                pass
                 #postContent = replace_text(stringIn = postContent,
                 #                          oldText = '<get_ipython().getoutput("-- wp:group --> \")
                 #                           <div class="wp-block-group"><get_ipython().getoutput("-- wp:heading {"level":3} -->\")
                 #                           <h3 id="video">video</h3>\
                 #                           <get_ipython().getoutput("-- /wp:heading -->\")
                 #                           <get_ipython().getoutput("-- wp:embed /--></div>\")
                 #                           <get_ipython().getoutput("-- /wp:group -->\")
                 #                           <get_ipython().getoutput("-- wp:spacer {"height":45} -->\")
                 #                           <div style="height:45px" aria-hidden="true" class="wp-block-spacer"></div>\
                 #                           <get_ipython().getoutput("-- /wp:spacer -->',")
                 #                          newText = '')
            
            
            
            entryAuthor = entry["Post Author"][index]
            postContent = replace_text(stringIn = postContent,
                                       oldText = '<p class="has-medium-font-size">post submitter</p>', 
                                       newText = '<p>'+entryAuthor+'</p>')
            
            #tags
            newPost.tags = entry["tags"][index]
            
            category1 = entry["Project categories (please select at most one per row) [Category 1]"][index]
            category2 = entry["Project categories (please select at most one per row) [Category 2]"][index]
            category3 = entry["Project categories (please select at most one per row) [Category 3]"][index]
            category4 = entry["Project categories (please select at most one per row) [Category 4]"][index]

            newPost.content = postContent
            newPost.author = "python-bot"
            #print(newPost.content)
            newPost.id = wp.call(posts.NewPost(newPost))
            del(newPost)
            time.sleep(1)
            



#vars(template)

template.thumbnail
test = template.thumbnail
for key in test.keys():
    pass

test["link"]=
test



print(postString)


vars(template[0])


vars(newPost)


entry
