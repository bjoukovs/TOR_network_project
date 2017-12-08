from tkinter import Tk, BOTH, RIGHT,LEFT,TOP,BOTTOM,X,N,W,Y,E,Text
from tkinter.ttk import Frame, Label, Button, Style, Entry


class Peer_gui(Frame):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.master.title("Shallot Messenger")
        self.pack(fill=BOTH, expand=1)

        message_frame = Frame(self)
        input_frame = Frame(self,relief="groove")
        dest_frame = Frame(self)

        message_frame.pack(side=TOP,fill=BOTH,expand=True)
        dest_frame.pack(side=BOTTOM,fill=BOTH)
        input_frame.pack(fill=BOTH)
        #message_frame.pack_propagate(0)

        #self.style = Style()
        #self.style.theme_use("default")

        intext = Entry(input_frame)
        intext.pack(side=LEFT,fill=X,expand=True,padx=5,pady=5)

        send_button = Button(input_frame, text="SEND")
        send_button.pack(side=RIGHT, padx=5, pady=5)

        lab = Label(dest_frame,text="Destination IP:PORT")
        lab.pack(side=LEFT,fill=X,padx=5,pady=5)

        dest_input = Entry(dest_frame)
        dest_input.pack(side=RIGHT,padx=5,pady=5,expand=True,fill=X)

        output_text= Label(message_frame, text="Welcome to Shallot Messenger",relief="solid",justify=LEFT,anchor=N+W,background="white")
        output_text.pack(fill=BOTH,padx=5,pady=5,expand=True)


