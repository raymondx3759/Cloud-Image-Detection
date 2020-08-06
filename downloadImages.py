from selenium import webdriver
import time
import shutil

#Downloads satellite image (NEF) from Cities at Night interactive website with given string parameters
#Every image can be found at "https://pmisson.carto.com/viz/281a7eb6-fa7a-11e4-8522-0e853d047bba/public_map"
def downloadImage(ISSNum, frameNum):
    assert(isinstance(ISSNum, str) and isinstance(frameNum, str))
    #Uses Safari to download image; can change to other browsers
    driver = webdriver.Safari()
    url = "https://eol.jsc.nasa.gov/SearchPhotos/RequestOriginalImage.pl?mission=ISS" + ISSNum + "&roll=E&frame="
    url += frameNum + "&file=iss" + ISSNum + "e" + frameNum + ".NEF"
    driver.get(url)
    #Server requests may take up to 6 minutes so sleep to guarantee download
    time.sleep(360)
    driver.find_element_by_link_text("this link").click()
    #Sleep so file can be downloaded
    time.sleep(10)
    print ("Done downloading")
    driver.quit()
    return (ISSNum, frameNum)

#Replace ISSNum and frameNum with respective strings ex. "030", "162833"
ISSNum, frameNum = None, None
ISSNum, frameNum = downloadImage(ISSNum, frameNum)
image = "iss" + ISSNum + "e" + frameNum + ".NEF" 
#Moves image from Downloads to specified directory for ease of access
newDir = shutil.move(image, "../Desktop/Year2(19-20)/Summer 20/Cloud-Image-Detection/Images")
print ("The image " + image + "was moved to " + newDir)

