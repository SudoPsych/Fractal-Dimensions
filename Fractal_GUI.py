"""
1/24/21
Program will store images user has input, current or past.
"""

from tkinter import *
from PIL import Image, ImageTk
from Process_Images import Fractal

root = Tk()

class GUI():

    def __init__(self, root):

        self._Fractal = Fractal()
        self.root = root
        self.root.title('Fractal Dimension')
        self.img = None
        # Create central canvas to display images
        self.canvas = Canvas(self.root, height = 500, width = 500)
        self.canvas.grid(row=1, rowspan=5, column=1, columnspan=4)
        # Path to image that is modifiable
        self.c_s_dir = 'Custom'
        self.img_dir = 'binary'
        self.img_name = 'serp.png'
        self.current_img = 'image_data/' + self.c_s_dir + '/' + self.img_dir + '/' + self.img_name



    # Button functions
    def put_image(self, img_path):
        # Display new image in central canvas

        # Open, resize, open with tk, and display to canvas
        img = Image.open(img_path)
        img = img.resize((500, 500))
        self.img = ImageTk.PhotoImage(img)
        self.canvas.create_image(0,0, anchor=NW, image=self.img)


    def change_dir(self, dir_name):
        # Button command to change path to image, this one is for bin_high_orig_skel
        self.img_dir = dir_name
        self.current_img = 'image_data/' + self.c_s_dir + '/' + self.img_dir + '/' + self.img_name
        self.put_image(self.current_img)

        return

    def test_command(self):
        print(self.img_dir)
        pass

    def create_buttons(self):
        # duh buttons :) smile

        original =     Button(self.root, text="original",    width = 11)
        binary =       Button(self.root, text="Binary",      width = 11)
        skeleton =     Button(self.root, text="Skeleton",    width = 11)
        highlighted =  Button(self.root, text="Highlighted", width = 11)
        test        =  Button(self.root, text="Test",        width = 11)
        upload =       Button(self.root, text="Upload",      width = 11)
        choose =       Button(self.root, text="Choose File", width = 11)
        previous =     Button(self.root, text="<",           width = 3)
        next_ =        Button(self.root, text=">",           width = 3)

        original.grid(   row = 1, column = 5)
        binary.grid(     row = 2, column = 5)
        skeleton.grid(   row = 3, column = 5)
        highlighted.grid(row = 4, column = 5)
        test.grid(       row = 5, column = 5)
        upload.grid(     row = 6, column = 1)
        choose.grid(     row = 6, column = 2)
        previous.grid(   row = 0, column = 3)
        next_.grid(      row = 0, column = 4)

        original['command']    = lambda dir_name = 'original'  : self.change_dir(dir_name)
        binary['command']      = lambda dir_name = 'binary'    : self.change_dir(dir_name)
        skeleton['command']    = lambda dir_name = 'skeleton'  : self.change_dir(dir_name)
        highlighted['command'] = lambda dir_name = 'highlighted': self.change_dir(dir_name)
        test['command']        = self.test_command
        upload['command']      = self.test_command
        choose['command']      = self.test_command
        previous['command']    = self.test_command
        next_['command']       = self.test_command

    def main(self):

        self.put_image("image_data/Custom/original/serp.png")
        self.create_buttons()
        self.root.mainloop()


GUI(root).main()
