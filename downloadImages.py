from selenium import webdriver
import time
import csv
import pickle

#Parses .csv file downloaded from https://pmisson.carto.com/tables/darkskiesresult_cities/public and returns list of ~60,000 URLs of images in dataset
def getURLs(filePath):
    urlList = []
    with open(filePath) as file:
        data = csv.reader(file)
        #Skip first line because it is header
        skip = next(data)
        for row in data:
            nasaID, url = row[1], row[13]
            #Check that url is valid
            if (url.startswith('http://')):
                split = nasaID.split('-')
                url = "https://eol.jsc.nasa.gov/SearchPhotos/RequestOriginalImage.pl?mission=" + split[0] + "&roll=E&frame="
                url += split[-1] + "&file=" + split[0] + "e" + split[-1] + ".NEF"
                urlList.append(url)
    return urlList

#Downloads satellite image (.NEF) from Cities at Night interactive website with given url
#Every image can be found at "https://pmisson.carto.com/viz/281a7eb6-fa7a-11e4-8522-0e853d047bba/public_map"
def downloadImage(url):
    assert(isinstance(url, str))
    #Uses Safari to download image; can change to other browsers
    driver = webdriver.Safari()
    driver.get(url)
    #Server requests may take up to 6 minutes so sleep to guarantee download
    time.sleep(360)
    driver.find_element_by_link_text("this link").click()
    #Sleep so file can be downloaded
    time.sleep(10)
    print ("Done downloading")
    
def saveList(lst, filename):
    with open(filename, 'wb') as fp:
        pickle.dump(lst, fp)

def loadList(filename):
    with open (filename, 'rb') as fp:
        urls = pickle.load(fp)
    return urls

#Get URL list
filePath = 'darkskiesresult_cities.csv'
urls = getURLs(filePath)
#Save list for quick access
saveList(urls, filename='urls')
#Load list and begin downloading images 
urls = loadList(filename='urls')
for url in urls:
    downloadImage(url)



