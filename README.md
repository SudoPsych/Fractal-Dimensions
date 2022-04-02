# Fractal-Dimension

This program implements a graphical user interface that accepts and maniuplates images from the user and performs image processing and mathematical analysis on them
to calculate the Hausdorff Dimension of the given image. The GUI stores and displays the maniuplated images used to calculate the dimension of the image
(preferably a fractal) as well as allowing the user to delete images, display plots, and add custom photos.

# Example Image of GUI

![GUI](https://github.com/SudoPsych/Fractal-Dimensions/blob/main/GUI_example.png?raw=true)
(matplotlib plot is separate window)

## Implementations:
> Web scraping
> Image Processing
> os pathing
> MatPlotLib
> Statistical Analysis
> Cool Maths
> csv files
> GUI

## Program Steps

1. Web scrape the 50 outline images of the American states off of this website:
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
