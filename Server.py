import sys
from socket import *
from tkinter import *
from threading import *

class Receive(Thread):
    def __init__(self,s,conn,txtbox):
        Thread.__init__(self)
        self.s=s
        self.conn=conn
        self.txtbox=txtbox

    def run(self):
        while 1:
            data = self.conn.recv(1024)
            if not data : break
            txt = data.decode('UTF-8')
            self.txtbox.configure(state = 'normal')
            self.txtbox.tag_config("tag-left",justify="left")
            self.txtbox.insert(END,"\n"+txt,"tag-left")
            self.txtbox.configure(state = 'disabled')

class Initi(Thread):
    
    HOST = 'localhost'
    PORT = 6014
    s = socket(AF_INET,SOCK_STREAM)
    s.bind((HOST,PORT))
    s.listen(1)
    print('server is running ......')
    conn,addr = s.accept()
    print('connected by',addr)

    def __init__(self,root):
        Thread.__init__(self)
        self.root=root
        
        frame = Frame(self.root)
        
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
        self.txtbox.insert(END,'Welcome\n')
        self.txtbox.configure(state='disabled')

    def send(self):
        self.txtbox.configure(state='normal')
        reply = self.entbox.get('1.0',END).strip()
        self.txtbox.tag_config("tag-right",justify="right")
        self.txtbox.insert(END,"\n"+reply,"tag-right")
        self.entbox.delete('1.0',END)
        self.conn.sendall(bytes(reply,'UTF-8'))
        self.txtbox.configure(state='disabled')

    def run(self):
        Receive(self.s,self.conn,self.txtbox).start()

obj = Tk()
obj.title('host')
app = Initi(obj)
app.start()
obj.mainloop()
