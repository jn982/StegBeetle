import tkinter as tk                # python 3
from tkinter import font  as tkfont # python 3

class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold")
        self.normal_font = tkfont.Font(family='Helvetica', size=15, weight="bold")

        self.title("StegBeetle")
        self.geometry("500x250")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, Hide, Discover):
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
                           command=lambda: controller.show_frame("StartPage"))

        hide_mp3_button = tk.Button(self, text="MP3",
                           command=lambda: controller.show_frame("StartPage"))

        back_button = tk.Button(self, text="Back",
                           command=lambda: controller.show_frame("StartPage"))

        hide_message_button.pack()
        hide_mp3_button.pack()
        back_button.pack()




class Discover(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Discover", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        back_button = tk.Button(self, text="Back",
                           command=lambda: controller.show_frame("StartPage"))
        back_button.pack()


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()