import tkinter as tk                # python 3
from tkinter import font as tkfont # python 3
import tkinter
from tkinter import filedialog
import os
"""
Change secret message to be dealt like file path
"""


class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Calibri', size=18, weight="bold")
        self.normal_font = tkfont.Font(family='Calibri', size=15, weight="bold")

        self.title("StegBeetle")
        self.geometry("600x500")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, Hide, Discover, HideSecretMessage_Message, HideSecretMessage_Input_File, HideSecretMessage_Ouput_Dir, Hide_Confirmation): #Intiate containers
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="StegBeetle", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        hide_button = tk.Button(self, text="Hide",
                            command=lambda: controller.show_frame("Hide"))
        discover_button = tk.Button(self, text="Discover",
                            command=lambda: controller.show_frame("Discover"))



        hide_button.pack()
        discover_button.pack()




class Hide(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Hide", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        label = tk.Label(self, text="What would you like to hide?", font=controller.normal_font)
        label.pack(fill="x", pady=10)

        hide_message_button = tk.Button(self, text="Secret Message",
                           command=lambda: controller.show_frame("HideSecretMessage_Message"))

        hide_mp3_button = tk.Button(self, text="MP3",
                           command=lambda: controller.show_frame("StartPage"))

        home_button = tk.Button(self, text="Home",
                           command=lambda: controller.show_frame("StartPage"))

        hide_message_button.pack()
        hide_mp3_button.pack()
        home_button.pack(side="bottom", pady=10)




class Discover(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Discover", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        home_button = tk.Button(self, text="Home",
                           command=lambda: controller.show_frame("StartPage"))
        home_button.pack(side="bottom", pady=10)


class HideSecretMessage_Message(tk.Frame):

    def updateSecret(self):
        global secret_message
        secret_message = self.secretMessage.get()
        #print("updateSecret: "+secret_message)
        write_secret(secret_message)
        self.controller.show_frame("HideSecretMessage_Input_File")

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        labelTitle = tk.Label(self, text="Hide: Secret Message", font=controller.title_font)

        labelSecret = tk.Label(self, text="What is your secret message?", font=controller.normal_font)
        self.secretMessage = tk.StringVar()
        entryLabel = tk.Label(self, textvariable=self.secretMessage)
        mEntry = tk.Entry(self, bd=4, relief='sunken', textvariable=self.secretMessage)

        start_button = tk.Button(self, text="Start Steganography",
                           command= lambda: self.updateSecret())

        home_button = tk.Button(self, text="Home",
                           command=lambda: controller.show_frame("StartPage"))

        labelTitle.pack(side="top", fill="x", pady=10)
        labelSecret.pack(fill="x", pady=10)
        entryLabel.pack()
        mEntry.pack()
        start_button.pack()
        home_button.pack(side="bottom", pady=10)

class HideSecretMessage_Input_File(tk.Frame):

    def find_file(self):
        global filepath
        filepath = file_grabber()
        write_filepath(filepath)

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)

        self.controller = controller

        self.labelTitle = tk.Label(self, text="Hide: Finding File", font=controller.title_font)

        self.labelSecret = tk.Label(self, text="Navigate to the file you would like to \n embed your message into", font=controller.normal_font)

        find_button = tk.Button(self, text="...",
                           command=self.find_file)

        start_button = tk.Button(self, text="Continue",
                           command=lambda: controller.show_frame("HideSecretMessage_Ouput_Dir"))

        home_button = tk.Button(self, text="Home",
                           command=lambda: controller.show_frame("StartPage"))

        self.labelTitle.pack(side="top", fill="x", pady=10)
        self.labelSecret.pack(fill="x", pady=10)
        find_button.pack()
        home_button.pack(side="bottom", pady=10)
        start_button.pack(side="bottom", pady=100)


class HideSecretMessage_Ouput_Dir(tk.Frame):

    def find_file(self):
        global output_filepath
        output_filepath = dir_grabber()
        write_output(output_filepath)


    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)

        self.controller = controller

        self.labelTitle = tk.Label(self, text="Hide: Output File", font=controller.title_font)

        self.labelSecret = tk.Label(self, text="Navigate to the file you would like \n to store your stegged picture", font=controller.normal_font)

        find_button = tk.Button(self, text="...",
                           command=self.find_file)

        start_button = tk.Button(self, text="Start Steganography",
                           command=lambda: controller.show_frame("Hide_Confirmation"))

        home_button = tk.Button(self, text="Home",
                           command=lambda: controller.show_frame("StartPage"))

        self.labelTitle.pack(side="top", fill="x", pady=10)
        self.labelSecret.pack(fill="x", pady=10)
        find_button.pack()
        home_button.pack(side="bottom", pady=10)
        start_button.pack(side="bottom", pady=100)

class Hide_Confirmation(tk.Frame):

    def updateLabel(self):
        global filepath, secret_message, output_filepath
        #print(filepath)
        self.labelInputPath.config(text=filepath)
        self.labelFilePath.config(text=output_filepath)
        self.labelSecretMessage.config(text=secret_message)
        #print(secret_message)


    def __init__(self, parent, controller):
        global filepath
        tk.Frame.__init__(self, parent)


        self.controller = controller

        self.labelTitle = tk.Label(self, text="Hide: Confirmation", font=controller.title_font)

        self.labelSecretMessageTitle = tk.Label(self, text="Your Secret Message", font=controller.normal_font)
        self.labelSecretMessage = tk.Label(self, text=secret_message, font=controller.normal_font)

        self.labelInputPathTitle = tk.Label(self, text="Input You've Chosen", font=controller.normal_font)
        self.labelInputPath = tk.Label(self, text=filepath, font=controller.normal_font)

        self.labelFilePathTitle = tk.Label(self, text="Output File You've Chosen", font=controller.normal_font)
        self.labelFilePath = tk.Label(self, text=output_filepath, font=controller.normal_font)

        home_button = tk.Button(self, text="Home",
                           command=lambda: controller.show_frame("StartPage"))

        update_button = tk.Button(self, text="Click to load your choices",
                           command=self.updateLabel)

        self.labelSecretMessage.config(bg="light blue")
        self.labelInputPath.config(bg="light yellow")
        self.labelFilePath.config(bg="light green")


        self.labelTitle.pack(side="top", fill="x", pady=10)
        self.labelSecretMessageTitle.pack(side="top", fill="x", pady=10)
        self.labelSecretMessage.pack(side="top", fill="x", pady=10)
        self.labelInputPathTitle.pack(side="top", fill="x", pady=10)
        self.labelInputPath.pack(side="top", fill="x", pady=10)
        self.labelFilePathTitle.pack(side="top", fill="x", pady=10)
        self.labelFilePath.pack(side="top", fill="x", pady=10)\

        update_button.pack()
        home_button.pack(side="bottom", pady=10)



def file_grabber():
    root = tkinter.Tk()
    root.withdraw()
    currdir = os.getcwd()
    selected_dir = filedialog.askopenfilename(parent=root, initialdir=currdir, title='Please select a directory')
    return selected_dir

def dir_grabber():
    root = tkinter.Tk()
    root.withdraw()
    currdir = os.getcwd()
    selected_dir = filedialog.askdirectory(parent=root, initialdir=currdir, title='Please select a directory')
    return selected_dir

def config_loader():
    global filepath, secret_message, output_filepath
    with open('StegBeetle_config.txt') as config_file:
        for i, line in enumerate(config_file):
            if i == 0:# 1st line: filepath
                filepath = line
            elif i == 1:# 2nd line: secret_message
                secret_message = line
            elif i == 2: #3rd line: output_path
                output_filepath = line

def write_filepath(new_filepath):
    with open('StegBeetle_config.txt', 'r') as config_file:
        # read a list of lines into data
        data = config_file.readlines()

    # now change the 1st line, note that you have to add a newline
    data[0] = new_filepath + '\n'

    # and write everything back
    with open('StegBeetle_config.txt', 'w') as file:
        file.writelines(data)
        #print(data)


def write_secret(new_secret):
    with open('StegBeetle_config.txt', 'r') as config_file:
        # read a list of lines into data
        data = config_file.readlines()

    # now change the 2nd line, note that you have to add a newline
    data[1] = new_secret + '\n'

    # and write everything back
    with open('StegBeetle_config.txt', 'w') as file:
        file.writelines(data)
        #print(data)

def write_output(new_output):
    with open('StegBeetle_config.txt', 'r') as config_file:
        # read a list of lines into data
        data = config_file.readlines()

    # now change the 3rd line, note that you have to add a newline
    data[2] = new_output + '\n'

    # and write everything back
    with open('StegBeetle_config.txt', 'w') as file:
        file.writelines(data)
        #print(data)


filepath = ""
secret_message = ""
output_filepath = ""

if __name__ == "__main__":
    config_loader()
    app = SampleApp()
    app.mainloop()


"""
WEAKNESS:
Config File means not an independent program that doesn't do everything on its own. Advantage of using it: makes sharing info between scripts easy. Also allows users to come back to sessions, as their options are saved.
Multiple scripts because python version differences means its not standalone. Advantage: means I can use python2 libraries, expanding usability. 
"""