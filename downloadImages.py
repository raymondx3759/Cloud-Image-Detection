from selenium import webdriver
import time
import shutil

#
def downloadImage(ISSNum, frameNum):
    driver = webdriver.Safari()
    url = "https://eol.jsc.nasa.gov/SearchPhotos/RequestOriginalImage.pl?mission=ISS" + ISSNum + "&roll=E&frame="
    url += frameNum + "&file=iss" + ISSNum + "e" + frameNum + ".NEF"
    # print (url)
    driver.get(url)
    #Server requests may take up to 6 minutes so sleep to guarantee download
    time.sleep(360)
    driver.find_element_by_link_text("this link").click()
    #Sleep so file can be downloaded
    time.sleep(15)
    print ("Done downloading")
    driver.quit()
    return (ISSNum, frameNum)

ISSNum, frameNum = downloadImage("035", "017200")
image = "iss" + ISSNum + "e" + frameNum + ".NEF" 
newDir = shutil.move(image, "../Desktop/Year2(19-20)/Summer 20/Cloud-Image-Detection/Images")
print ("The image " + image + "was moved to " + newDir)

