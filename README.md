# Cloud-Image-Detection
This project aims to automate the identification of cloudy areas at night from satellite imagery using the Cities at Night dataset with OpenCV. Clouds from night time data are much harder to identify compared to their daylight images. This is mainly due to the fact that it is challenging to distinguish between areas with no light and clouds. All images are from the [Cities at Night dataset](https://pmisson.carto.com/viz/281a7eb6-fa7a-11e4-8522-0e853d047bba/public_map).

### Image Processing Algorithm

1. As these are satellite images, they come in raw formats (NEF) and thus must first be converted to BGR format. 

![Alt text](Show/im1.jpg?raw=true "Title") 
![Alt text](Show/im2.jpg?raw=true "Title") 
![Alt text](Show/im3.jpg?raw=true "Title") 

2. Similar images of the same general terrain (such as the 3 images above) can be stitched into one composite image.

![Alt text](Show/stitched.jpg?raw=true "Title") 


3. The composite image has it's contrast increased to highlight artificial lighting and is then converted to a grayscale image. As can be seen in the grayscale image, the clouds seem to primarily be in the bottom right and left corners.

![Alt text](Show/contrast.jpg?raw=true "Title") 
![Alt text](Show/gray.jpg?raw=true "Title") 


4. The grayscale image is then blurred with a Gaussian filter to reduce noise and remove isolated lighting.

![Alt text](Show/gblur.jpg?raw=true "Title") 


5. A high pass filter combined with thresholding is then used to identify heavily lighted areas (such as a city). 

![Alt text](Show/highP.jpg?raw=true "Title") 
![Alt text](Show/thresh.jpg?raw=true "Title") 



An initial cloud mask is then formed based on parameters such as image brightness and dimensions. The resulting mask is then opened to remove small isolated chunks. It is thresholded to refine the mask and then closed to smooth it out. Lastly, an alorigthm is run to fill holes within the mask. 





### Future Improvements
1. Extracting raw data from the Cities at Night dataset is currently time consuming and slow. Improvements can be made to speed up this process so large datasets can easily be formed.
2. Use machine learning techniques to improve algorithm performance. ML was not used due to time constraints and relatively small datasets.
3. Generate correct cloud masks for images in dataset so that algorithm output can be compared and used to improve itself.
