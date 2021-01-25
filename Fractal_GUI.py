"""
1/24/21
Program will store images user has input, current or past.
"""

from tkinter import *
from PIL import Image, ImageTk

root = Tk()

class GUI():

    def __init__(self, root):

        self.root = root
        self.root.title('Fractal Dimension')
        self.img = None
        self.canvas = Canvas(self.root, height = 500, width = 500)
        self.canvas.grid(row=1, rowspan=5, column=1, columnspan=4)


    # Button functions
    def put_image(self, img_path):

        self.img = ImageTk.PhotoImage(Image.open(img_path))
        self.canvas.create_image(0,0, anchor=NW, image=self.img)



    def create_buttons(self):

        original =     Button(self.root, text="Original",    width = 11)
        binary =       Button(self.root, text="Binary",      width = 11)
        skeleton =     Button(self.root, text="Skeleton",    width = 11)
        highlighted =  Button(self.root, text="Highlighted", width = 11)
        upload =       Button(self.root, text="Upload",      width = 11)
        choose =       Button(self.root, text="Choose File", width = 11)
        previous =     Button(self.root, text="<",           width = 3)
        next_ =        Button(self.root, text=">",           width = 3)

        original.grid(   row = 1, column = 5)
        binary.grid(     row = 2, column = 5)
        skeleton.grid(   row = 3, column = 5)
        highlighted.grid(row = 4, column = 5)
        upload.grid(     row = 6, column = 1)
        choose.grid(     row = 6, column = 2)
        previous.grid(   row = 0, column = 3)
        next_.grid(      row = 0, column = 4)

    def main(self):

        self.put_image("thin_bin_outlines/Alaska.png")
        self.create_buttons()
        self.root.mainloop()


GUI(root).main()
