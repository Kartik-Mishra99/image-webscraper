
from bs4 import BeautifulSoup as bs
import os
import json
import urllib.request
import urllib.parse
import urllib.error
from urllib.request import urlretrieve

class ScrapperImage:
    
   
    def createImageUrl(searchterm):
        searchterm=searchterm.split()
        searchterm="+".join(searchterm)
        web_url="https://www.google.co.in/search?q=" + searchterm + "&source=lnms&tbm=isch"
        return web_url
    
    def scrap_html_data(url,header):
        request=urllib.request.Request(url,headers=header)
        response = urllib.request.urlopen(request)
        responseData = response.read()
        html = bs(responseData, 'html.parser')
        return html
    
    def getimageUrlList(rawHtml):
        imageUrlList = []
        for a in rawHtml.find_all("div", {"class": "rg_meta"}):
            link, imageExtension = json.loads(a.text)["ou"], json.loads(a.text)["ity"]
            imageUrlList.append((link, imageExtension))

        print("total", len(imageUrlList), "images found")
        return imageUrlList
    
    def downloadImagesFromURL(imageUrlList,image_name, header):
        masterListOfImages = []
        count=0
        imageFiles = []
        imageTypes = []
        image_counter=0
        for i, (img, Type) in enumerate(imageUrlList):
            try:
                if (count >= 10):
                    break
                else:
                    count = count + 1
                req = urllib.request.Request(img, headers=header)
                try:
                    urllib.request.urlretrieve(img,"./static/"+image_name+str(image_counter)+".jpg")
                    image_counter=image_counter+1
                except Exception as e:
                    print("Image write failed:  ",e)
                    image_counter = image_counter + 1
                respData = urllib.request.urlopen(req)
                raw_img = respData.read()
                imageFiles.append(raw_img)
                imageTypes.append(Type)

            except Exception as e:
                print("could not load : " + img)
                print(e)
                count = count + 1
        masterListOfImages.append(imageFiles)
        masterListOfImages.append(imageTypes)

        return masterListOfImages
    
    def delete_downloaded_images(self,list_of_images):
        for self.image in list_of_images:
            try:
                os.remove("./static/"+self.image)
            except Exception as e:
                print('error in deleting:  ',e)
        return 0
    
   
    
    
    
    