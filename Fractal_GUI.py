"""
1/24/21
"""

from tkinter import *
from tkinter.filedialog import askopenfilename
from PIL import ImageTk
from Process_Images import Fractal
from Image_Pruning import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


root = Tk()

class GUI():

    def __init__(self, root_):

        self._Fractal = Fractal()
        self.root = root_
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

        self.original     = Button(self.root, text="original",    width=11)
        self.binary       = Button(self.root, text="Binary",      width=11)
        self.skeleton     = Button(self.root, text="Skeleton",    width=11)
        self.choose       = Button(self.root, text="Choose File", width=11)
        self.previous     = Button(self.root, text="<",           width=3)
        self.next_        = Button(self.root, text=">",           width=3)
        self.highlighted  = Button(self.root, text="Highlighted", width=11)
        self.test         = Button(self.root, text="Test",        width=11)
        self.upload       = Button(self.root, text="Upload",      width=11)

        self.clicked = StringVar(self.root)
        self.clicked.set('serp')
        self.img_options = [name.split('.')[0] for name in os.listdir('image_data/Custom/binary')]
        self.dropdown = OptionMenu(self.root,
                                   self.clicked,
                                   *self.img_options,
                                   command=lambda clicked=self.clicked: self.dropdown_command(clicked))

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
        self.current_img = 'image_data/' + self.c_s_dir + '/' + self.img_dir + '/' + self.img_name + '.png'
        self.put_image(self.current_img)

        return



    def highlighted_command(self):

        self.img_dir = 'highlighted'
        self.highlighted_list = []
        self.highlighted_intex = 0
        for pic in os.listdir('image_data/' + self.c_s_dir + '/highlighted/' + self.img_name):
            self.highlighted_list.append('image_data/' + self.c_s_dir + '/highlighted/' + self.img_name + '/' + pic)
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




    def delete_command(self):
        # Select and delete entry in Custom dir
        pass




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
        original_path = 'image_data/Custom/original/' + name + '.png'
        bin_path      = 'image_data/Custom/binary/'   + name + '.png'
        skeleton_path = 'image_data/Custom/skeleton/' + name + '.png'
        csv_file_path = 'image_data/Custom/csv_data/' + name + '.csv'

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
        self._Fractal.store_images(pictures, name)
        print('images stored')

        # Do fancy math and store data in csv file to proper dir
        graph_data = self._Fractal.calculate_fractal_dimensions(img_data)
        self._Fractal.data_to_file(csv_file_path, graph_data)
        print('data stored')

        # Update the option menu
        self.dropdown.destroy()
        self.img_options.append(name)
        self.dropdown = OptionMenu(self.root,
                                   self.clicked,
                                   *self.img_options,
                                   command=lambda clicked=self.clicked: self.dropdown_command(clicked))
        self.dropdown.grid(row=1, column=0)

        self.c_s_dir = 'Custom'
        self.img_dir = 'original'
        self.img_name = name
        self.current_img = original_path
        self.put_image(self.current_img)

        return




    def choose_file_command(self):
        # Allow user to choose file from computer

        # Gets user input
        self.chosen_path = askopenfilename()
        # Set text on button to the name of that file
        name = os.path.basename(self.chosen_path)
        self.choose['text'] = name
        return




    def test_command(self):

        pass



    def dropdown_command(self, clicked):

        self.img_name = clicked
        self.img_dir  = 'original'
        self.current_img = 'image_data/' + self.c_s_dir + '/' + self.img_dir + '/' + self.img_name + '.png'
        self.put_image(self.current_img)



    def place_widgets(self):
        # duh buttons :) smile

        self.original.grid(   row=1, column=5)
        self.binary.grid(     row=2, column=5)
        self.skeleton.grid(   row=3, column=5)
        self.choose.grid(     row=6, column=2)
        self.previous.grid(   row=0, column=3)
        self.next_.grid(      row=0, column=4)
        self.highlighted.grid(row=4, column=5)
        self.test.grid(       row=5, column=5)
        self.upload.grid(     row=6, column=1)

        self.original['command']    = lambda dir_name = 'original'  : self.change_dir(dir_name)
        self.binary['command']      = lambda dir_name = 'binary'    : self.change_dir(dir_name)
        self.skeleton['command']    = lambda dir_name = 'skeleton'  : self.change_dir(dir_name)
        self.choose['command']      = self.choose_file_command
        self.previous['command']    = lambda pre      = 'pre'       : self.pre_nex(pre)
        self.next_['command']       = lambda nex      = 'nex'       : self.pre_nex(nex)
        self.highlighted['command'] = self.highlighted_command
        self.test['command']        = self.test_command
        self.upload['command']      = self.upload_command

        self.dropdown.grid(row=1, column=0)

        return




    def main(self):

        self.put_image(self.current_img)
        self.place_widgets()
        self.root.mainloop()

if __name__ == '__main__':
    GUI(root).main()
