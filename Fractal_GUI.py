"""
1/24/21
"""

from tkinter import *
from tkinter.filedialog import askopenfilename
from PIL import ImageTk
from Process_Images import Fractal
from Image_Pruning import *
import matplotlib.pyplot as plt
import numpy as np
import os


root = Tk()

class GUI():

    def __init__(self, root_):

        self._Fractal = Fractal()
        self.root = root_
        self.root.configure(background="#090C40")
        self.root.title('Fractal Dimension')
        # Create central canvas to display images
        self.canvas = Canvas(self.root, height = 500, width = 500)
        self.canvas.grid(row=1, rowspan=5, column=1, columnspan=4)
        self.img = None
        # Path to image that is modifiable
        self.c_s_dir = 'Custom'
        self.img_dir = 'original'
        self.img_name = 'serp'
        self.current_img = 'image_data/Custom/original/serp.png'
        self.chosen_path = ''
        self.highlighted_index = 0
        self.highlighted_list = [pic for pic in os.listdir('image_data/Custom/highlighted/serp')]

        self.original     = Button(self.root, text="original",    width=11, bg = "#07939F")
        self.binary       = Button(self.root, text="Binary",      width=11, bg = "#07939F")
        self.skeleton     = Button(self.root, text="Skeleton",    width=11, bg = "#07939F")
        self.choose       = Button(self.root, text="Choose File", width=30, bg = "#07939F")
        self.previous     = Button(self.root, text="<",           width=3,  bg = "#07939F")
        self.next_        = Button(self.root, text=">",           width=3,  bg = "#07939F")
        self.highlighted  = Button(self.root, text="Highlighted", width=11,  bg = "#07939F")
        self.plot         = Button(self.root, text="Plot",        width=11, bg = "#07939F")
        self.upload       = Button(self.root, text="Upload",      width=11, bg = "#07939F")
        self.c_s_button   = Button(self.root, text="Custom",      width=11, bg = "#07939F")
        self.delete_img   = Button(self.root, text="Delete",      width=11, bg = "#07939F")

        self.clicked = StringVar(self.root)
        self.clicked.set('serp')
        self.img_options = [name.split('.')[0] for name in os.listdir('image_data/Custom/binary')]
        self.dropdown = OptionMenu(self.root,
                                   self.clicked,
                                   *self.img_options,
                                   command=lambda clicked=self.clicked: self.dropdown_command(clicked))
        self.dropdown.configure(bg = "#07939F")

        return




    # Button functions
    def put_image(self, img_path):
        # Display new image in central canvas

        # Open, resize, open with tk, and display to canvas
        img = Image.open(img_path)
        img = img.resize((500, 500))
        self.img = ImageTk.PhotoImage(img)
        self.canvas.create_image(0,0, anchor=NW, image=self.img)

        return




    def change_dir(self, dir_name):
        # Button command to change path to image, this one is for bin_high_orig_skel
        self.img_dir = dir_name
        self.current_img = "image_data/{}/{}/{}.png".format(self.c_s_dir, self.img_dir, self.img_name)
        self.put_image(self.current_img)

        return



    def highlighted_command(self):

        self.img_dir = 'highlighted'
        self.highlighted_list = []
        self.highlighted_intex = 0

        for pic in os.listdir("image_data/{}/highlighted/{}".format(self.c_s_dir, self.img_name)):
            self.highlighted_list.append("image_data/{}/highlighted/{}/{}".format(self.c_s_dir, self.img_name, pic))
        self.current_img = self.highlighted_list[self.highlighted_index]

        self.put_image(self.current_img)

        return




    def pre_nex(self, pre_or_nex):

        if self.img_dir is not 'highlighted':
            return

        if pre_or_nex == 'nex' and self.highlighted_index is not 9:
            self.highlighted_index += 1

        elif pre_or_nex == 'pre' and self.highlighted_index is not 0:
            self.highlighted_index -= 1
        else:
            return

        self.current_img = self.highlighted_list[self.highlighted_index]
        self.put_image(self.current_img)

        return



    def delete_confirm(self):
        # Asks user to confirm deletion

        delete_window = Tk()
        img_to_delete = self.img_name

        if self.c_s_dir != "Custom" or img_to_delete == 'serp':

                delete_window.title("Oops")
                message = Label(delete_window, text="You cannot delete this image.")
                ok = Button(delete_window, text="Ok", command=delete_window.destroy)

                message.pack()
                ok.pack()

        else:

            delete_window.title("Delete?")

            message = Label(delete_window, text="Are you sure you want to delete {}?".format(self.img_name))
            confirm = Button(delete_window, text="Yes", width=10,
                             command=lambda : self.delete_command(delete_window, img_to_delete))
            deny = Button(delete_window, text="No", width=10, command=delete_window.destroy)

            message.grid(row=0, column=0, columnspan=2)
            confirm.grid(row=1, column=0)
            deny.grid(row=1, column=1)


        return



    def delete_command(self, window, img_to_delete):
        # Select and delete entry in Custom dir

        # Delete images and csv file
        os.remove("image_data/Custom/binary/{}.png".format(img_to_delete))
        os.remove("image_data/Custom/original/{}.png".format(img_to_delete))
        os.remove("image_data/Custom/skeleton/{}.png".format(img_to_delete))
        os.remove("image_data/Custom/csv_data/{}.csv".format(img_to_delete))

        # Delete images in highlighted folder then highlighted dir
        files = os.listdir("image_data/Custom/highlighted/" + img_to_delete)
        for file in files:
            os.remove("image_data/Custom/highlighted/{}/{}".format(img_to_delete, file))
        os.rmdir("image_data/Custom/highlighted/" + img_to_delete)

        # Set image to Serp triangle
        self.c_s_dir = 'Custom'
        self.img_dir = 'original'
        self.img_name = 'serp'
        self.current_img = 'image_data/Custom/original/serp.png'
        self.put_image(self.current_img)

        # Update the option menu
        self.remake_dropdown()
        self.clicked.set('serp')

        window.destroy()

        return




    def upload_command(self):
        # Allow user to input their own image for analysis

        # Check if file chosen is a valid image.
        try:
            Image.open(self.chosen_path)
        except:
            return

        # Get name of image file
        name = os.path.basename(self.chosen_path).split('.')[0]

        # Create path strings for easy use
        original_path = "image_data/Custom/original/{}.png".format(name)
        bin_path      = "image_data/Custom/binary/{}.png".format(name)
        skeleton_path = "image_data/Custom/skeleton/{}.png".format(name)
        csv_file_path = "image_data/Custom/csv_data/{}.csv".format(name)

        # Resize image to 2000 x 2000 and convert to png file
        # Store in 'original' dir

        resized_image = resize_(self.chosen_path)
        resized_image.save(original_path)
        print('resize complete')

        # Convert to binary and save to 'binary' dir
        bin_image = convert_to_binary(original_path)
        bin_image.save(bin_path)
        print('bin complete')

        # Skeletonize the image and save in skeleton dir
        skeleton_image = skeletonize_(bin_path)
        skeleton_image.save(skeleton_path)
        print('skele complete')
        
        # Split image up and save pictures to highlighted dir
        img_data, pictures = self._Fractal.split_image(bin_path, skeleton_path)
        self._Fractal.store_images(pictures, name, "Custom")
        print('images stored')

        # Do fancy math and store data in csv file to proper dir
        graph_data = self._Fractal.calculate_fractal_dimensions(img_data)
        self._Fractal.data_to_file(csv_file_path, graph_data)
        print('data stored')

        self.c_s_dir = 'Custom'
        self.img_dir = 'original'
        self.img_name = name
        self.current_img = original_path
        self.put_image(self.current_img)

        # Update the option menu
        self.remake_dropdown()
        self.clicked.set(self.img_name)

        self.chosen_path = ''
        self.choose["text"] = "Choose File"

        return




    def choose_file_command(self):
        # Allow user to choose file from computer

        # Gets user input
        self.chosen_path = askopenfilename()
        # Set text on button to the name of that file
        name = os.path.basename(self.chosen_path)
        if self.chosen_path == "":
            self.choose['text'] = "Choose File"
        else:
            self.choose['text'] = name

        return




    def plot_command(self):
        # Display the tkinter plot from the data in the csv file

        path = "image_data/{}/csv_data/{}.csv".format(self.c_s_dir, self.img_name)
        s_f, b_r, f_d, m, b = self._Fractal.get_data(path)

        fig, ax = plt.subplots()
        fig.canvas.set_window_title(self.img_name)
        # Turning lists into numpy arrays cuz matplotlib is picky
        s_f = np.array(s_f)
        b_r = np.array(b_r)
        # Axes
        ax.set_title("Fractal Dimension of {} = {}".format(self.img_name, str(round(m,4))))
        ax.set_xlabel('log(Scaling Factor)')
        ax.set_ylabel('log(Block Ratio)')
        # Scatter plot for values and line of best fit
        ax.scatter(s_f, b_r, label="Calculated Values", color='b')
        ax.plot(s_f, (m * s_f) + b, label="Line of best fit", color='r')

        ax.legend()

        plt.show()

        return



    def dropdown_command(self, clicked):

        self.img_name = clicked
        self.img_dir  = 'original'
        self.current_img = 'image_data/{}/{}/{}.png'.format(self.c_s_dir, self.img_dir, self.img_name)
        self.put_image(self.current_img)
        self.highlighted_index = 0

        return



    def remake_dropdown(self):

        self.dropdown.destroy()
        self.img_options = [name.split('.')[0] for name in os.listdir("image_data/{}/binary".format(self.c_s_dir))]
        self.dropdown = OptionMenu(self.root,
                                   self.clicked,
                                   *self.img_options,
                                   command=lambda clicked=self.clicked: self.dropdown_command(clicked))
        self.dropdown.grid(row=2, column=0)
        self.dropdown.configure(bg = "#07939F")

        return



    def c_s_command(self):
        # Switch between custom dir and states dir

        if self.c_s_dir == "Custom":
            self.c_s_button['text'] = "States"
            self.c_s_dir = 'States'
            self.img_dir = 'original'
            self.img_name = 'Alabama'
            self.current_img = 'image_data/States/original/Alabama.png'
            self.clicked.set(self.img_name)
            self.put_image(self.current_img)

        else:
            self.c_s_button['text'] = "Custom"
            self.c_s_dir = 'Custom'
            self.img_dir = 'original'
            self.img_name = 'serp'
            self.current_img = 'image_data/Custom/original/serp.png'
            self.clicked.set(self.img_name)
            self.put_image(self.current_img)

        self.remake_dropdown()

        return

    def place_widgets(self):
        # duh buttons :) smile

        self.original.grid(   row=1, column=5)
        self.binary.grid(     row=2, column=5)
        self.skeleton.grid(   row=3, column=5)
        self.choose.grid(     row=6, column=2)
        self.previous.grid(   row=0, column=3)
        self.next_.grid(      row=0, column=4)
        self.highlighted.grid(row=4, column=5)
        self.plot.grid(       row=5, column=5)
        self.upload.grid(     row=6, column=1)
        self.c_s_button.grid( row=1, column=0)
        self.delete_img.grid( row=6, column=5)

        self.original['command']    = lambda : self.change_dir("original")
        self.binary['command']      = lambda : self.change_dir("binary")
        self.skeleton['command']    = lambda : self.change_dir("skeleton")
        self.choose['command']      = self.choose_file_command
        self.previous['command']    = lambda : self.pre_nex("pre")
        self.next_['command']       = lambda : self.pre_nex("nex")
        self.highlighted['command'] = self.highlighted_command
        self.plot['command']        = self.plot_command
        self.upload['command']      = self.upload_command
        self.c_s_button['command']  = self.c_s_command
        self.delete_img['command']  = self.delete_confirm

        self.dropdown.grid(row=2, column=0)

        return




    def main(self):

        self.put_image(self.current_img)
        self.place_widgets()
        self.root.mainloop()

        return

if __name__ == '__main__':
    GUI(root).main()
