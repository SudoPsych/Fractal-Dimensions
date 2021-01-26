# Fractal-Dimension_50_US_States

This program is designed to calculate the fractal dimension of each of 50 US states (and any user inputed image).
I got the idea for this project from 3Blue1Brown's video about fractals and thought it would be a 
cool thing to try out for myself. Link to video here -> https://www.youtube.com/watch?v=gB9n2gHsHN4

This is another project intented to expand my breadth of knowledge of Python and programming in general.

The program uses:
- Web scraping
- Image Processing
- os pathing
- MatPlotLib
- Statistical Analysis
- Cool Maths
- csv files
- GUI

Process of the project:

1. Web scrape the 50 outline images of the states off of this website:
https://gisgeography.com/state-outlines-blank-maps-united-states/
(Beautiful Soup)

2. Resize, convert to binary, and skeletonize the image.
(Image, ImageStat, ImageChops from Pillow)
(skeletonize from skimage.morphology)

3. Cut the images up into evenly sized squares

4. Check if the state's outline is in the image:
  - Tint the image some color
  - Store that data

5. Stitch the bits back together and store the image files

6. Run statistical analysis to calculate fractal dimension of each image

7. Store data in csv file, extract for next step
(csv)

8. Represent the data with MatPlotLib
(MatPlotLib.pyplot)

9. Build GUI to show off all the data and images
(Tkinter)
