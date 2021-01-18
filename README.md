# Fractal-Dimension_50_US_States

This program is designed to calculate the fractal dimension of each of 50 US states.
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

Process of the project:

1. Web scrape the 50 outline images of the states off of this website:
https://www.youtube.com/watch?v=gB9n2gHsHN4
(Beautiful Soup)

2. Resize the images to be 2000 x 2000 pixels
(Image from Pillow)

3. Cut the images up into evenly sized squares

4. Check if the state's outline is in the image:
  - Tint the image some color
  - Store that data

5. Stitch the bits back together and store the image files

6. Run statistical analysis to calculate fractal dimension of each state

7. Represent the data with MatPlotLib
(MatPlotLib)

8. Build GUI to show off all the data and images
(Tkinter)
