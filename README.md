# Cloud-Image-Detection
This project aims to automate the identification of cloudy areas at night from satellite imagery using the Cities at Night dataset with OpenCV. Clouds from night time data are much harder to identify compared to their daylight images. This is mainly due to the fact that it is challenging to distinguish between areas with no light and clouds. All images are from the [Cities at Night dataset](https://pmisson.carto.com/viz/281a7eb6-fa7a-11e4-8522-0e853d047bba/public_map).

### Image Processing Algorithm

As these are satellite images, they come in raw formats (NEF) and thus must first be converted to BGR format. Similar images of the same general terrain can be stitched into one composite image.

The composite image has it's contrast increased to highlight artificial lighting and is then converted to a grayscale image. It is blurred with a Gaussian filter to reduce noise and remove isolated lighting. A high pass filter combined with thresholding is then used to identify heavily lighted areas (such as a city). An initial cloud mask is then formed based on parameters such as image brightness and dimensions. The resulting mask is then opened to remove small isolated chunks. It is thresholded to refine the mask and then closed to smooth it out. Lastly, an alorigthm is run to fill holes within the mask. 
