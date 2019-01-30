import sys
from socket import *
from tkinter import *
from threading import *

class Receive(Thread):
    def __init__(self,s,txtbox):
        Thread.__init__(self)
        self.s=s
        self.txtbox=txtbox

    def run(self):
        while 1:
            reply = self.s.recv(1024)
            if not reply : break
            txt = reply.decode('UTF-8')
            self.txtbox.configure(state='normal')
            self.txtbox.tag_config("tag-left",justify="left")
            self.txtbox.insert(END,"\n"+txt,"tag-left")
            self.txtbox.configure(state='disabled')

class Initi(Thread):
    
    HOST = 'localhost'
    PORT = 6014
    s = socket(AF_INET,SOCK_STREAM)
    s.connect((HOST,PORT))
   

    def __init__(self,root):
        Thread.__init__(self)
        self.root=root
        
        frame= Frame(root)
        frame.pack()

        self.mbut = Button(frame,text='quit',command=frame.quit,bg='skyblue',fg='white',pady=15)
        self.mbut.grid(row=1,column=2)
        self.mbut.config(width=15)

        self.mbut1 = Button(frame,text='send',command=self.send,bg='skyblue',fg='white',pady=15)
        self.mbut1.grid(row=1,column=1)
        self.mbut1.config(width=15)

        self.entbox = Text(frame,width=40,height=3)
        self.entbox.grid(row=1,column=0)


        self.txtbox = Text(frame,height=20,width=69,wrap=WORD)
        self.txtbox.grid(row=0,columnspan=3)
        self.txtbox.insert(END,'welcome\n')
        self.txtbox.configure(state='disabled')

    def send(self):
        self.txtbox.configure(state='normal')
        text = self.entbox.get('1.0',END).strip()
        self.txtbox.tag_config("tag-right",justify="right")
        self.txtbox.insert(END,"\n"+text,"tag-right")
        self.entbox.delete('1.0',END)
        self.s.send(bytes(text,'UTF-8'))
        self.txtbox.configure(state='disabled')

    def run(self):
        Receive(self.s,self.txtbox).start()

obj = Tk()
obj.title('client')
app = Initi(obj)
app.start()
obj.mainloop()
