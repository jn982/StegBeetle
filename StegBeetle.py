import tkinter as tk  # python 3
from tkinter import font as tkfont  # python 3
import tkinter
from tkinter import filedialog
import os
import base64
from shutil import copyfile
from random import *
from stegano import lsb
from cryptosteganography import CryptoSteganography


class StegBeetle(tk.Tk):

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
        for F in (
        StartPage, Hide, HideSecretMessage_Message, HideSecretMessage_Input_File, HideSecretMessage_Ouput_Dir,
        Hide_Confirmation, Hide_PNG_Key_or_No_Key, Something_Went_Wrong, Create_Success, Hide_PNG__With_Key,
        Hide_MP4_Encrypt_or_No_Encrypt, Hide_WEBM_Encrypt_or_No_Encrypt, Hide_JPG_Encrypt_or_No_Encrypt,
        Hide_BMP_Encrypt_or_No_Encrypt, Hide_GIF_Encrypt_or_No_Encrypt, HideSecretMessage_MP3_File, HideMP3_Input_File,
        HideMP3_Ouput_Dir, HideMP3_Confirmation, Hide_MP3_Key_or_No_Key, Hide_MP3_With_Key, Discover_Input_File,
        Discover_Ouput_Dir, Discover_Confirmation, Discover_PNG_MP3_Detected, Discover_PNG_Key_Detected,
        key_possibly_detected):  # Intiate containers
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


class Something_Went_Wrong(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Something Went Wrong", font=controller.title_font)
        label.config(bg="red")
        label.pack(side="top", fill="x", pady=10)
        home_button = tk.Button(self, text="Home",
                                command=lambda: controller.show_frame("StartPage"))
        home_button.pack(side="top", pady=200)

class Create_Success(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Success!", font=controller.title_font)
        label.config(bg="light green")
        labelInfo = tk.Label(self, text="Your file has been created!", font=controller.normal_font)
        labelInfo.pack()

        label.pack(side="top", fill="x", pady=10)
        home_button = tk.Button(self, text="Home",
                                command=lambda: controller.show_frame("StartPage"))
        home_button.pack(side="top", pady=200)

class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="StegBeetle", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        hide_button = tk.Button(self, text="Hide",
                                command=lambda: controller.show_frame("Hide"))
        discover_button = tk.Button(self, text="Discover",
                                    command=lambda: controller.show_frame("Discover_Input_File"))

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
                                    command=lambda: controller.show_frame("HideSecretMessage_MP3_File"))

        home_button = tk.Button(self, text="Home",
                                command=lambda: controller.show_frame("StartPage"))

        hide_message_button.pack()
        hide_mp3_button.pack()
        home_button.pack(side="bottom", pady=10)


class HideSecretMessage_Message(tk.Frame):

    def updateSecret(self):
        global secret_message
        secret_message = self.secretMessage.get()
        # print("updateSecret: "+secret_message)
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
                                 command=lambda: self.updateSecret())

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
        try:
            write_filepath(filepath)
        except TypeError:
            self.controller.show_frame("Something_Went_Wrong")

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller

        self.labelTitle = tk.Label(self, text="Hide: Finding File", font=controller.title_font)

        self.labelSecret = tk.Label(self, text="Navigate to the image you would like to \n embed your message into",
                                    font=controller.normal_font)

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
        try:
            write_output(output_filepath)
        except TypeError:
            self.controller.show_frame("Something_Went_Wrong")

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller

        self.labelTitle = tk.Label(self, text="Hide: Output File", font=controller.title_font)

        self.labelSecret = tk.Label(self, text="Navigate to the file you would like \n to store your stegged picture",
                                    font=controller.normal_font)

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
        # print(filepath)
        self.labelInputPath.config(text=filepath)
        self.labelFilePath.config(text=output_filepath)
        self.labelSecretMessage.config(text=secret_message)
        # print(secret_message)

    def load_correct_process(self): #This is what will dynamically load the correct method of steganography
        global filepath
        if ".png" in filepath: #Stegano or cryptosteg depending on key or not
            self.controller.show_frame("Hide_PNG_Key_or_No_Key")

        elif ".mp4" in filepath:
            self.controller.show_frame("Hide_MP4_Encrypt_or_No_Encrypt")

        elif ".webm" in filepath:
            self.controller.show_frame("Hide_WEBM_Encrypt_or_No_Encrypt")

        elif (".jpg" in filepath) or (".jpeg" in filepath):
            self.controller.show_frame("Hide_JPG_Encrypt_or_No_Encrypt")

        elif ".bmp" in filepath:
            self.controller.show_frame("Hide_BMP_Encrypt_or_No_Encrypt")

        elif ".gif" in filepath:
            self.controller.show_frame("Hide_GIF_Encrypt_or_No_Encrypt")

        else:
            self.controller.show_frame("Something_Went_Wrong")

    def __init__(self, parent, controller):
        global filepath, secret_message, output_filepath
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

        proceed_button = tk.Button(self, text="Proceed To Steg",
                                   command=self.load_correct_process)

        self.labelSecretMessage.config(bg="light blue")
        self.labelInputPath.config(bg="light yellow")
        self.labelFilePath.config(bg="light green")

        self.labelTitle.pack(side="top", fill="x", pady=5)
        self.labelSecretMessageTitle.pack(side="top", fill="x", pady=5)
        self.labelSecretMessage.pack(side="top", fill="x", pady=5)
        self.labelInputPathTitle.pack(side="top", fill="x", pady=5)
        self.labelInputPath.pack(side="top", fill="x", pady=5)
        self.labelFilePathTitle.pack(side="top", fill="x", pady=5)
        self.labelFilePath.pack(side="top", fill="x", pady=5)
        update_button.pack(side="top", pady=5)
        proceed_button.pack(side="top", pady=5)
        home_button.pack(side="bottom", pady=10)

class Hide_PNG_Key_or_No_Key(tk.Frame):

    def no_key(self):
        global filepath, secret_message, output_filepath
        try:
            stegano(filepath, secret_message, output_filepath)
            self.controller.show_frame("Create_Success")
        except AssertionError:
            self.controller.show_frame("Something_Went_Wrong")

        except FileNotFoundError:
            self.controller.show_frame("Something_Went_Wrong")

    def with_key(self):
            self.controller.show_frame("Hide_PNG__With_Key")


    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="PNG Detected", font=controller.title_font)
        label.config(bg="light blue")
        label.pack(side="top", fill="x", pady=10)

        label = tk.Label(self, text="Would you like to use a key?", font=controller.normal_font)
        label.pack(side="top", fill="x", pady=10)

        yes_key_button = tk.Button(self, text="Yes",
                                command=self.with_key)
        no_key_button = tk.Button(self, text="No",
                                    command=self.no_key)


        home_button = tk.Button(self, text="Home",
                                command=lambda: controller.show_frame("StartPage"))


        yes_key_button.pack()
        no_key_button.pack()
        home_button.pack(side="bottom", pady=10)


class Hide_PNG__With_Key(tk.Frame):

    def updateSecret(self):
        global filepath, secret_message, key, output_filepath
        key = self.secretKey.get()
        try:
            cryptosteganography(filepath, secret_message, key, output_filepath)
            self.controller.show_frame("Create_Success")
        except AssertionError:
            self.controller.show_frame("Something_Went_Wrong")

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        labelTitle = tk.Label(self, text="Hide: Secret Message", font=controller.title_font)

        labelSecret = tk.Label(self, text="What is your key?", font=controller.normal_font)
        self.secretKey = tk.StringVar()
        entryLabel = tk.Label(self, textvariable=self.secretKey)
        mEntry = tk.Entry(self, bd=4, relief='sunken', textvariable=self.secretKey)

        start_button = tk.Button(self, text="Begin Steganography",
                                 command=lambda: self.updateSecret())

        home_button = tk.Button(self, text="Home",
                                command=lambda: controller.show_frame("StartPage"))

        labelTitle.pack(side="top", fill="x", pady=10)
        labelSecret.pack(fill="x", pady=10)
        entryLabel.pack()
        mEntry.pack()
        start_button.pack()
        home_button.pack(side="bottom", pady=10)


class Hide_MP4_Encrypt_or_No_Encrypt(tk.Frame):

    def no_Encrypt(self):
        global filepath, secret_message, output_filepath
        video_append(filepath, secret_message, output_filepath, 'mp4')
        self.controller.show_frame("Create_Success")

    def with_Encrypt(self):
        global filepath, secret_message, output_filepath
        secret_message = encrypt_base64(secret_message)
        video_append(filepath, secret_message, output_filepath, 'mp4')
        self.controller.show_frame("Create_Success")


    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="MP4 Detected", font=controller.title_font)
        label.config(bg="light blue")
        label.pack(side="top", fill="x", pady=10)

        label = tk.Label(self, text="Would you like to encode the secret message?", font=controller.normal_font)
        label.pack(side="top", fill="x", pady=10)

        yes_key_button = tk.Button(self, text="Yes",
                                command=self.with_Encrypt)
        no_key_button = tk.Button(self, text="No",
                                    command=self.no_Encrypt)


        home_button = tk.Button(self, text="Home",
                                command=lambda: controller.show_frame("StartPage"))


        yes_key_button.pack()
        no_key_button.pack()
        home_button.pack(side="bottom", pady=10)


class Hide_WEBM_Encrypt_or_No_Encrypt(tk.Frame):

    def no_Encrypt(self):
        global filepath, secret_message, output_filepath
        video_append(filepath, secret_message, output_filepath, 'webm')
        self.controller.show_frame("Create_Success")

    def with_Encrypt(self):
        global filepath, secret_message, output_filepath
        secret_message = encrypt_base64(secret_message)
        video_append(filepath, secret_message, output_filepath, 'webm')
        self.controller.show_frame("Create_Success")


    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="WEBM Detected", font=controller.title_font)
        label.config(bg="light blue")
        label.pack(side="top", fill="x", pady=10)

        label = tk.Label(self, text="Would you like to encode the secret message?", font=controller.normal_font)
        label.pack(side="top", fill="x", pady=10)

        yes_key_button = tk.Button(self, text="Yes",
                                command=self.with_Encrypt)
        no_key_button = tk.Button(self, text="No",
                                    command=self.no_Encrypt)


        home_button = tk.Button(self, text="Home",
                                command=lambda: controller.show_frame("StartPage"))


        yes_key_button.pack()
        no_key_button.pack()
        home_button.pack(side="bottom", pady=10)



class Hide_JPG_Encrypt_or_No_Encrypt(tk.Frame):

    def no_Encrypt(self):
        global filepath, secret_message, output_filepath
        steg_dir = os.path.dirname(os.path.realpath(__file__))
        steg_dir += '/bin_StegBeetle_jpg.py'
        os.system("python2.7 " + steg_dir)
        self.controller.show_frame("Create_Success")

    def with_Encrypt(self):
        global filepath, secret_message, output_filepath
        secret_message = encrypt_base64(secret_message)
        write_secret(secret_message)
        steg_dir = os.path.dirname(os.path.realpath(__file__))
        steg_dir += '/bin_StegBeetle_jpg.py'
        os.system("python2.7 " + steg_dir)
        self.controller.show_frame("Create_Success")


    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="JPG Detected", font=controller.title_font)
        label.config(bg="light blue")
        label.pack(side="top", fill="x", pady=10)

        label = tk.Label(self, text="Would you like to encode the secret message?", font=controller.normal_font)
        label.pack(side="top", fill="x", pady=10)

        yes_key_button = tk.Button(self, text="Yes",
                                command=self.with_Encrypt)
        no_key_button = tk.Button(self, text="No",
                                    command=self.no_Encrypt)


        home_button = tk.Button(self, text="Home",
                                command=lambda: controller.show_frame("StartPage"))


        yes_key_button.pack()
        no_key_button.pack()
        home_button.pack(side="bottom", pady=10)

class Hide_BMP_Encrypt_or_No_Encrypt(tk.Frame):

    def no_Encrypt(self):
        global filepath, secret_message, output_filepath
        steg_dir = os.path.dirname(os.path.realpath(__file__))
        steg_dir += '/bin_StegBeetle_bmp.py'
        os.system("python2.7 " + steg_dir)
        self.controller.show_frame("Create_Success")

    def with_Encrypt(self):
        global filepath, secret_message, output_filepath
        secret_message = encrypt_base64(secret_message)
        write_secret(secret_message)
        steg_dir = os.path.dirname(os.path.realpath(__file__))
        steg_dir += '/bin_StegBeetle_bmp.py'
        os.system("python2.7 " + steg_dir)
        self.controller.show_frame("Create_Success")


    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="BMP Detected", font=controller.title_font)
        label.config(bg="light blue")
        label.pack(side="top", fill="x", pady=10)

        label = tk.Label(self, text="Would you like to encode the secret message?", font=controller.normal_font)
        label.pack(side="top", fill="x", pady=10)

        yes_key_button = tk.Button(self, text="Yes",
                                command=self.with_Encrypt)
        no_key_button = tk.Button(self, text="No",
                                    command=self.no_Encrypt)


        home_button = tk.Button(self, text="Home",
                                command=lambda: controller.show_frame("StartPage"))


        yes_key_button.pack()
        no_key_button.pack()
        home_button.pack(side="bottom", pady=10)

class Hide_GIF_Encrypt_or_No_Encrypt(tk.Frame):

    def no_Encrypt(self):
        global filepath, secret_message, output_filepath
        steg_dir = os.path.dirname(os.path.realpath(__file__))
        steg_dir += '/bin_StegBeetle_gif.py'
        os.system("python2.7 " + steg_dir)
        self.controller.show_frame("Create_Success")

    def with_Encrypt(self):
        global filepath, secret_message, output_filepath
        secret_message = encrypt_base64(secret_message)
        write_secret(secret_message)
        steg_dir = os.path.dirname(os.path.realpath(__file__))
        steg_dir += '/bin_StegBeetle_gif.py'
        os.system("python2.7 " + steg_dir)
        self.controller.show_frame("Create_Success")

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="GIF Detected", font=controller.title_font)
        label.config(bg="light blue")
        label.pack(side="top", fill="x", pady=10)

        label = tk.Label(self, text="Would you like to encode the secret message?", font=controller.normal_font)
        label.pack(side="top", fill="x", pady=10)

        yes_key_button = tk.Button(self, text="Yes",
                                command=self.with_Encrypt)
        no_key_button = tk.Button(self, text="No",
                                    command=self.no_Encrypt)


        home_button = tk.Button(self, text="Home",
                                command=lambda: controller.show_frame("StartPage"))

        yes_key_button.pack()
        no_key_button.pack()
        home_button.pack(side="bottom", pady=10)

class HideSecretMessage_MP3_File(tk.Frame):

    def find_file(self):
        global mp3
        mp3 = file_grabber()

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller

        self.labelTitle = tk.Label(self, text="Hide MP3: Finding MP3", font=controller.title_font)

        self.labelSecret = tk.Label(self, text="Navigate to the mp3 file you would like to hide",
                                    font=controller.normal_font)

        find_button = tk.Button(self, text="...",
                                command=self.find_file)

        start_button = tk.Button(self, text="Continue",
                                 command=lambda: controller.show_frame("HideMP3_Input_File"))

        home_button = tk.Button(self, text="Home",
                                command=lambda: controller.show_frame("StartPage"))

        self.labelTitle.pack(side="top", fill="x", pady=10)
        self.labelSecret.pack(fill="x", pady=10)
        find_button.pack()
        home_button.pack(side="bottom", pady=10)
        start_button.pack(side="bottom", pady=100)

class HideMP3_Input_File(tk.Frame):

    def find_file(self):
        global filepath
        filepath = file_grabber()

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller

        self.labelTitle = tk.Label(self, text="Hide MP3: Finding File", font=controller.title_font)

        self.labelSecret = tk.Label(self, text="Navigate to the PNG you would like to \n embed your MP3 into",
                                    font=controller.normal_font)

        find_button = tk.Button(self, text="...",
                                command=self.find_file)

        start_button = tk.Button(self, text="Continue",
                                 command=lambda: controller.show_frame("HideMP3_Ouput_Dir"))

        home_button = tk.Button(self, text="Home",
                                command=lambda: controller.show_frame("StartPage"))

        self.labelTitle.pack(side="top", fill="x", pady=10)
        self.labelSecret.pack(fill="x", pady=10)
        find_button.pack()
        home_button.pack(side="bottom", pady=10)
        start_button.pack(side="bottom", pady=100)

class HideMP3_Ouput_Dir(tk.Frame):

    def find_file(self):
        global output_filepath
        output_filepath = dir_grabber()

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller

        self.labelTitle = tk.Label(self, text="Hide: Output File", font=controller.title_font)

        self.labelSecret = tk.Label(self, text="Navigate to the file you would like \n to store your stegged picture",
                                    font=controller.normal_font)

        find_button = tk.Button(self, text="...",
                                command=self.find_file)

        start_button = tk.Button(self, text="Start Steganography",
                                 command=lambda: controller.show_frame("HideMP3_Confirmation"))

        home_button = tk.Button(self, text="Home",
                                command=lambda: controller.show_frame("StartPage"))

        self.labelTitle.pack(side="top", fill="x", pady=10)
        self.labelSecret.pack(fill="x", pady=10)
        find_button.pack()
        home_button.pack(side="bottom", pady=10)
        start_button.pack(side="bottom", pady=100)

class HideMP3_Confirmation(tk.Frame):

    def updateLabel(self):
        global filepath, mp3, output_filepath
        self.labelInputPath.config(text=filepath)
        self.labelFilePath.config(text=output_filepath)
        self.labelSecretMessage.config(text=mp3)
        # print(secret_message)

    def load_correct_process(self): #This is what will dynamically load the correct method of steganography
        global filepath
        if ".png" in filepath:
            #ask key or no
            self.controller.show_frame("Hide_MP3_Key_or_No_Key")
        else:
            self.controller.show_frame("Something_Went_Wrong")

    def __init__(self, parent, controller):
        global filepath, mp3, output_filepath
        tk.Frame.__init__(self, parent)

        self.controller = controller

        self.labelTitle = tk.Label(self, text="Hide: Confirmation", font=controller.title_font)

        self.labelSecretMessageTitle = tk.Label(self, text="Your Secret MP3", font=controller.normal_font)
        self.labelSecretMessage = tk.Label(self, text=mp3, font=controller.normal_font)

        self.labelInputPathTitle = tk.Label(self, text="Input You've Chosen", font=controller.normal_font)
        self.labelInputPath = tk.Label(self, text=filepath, font=controller.normal_font)

        self.labelFilePathTitle = tk.Label(self, text="Output File You've Chosen", font=controller.normal_font)
        self.labelFilePath = tk.Label(self, text=output_filepath, font=controller.normal_font)

        home_button = tk.Button(self, text="Home",
                                command=lambda: controller.show_frame("StartPage"))

        update_button = tk.Button(self, text="Click to load your choices",
                                  command=self.updateLabel)

        proceed_button = tk.Button(self, text="Proceed To Steg",
                                   command=self.load_correct_process)

        self.labelSecretMessage.config(bg="light blue")
        self.labelInputPath.config(bg="light yellow")
        self.labelFilePath.config(bg="light green")

        self.labelTitle.pack(side="top", fill="x", pady=5)
        self.labelSecretMessageTitle.pack(side="top", fill="x", pady=5)
        self.labelSecretMessage.pack(side="top", fill="x", pady=5)
        self.labelInputPathTitle.pack(side="top", fill="x", pady=5)
        self.labelInputPath.pack(side="top", fill="x", pady=5)
        self.labelFilePathTitle.pack(side="top", fill="x", pady=5)
        self.labelFilePath.pack(side="top", fill="x", pady=5)
        update_button.pack(side="top", pady=5)
        proceed_button.pack(side="top", pady=5)
        home_button.pack(side="bottom", pady=10)

class Hide_MP3_Key_or_No_Key(tk.Frame):

    def no_key(self):
        global filepath, mp3, key, output_filepath
        try:
            cryptosteganography_mp3(filepath, mp3, key, output_filepath)
            self.controller.show_frame("Create_Success")
        except AssertionError:
            self.controller.show_frame("Something_Went_Wrong")

        except FileNotFoundError:
            self.controller.show_frame("Something_Went_Wrong")

    def with_key(self):
            self.controller.show_frame("Hide_MP3_With_Key")


    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Hide: MP3", font=controller.title_font)
        label.config(bg="light blue")
        label.pack(side="top", fill="x", pady=10)

        label = tk.Label(self, text="Would you like to use a key?", font=controller.normal_font)
        label.pack(side="top", fill="x", pady=10)

        yes_key_button = tk.Button(self, text="Yes",
                                command=self.with_key)
        no_key_button = tk.Button(self, text="No",
                                    command=self.no_key)


        home_button = tk.Button(self, text="Home",
                                command=lambda: controller.show_frame("StartPage"))


        yes_key_button.pack()
        no_key_button.pack()
        home_button.pack(side="bottom", pady=10)


class Hide_MP3_With_Key(tk.Frame):

    def updateSecret(self):
        global filepath, mp3, key, output_filepath
        key = self.secretKey.get()
        try:
            cryptosteganography_mp3(filepath, mp3, key, output_filepath)
            self.controller.show_frame("Create_Success")
        except AssertionError:
            self.controller.show_frame("Something_Went_Wrong")

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        labelTitle = tk.Label(self, text="Hide: MP3", font=controller.title_font)

        labelSecret = tk.Label(self, text="What is your key?", font=controller.normal_font)
        self.secretKey = tk.StringVar()
        entryLabel = tk.Label(self, textvariable=self.secretKey)
        mEntry = tk.Entry(self, bd=4, relief='sunken', textvariable=self.secretKey)

        start_button = tk.Button(self, text="Begin Steganography",
                                 command=lambda: self.updateSecret())

        home_button = tk.Button(self, text="Home",
                                command=lambda: controller.show_frame("StartPage"))

        labelTitle.pack(side="top", fill="x", pady=10)
        labelSecret.pack(fill="x", pady=10)
        entryLabel.pack()
        mEntry.pack()
        start_button.pack()
        home_button.pack(side="bottom", pady=10)

class Discover_Input_File(tk.Frame):

    def find_file(self):
        global filepath
        filepath = file_grabber()
        try:
            write_filepath(filepath)
        except TypeError:
            self.controller.show_frame("Something_Went_Wrong")

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller

        self.labelTitle = tk.Label(self, text="Discover: Finding File", font=controller.title_font)

        self.labelSecret = tk.Label(self, text="Navigate to the image you would like to look into",
                                    font=controller.normal_font)

        find_button = tk.Button(self, text="...",
                                command=self.find_file)

        start_button = tk.Button(self, text="Continue",
                                 command=lambda: controller.show_frame("Discover_Ouput_Dir"))

        home_button = tk.Button(self, text="Home",
                                command=lambda: controller.show_frame("StartPage"))

        self.labelTitle.pack(side="top", fill="x", pady=10)
        self.labelSecret.pack(fill="x", pady=10)
        find_button.pack()
        home_button.pack(side="bottom", pady=10)
        start_button.pack(side="bottom", pady=100)

class Discover_Ouput_Dir(tk.Frame):

    def find_file(self):
        global output_filepath
        output_filepath = dir_grabber()
        try:
            write_output(output_filepath)
        except TypeError:
            self.controller.show_frame("Something_Went_Wrong")

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller

        self.labelTitle = tk.Label(self, text="Discover: Output File", font=controller.title_font)

        self.labelSecret = tk.Label(self, text="Navigate to the file you would like \n to store your de-stegged information",
                                    font=controller.normal_font)

        find_button = tk.Button(self, text="...",
                                command=self.find_file)

        start_button = tk.Button(self, text="Start Discovery",
                                 command=lambda: controller.show_frame("Discover_Confirmation"))

        home_button = tk.Button(self, text="Home",
                                command=lambda: controller.show_frame("StartPage"))

        self.labelTitle.pack(side="top", fill="x", pady=10)
        self.labelSecret.pack(fill="x", pady=10)
        find_button.pack()
        home_button.pack(side="bottom", pady=10)
        start_button.pack(side="bottom", pady=100)

class Discover_Confirmation(tk.Frame):

    def updateLabel(self):
        global filepath, output_filepath
        # print(filepath)
        self.labelInputPath.config(text=filepath)
        self.labelFilePath.config(text=output_filepath)
        # print(secret_message)

    def load_correct_process(self): #This is what will dynamically load the correct method of desteg
        global filepath
        if ".png" in filepath:
            detected = PNG_autodetect()
            if detected == "maybe_key":
                self.controller.show_frame("key_possibly_detected")

            elif detected == "stegano_no_key":
                stegano_discover()
                self.controller.show_frame("Create_Success")
            elif detected == "no_steg":
                self.controller.show_frame("Something_Went_Wrong")
            else:
                mp3_detect = detect_mp3()
                if mp3_detect == "True":
                    self.controller.show_frame("Discover_PNG_MP3_Detected")
                else:
                    png_desteg()
                    self.controller.show_frame("Create_Success")


        elif ".mp4" in filepath:
            video_discover()
            self.controller.show_frame("Create_Success")

        elif ".webm" in filepath:
            video_discover()
            self.controller.show_frame("Create_Success")

        elif (".jpg" in filepath) or (".jpeg" in filepath):
            steganography_discover()
            self.controller.show_frame("Create_Success")

        elif ".bmp" in filepath:
            steganography_discover()
            self.controller.show_frame("Create_Success")

        elif ".gif" in filepath:
            steganography_discover()
            self.controller.show_frame("Create_Success")

        else:
            self.controller.show_frame("Something_Went_Wrong")

    def __init__(self, parent, controller):
        global filepath, output_filepath
        tk.Frame.__init__(self, parent)

        self.controller = controller

        self.labelTitle = tk.Label(self, text="Discover: Confirmation", font=controller.title_font)

        self.labelInputPathTitle = tk.Label(self, text="Input You've Chosen", font=controller.normal_font)
        self.labelInputPath = tk.Label(self, text=filepath, font=controller.normal_font)

        self.labelFilePathTitle = tk.Label(self, text="Output File You've Chosen", font=controller.normal_font)
        self.labelFilePath = tk.Label(self, text=output_filepath, font=controller.normal_font)

        home_button = tk.Button(self, text="Home",
                                command=lambda: controller.show_frame("StartPage"))

        update_button = tk.Button(self, text="Click to load your choices",
                                  command=self.updateLabel)

        proceed_button = tk.Button(self, text="Proceed To Discover",
                                   command=self.load_correct_process)

        self.labelInputPath.config(bg="light yellow")
        self.labelFilePath.config(bg="light green")

        self.labelTitle.pack(side="top", fill="x", pady=5)
        self.labelInputPathTitle.pack(side="top", fill="x", pady=5)
        self.labelInputPath.pack(side="top", fill="x", pady=5)
        self.labelFilePathTitle.pack(side="top", fill="x", pady=5)
        self.labelFilePath.pack(side="top", fill="x", pady=5)
        update_button.pack(side="top", pady=5)
        proceed_button.pack(side="top", pady=5)
        home_button.pack(side="bottom", pady=10)

class Discover_PNG_Key_Detected(tk.Frame):

    def updateSecret(self):
        global filepath, mp3, key, output_filepath
        key = self.secretKey.get()
        mp3_detect = detect_mp3()
        if mp3_detect == "False":
            try:
                crypto_steganography = CryptoSteganography(key)
                check = crypto_steganography.retrieve(filepath)
                if not check: #wrong key
                    self.controller.show_frame("Something_Went_Wrong")
                else:
                    png_desteg_key()
                    self.controller.show_frame("Create_Success")
            except AssertionError:
                self.controller.show_frame("Something_Went_Wrong")
            except TypeError:
                self.controller.show_frame("Something_Went_Wrong")
        else:
            self.controller.show_frame("Discover_PNG_MP3_Detected")

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        labelTitle = tk.Label(self, text="Discover PNG: KEY DETECTED", font=controller.title_font)

        labelSecret = tk.Label(self, text="What is the key?", font=controller.normal_font)
        self.secretKey = tk.StringVar()
        entryLabel = tk.Label(self, textvariable=self.secretKey)
        mEntry = tk.Entry(self, bd=4, relief='sunken', textvariable=self.secretKey)

        start_button = tk.Button(self, text="Discover",
                                 command=lambda: self.updateSecret())

        home_button = tk.Button(self, text="Home",
                                command=lambda: controller.show_frame("StartPage"))

        labelTitle.pack(side="top", fill="x", pady=10)
        labelSecret.pack(fill="x", pady=10)
        entryLabel.pack()
        mEntry.pack()
        start_button.pack()
        home_button.pack(side="bottom", pady=10)

class Discover_PNG_MP3_Detected(tk.Frame):

    def output_mp3(self):
        global filepath, output_filepath
        crypto_steganography = CryptoSteganography(key)
        decrypted_mp3 = crypto_steganography.retrieve(filepath)
        # read as an mp3
        with open(output_filepath + "/destegged-mp3-output.mp3", 'wb') as write_mp3:
            write_mp3.write(decrypted_mp3)

        self.controller.show_frame("Create_Success")

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Discover: MP3 DETECTED", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        output_mp3_button = tk.Button(self, text="Output as MP3",
                                command=self.output_mp3)


        output_mp3_button.pack()

class key_possibly_detected(tk.Frame):

    def no_key(self):
        stegano_discover()
        self.controller.show_frame("Create_Success")

    def with_key(self):
        self.controller.show_frame("Discover_PNG_Key_Detected")


    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Discover: KEY POSSIBLY DETECTED", font=controller.title_font)
        label.config(bg="light blue")
        label.pack(side="top", fill="x", pady=10)

        label = tk.Label(self, text="There is a possibility that the payload \nis encrypted with a key. \n Would you like to proceed with a key?", font=controller.normal_font)
        label.pack(side="top", fill="x", pady=10)

        yes_key_button = tk.Button(self, text="Yes",
                                command=self.with_key)
        no_key_button = tk.Button(self, text="No",
                                    command=self.no_key)


        home_button = tk.Button(self, text="Home",
                                command=lambda: controller.show_frame("StartPage"))


        yes_key_button.pack()
        no_key_button.pack()
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
            if i == 0:  # 1st line: filepath
                filepath = purify(line)
            elif i == 1:  # 2nd line: secret_message
                secret_message = purify(line)
            elif i == 2:  # 3rd line: output_path
                output_filepath = purify(line)


def write_filepath(new_filepath):
    with open('StegBeetle_config.txt', 'r') as config_file:
        # read a list of lines into data
        data = config_file.readlines()

    # now change the 1st line, note that you have to add a newline
    data[0] = new_filepath + '\n'

    # and write everything back
    with open('StegBeetle_config.txt', 'w') as file:
        file.writelines(data)
        # print(data)


def write_secret(new_secret):
    with open('StegBeetle_config.txt', 'r') as config_file:
        # read a list of lines into data
        data = config_file.readlines()

    # now change the 2nd line, note that you have to add a newline
    data[1] = new_secret + '\n'

    # and write everything back
    with open('StegBeetle_config.txt', 'w') as file:
        file.writelines(data)
        # print(data)


def write_output(new_output):
    with open('StegBeetle_config.txt', 'r') as config_file:
        # read a list of lines into data
        data = config_file.readlines()

    # now change the 3rd line, note that you have to add a newline
    data[2] = new_output + '\n'

    # and write everything back
    with open('StegBeetle_config.txt', 'w') as file:
        file.writelines(data)
        # print(data)

def stegano(given_filepath, given_secret_message, given_output_filepath):
    pure_filepath = purify(given_filepath) #takes away the \n added by the write function
    pure_secret = purify(given_secret_message)
    pure_output_filepath = purify(given_output_filepath) + '/stegged-png-image-'+str(randint(0,100000))+'.png'

    secret = lsb.hide(pure_filepath, pure_secret)
    secret.save(pure_output_filepath)

def cryptosteganography(given_filepath, given_secret_message, given_secret_key, given_output_filepath):
    pure_filepath = purify(given_filepath) #takes away the \n added by the write function
    pure_secret = purify(given_secret_message)
    pure_output_filepath = purify(given_output_filepath) + '/stegged-png-image-'+str(randint(0,100000))+'.png'
    #print(pure_filepath, given_secret_message, given_secret_key, given_output_filepath)
    crypto_steganography = CryptoSteganography(given_secret_key)
    crypto_steganography.hide(pure_filepath, pure_output_filepath, pure_secret)

def video_append(given_filepath, given_secret_message, given_output_filepath, filetype):
    pure_filepath = purify(given_filepath) #takes away the \n added by the write function
    pure_secret = purify(given_secret_message)
    pure_output_filepath = purify(given_output_filepath) + '/stegged-'+filetype+'-image-'+str(randint(0,100000))+'.'+ filetype

    copyfile(pure_filepath, pure_output_filepath)   #make a copy of the video
    with open(pure_output_filepath, "a") as myfile:
        myfile.write("{({({ " + pure_secret + " })})}") #append data to it

def encrypt_base64(data):
    base64_data = str(base64.b64encode(data.encode('ascii')))
    return base64_data

def purify(data):
    if "\n" in data:
        data = data[:-1]

    return data

def cryptosteganography_mp3(given_filepath, given_secret_mp3, given_secret_key, given_output_filepath):
    pure_filepath = purify(given_filepath) #takes away the \n added by the write function
    pure_output_filepath = purify(given_output_filepath) + '/stegged-png-image-'+str(randint(0,100000))+'.png'
    crypto_steganography = CryptoSteganography(given_secret_key)

    with open(given_secret_mp3, "rb") as f: #filepath = jpg, mp3 = mp3 path
        write_data = f.read()

    crypto_steganography.hide(pure_filepath, pure_output_filepath, write_data)

def PNG_autodetect():
    global filepath
    secret = lsb.reveal(filepath)
    try:
        if " " in secret:
            secret = "stegano_no_key"

        else:
            secret = "maybe_key"
            #print("there is a key")

    except TypeError:
        secret = "no_steg"


    return secret

def stegano_discover():
    global filepath
    write_data = lsb.reveal(filepath)
    #print(type(write_data))

    with open(output_filepath+'/StegBeetle_Discovered_Informaton.txt', 'w') as discover_info:
        discover_info.write(write_data)


def png_desteg():
    crypto_steganography = CryptoSteganography("")
    write_data = crypto_steganography.retrieve(filepath)

    with open(output_filepath+'/StegBeetle_Discovered_Informaton.txt', 'w') as discover_info:
        discover_info.write(write_data)

def png_desteg_key():
    crypto_steganography = CryptoSteganography(key)
    write_data = str(crypto_steganography.retrieve(filepath))

    with open(output_filepath+'/StegBeetle_Discovered_Informaton.txt', 'w') as discover_info:
        discover_info.write(write_data)

def detect_mp3():
    crypto_steganography = CryptoSteganography(key)
    write_data = crypto_steganography.retrieve(filepath)
    detected = ""
    if type(write_data) == bytes:
        detected = "True"
        #print("mp3 caugtht")
    else:
        detected = "False"


    return detected

def video_discover():
    write_data = os.popen("strings " + filepath).read()

    with open(output_filepath+'/StegBeetle_Discovered_Informaton.txt', 'w') as discover_info:
        discover_info.write(write_data)

def steganography_discover():
    steg_dir = os.path.dirname(os.path.realpath(__file__))
    steg_dir += '/bin_StegBeetle_discover.py'
    os.system("python2.7 " + steg_dir)


filepath = ""
secret_message = ""
output_filepath = ""
mp3 = ""
key = ""

if __name__ == "__main__":
    config_loader()
    app = StegBeetle()
    app.mainloop()