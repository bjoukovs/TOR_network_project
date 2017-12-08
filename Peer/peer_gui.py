from tkinter import Tk, BOTH, RIGHT,LEFT,TOP,BOTTOM,X,N,W,Y,E,Text,END
from tkinter.ttk import Frame, Label, Button, Style, Entry
from tkinter.font import Font


class Peer_gui(Frame):

    def __init__(self, relay):
        super().__init__()

        self.bold_font = Font(family="Helvetica", size=14, weight="bold")

        self.message_frame = Frame(self)
        self.input_frame = Frame(self,relief="groove")
        self.dest_frame = Frame(self)
        self.intext = Entry(self.input_frame)
        self.send_button = Button(self.input_frame, text="SEND",command=self.send_pressed)
        self.lab = Label(self.dest_frame,text="Destination IP:PORT")
        self.dest_input = Entry(self.dest_frame)
        self.output_text = Text(self.message_frame, height=10, state='disabled') #Read-only text box
        self.peer = relay

        self.initUI()

    def print_message(self,text,type=0):
        #Type 0 : Normal print
        #Type 1 : Received message
        #Type 2 : Sent message

        self.output_text.configure(state='normal')

        if type==0:
            self.output_text.insert(END,text+'\n','normal')
        elif type==1:
            self.output_text.insert(END,text+'\n','received')
        elif type ==2:
            self.output_text.insert(END,text+'\n','sent')

        self.output_text.configure(state='disabled')


    def send_pressed(self):
        #Envoie le message actuel

        message = self.intext.get()
        self.intext.delete(0, 'end')
        address = self.dest_input.get()

        self.print_message("you -> "+address,0)
        self.print_message("    "+message,2)

    def receive_message(self,message,ip,port):
        #Reçoit un message depuis le relais

        self.print_message(str(ip)+":"+str(port)+" -> you",0)
        self.print_message("    "+message,1)

    def initUI(self):
        self.master.title("Shallot Messenger")
        self.pack(fill=BOTH, expand=1)

        self.message_frame.pack(side=TOP,fill=BOTH,expand=True)
        self.dest_frame.pack(side=BOTTOM,fill=BOTH)
        self.input_frame.pack(fill=BOTH)

        self.intext.pack(side=LEFT,fill=X,expand=True,padx=5,pady=5)
        self.send_button.pack(side=RIGHT, padx=5, pady=5)    
        self.lab.pack(side=LEFT,fill=X,padx=5,pady=5)        
        self.dest_input.pack(side=RIGHT,padx=5,pady=5,expand=True,fill=X)      

        #Configuring text box and fonts
        self.output_text.pack(fill=BOTH,padx=5,pady=5,expand=True)
        self.output_text.tag_configure('normal', foreground='#000000', font=('Consolas', 10, 'italic'))
        self.output_text.tag_configure('received', foreground='#0000FF', font=('Consolas', 10, 'normal'))
        self.output_text.tag_configure('sent', foreground='#006600', font=('Consolas', 10, 'normal'))

        self.print_message("-- Welcome to Shallot Messenger --",0)
        self.receive_message("Coucou","1.1.1.1",1000)

