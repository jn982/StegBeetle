import tkinter as tk                # python 3
from tkinter import font  as tkfont # python 3
import tkinter
from tkinter import filedialog
import os

class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold")
        self.normal_font = tkfont.Font(family='Helvetica', size=15, weight="bold")

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
        for F in (StartPage, Hide, Discover, HideSecretMessage_Message, HideSecretMessage_Dir): #Intiate containers
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
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        labelTitle = tk.Label(self, text="Hide: Secret Message", font=controller.title_font)

        labelSecret = tk.Label(self, text="What is your secret message?", font=controller.normal_font)
        secretMessage = tk.StringVar()
        entryLabel = tk.Label(self, textvariable=secretMessage)
        mEntry = tk.Entry(self, bd=4, relief='sunken', textvariable=secretMessage)
        start_button = tk.Button(self, text="Start Steganography",
                           command=lambda: controller.show_frame("HideSecretMessage_Dir"))
        home_button = tk.Button(self, text="Home",
                           command=lambda: controller.show_frame("StartPage"))

        labelTitle.pack(side="top", fill="x", pady=10)
        labelSecret.pack(fill="x", pady=10)
        entryLabel.pack()
        mEntry.pack()
        start_button.pack()
        home_button.pack(side="bottom", pady=10)

class HideSecretMessage_Dir(tk.Frame):

    def find_file(self):
        global filepath
        filepath = file_grabber()

    def test(self):
        print(filepath)


    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        labelTitle = tk.Label(self, text="Hide: Finding File", font=controller.title_font)

        labelSecret = tk.Label(self, text="Navigate to the file you would like to \n embed your message into", font=controller.normal_font)

        find_button = tk.Button(self, text="...",
                           command=self.find_file)

        home_button = tk.Button(self, text="Home",
                           command=lambda: controller.show_frame("StartPage"))

        labelTitle.pack(side="top", fill="x", pady=10)
        labelSecret.pack(fill="x", pady=10)
        find_button.pack()
        home_button.pack(side="bottom", pady=10)


def file_grabber():
    root = tkinter.Tk()
    root.withdraw()
    currdir = os.getcwd()
    selected_dir = filedialog.askopenfilename(parent=root, initialdir=currdir, title='Please select a directory')
    return selected_dir



filepath = "oo"

if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()