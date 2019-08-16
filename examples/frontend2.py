from tkinter import *
from tkinter import Label

import examples.microphone_speech_to_text2 as mi


class Window(Frame):

    def __init__(self, master=None):
        """Define settings upon initialization. Here you can specify
        parameters that you want to send through the Frame class.
        :param master: None
        """

        Frame.__init__(self, master)

        # reference to the master widget, which is the tk window
        self.master = master
        # init the mic to text instance
        self.mic = mi.MicrophoneToText()
        # with that, we want to then run init_window, which doesn't yet exist
        self.init_window()
        self.configure(background='white')

    def init_window(self):
        """Creation of init_window
        :return: None
        """

        # changing the title of our master widget
        self.master.title("Sprachassistent")

        # allowing the widget to take the full space of the root window
        self.pack(fill=BOTH, expand=1)

        # creating the buttons instances
        self.quitButton = Button(self, bg="red", text="Exit", command=self.client_exit, height=6, width=54)
        self.commandButton = Button(self, bg="green", text="Start listening", command=self.mic.threader, height=6,
                                    width=54)
        self.resultButton = Button(self, bg="orange", text="Show me what you got", command=self.show_results, height=6,
                                   width=54)

        self.streetlabel = Label(self, text="Strasse:", anchor=W, justify=LEFT, height=2, background='white')
        self.streetlabel.grid(row=2, column=0, sticky=N+S+E+W)
        self.locationlabel = Label(self, text="Ort:", anchor=W, justify=LEFT, height=2, background='white')
        self.locationlabel.grid(row=3, column=0, sticky=N+S+E+W)
        self.capitallabel = Label(self, text="Eigenkapital:", anchor=W, justify=LEFT, height=2, background='white')
        self.capitallabel.grid(row=4, column=0, sticky=N+S+E+W)
        self.incomelabel = Label(self, text="Einkommen:", anchor=W, justify=LEFT, height=2, background='white')
        self.incomelabel.grid(row=5, column=0, sticky=N+S+E+W)
        self.pricelabel = Label(self, text="Kaufpreis:", anchor=W, justify=LEFT, height=2, background='white')
        self.pricelabel.grid(row=6, column=0, sticky=N+S+E+W)

        self.x1000button1 = Button(self, text="x 1000", command=lambda x='capital': self.xtousand(x))
        self.x1000button2 = Button(self, text="x 1000", command=lambda x='income': self.xtousand(x))
        self.x1000button3 = Button(self, text="x 1000", command=lambda x='price': self.xtousand(x))
        self.x1000button1.grid(row=4, column=6, sticky=N+S+E+W)
        self.x1000button2.grid(row=5, column=6, sticky=N+S+E+W)
        self.x1000button3.grid(row=6, column=6, sticky=N+S+E+W)

        # placing the button on my window

        self.quitButton.grid(row=7, column=0, columnspan=2, sticky=N+S+E+W)
        self.commandButton.grid(row=7, column=2, columnspan=2, sticky=N+S+E+W)
        self.resultButton.grid(row=7, column=4, columnspan=2, sticky=N+S+E+W)

    def client_exit(self):
        """exits the frontend and shuts down the microphone to text service
        :return: None
        """
        resultlist = {'street': self.streetlabel["text"][9:],
                      'location': self.locationlabel["text"][5:],
                      'capital': self.capitallabel["text"][13:],
                      'income': self.incomelabel["text"][11:],
                      'price': self.pricelabel["text"][11:]}
        print("final: ")
        print(resultlist)
        self.mic.switchoff()
        exit()

    def show_results(self):
        """shows the results of the microphone to text service in the ResultLabel
        :return: None
        """

        self.dic = self.mic.print_results()

        self.street = self.dic['street']
        self.location = self.dic['location']
        self.capital = self.dic['capital']
        self.income = self.dic['income']
        self.price = self.dic['price']

        for i in range(0, len(self.street)):
            Button(self, text=self.street[i], command=lambda x=self.street[i]: self.writes(x), height=2).grid(row=2, column=1+i, sticky=N+S+E+W)

        for o in range(0, len(self.location)):
            Button(self, text=self.location[o], command=lambda x=self.location[o]: self.writel(x), height=2).grid(row=3, column=1+o, sticky=N+S+E+W)

        for a in range(0, len(self.capital)):
            Button(self, text=self.capital[a], command=lambda x=self.capital[a]: self.writec(x), height=2).grid(row=4, column=1+a, sticky=N+S+E+W)

        for b in range(0, len(self.income)):
            Button(self, text=self.income[b], command=lambda x=self.income[b]: self.writei(x), height=2).grid(row=5, column=1+b, sticky=N+S+E+W)

        for c in range(0, len(self.price)):
            Button(self, text=self.price[c], command=lambda x=self.price[c]: self.writep(x), height=2).grid(row=6, column=1+c, sticky=N+S+E+W)





    def writes(self, text):
        if text not in self.streetlabel["text"]:
            self.streetlabel["text"] = "Strasse: " + text

    def writel(self, text):
        if text not in self.locationlabel["text"]:
            self.locationlabel["text"] = "Ort: " + text

    def writec(self, text):
        if str(text) not in self.capitallabel["text"]:
            self.capitallabel["text"] = "Eigenmittel: " + str(text)

    def writei(self, text):
        if str(text) not in self.incomelabel["text"]:
            self.incomelabel["text"] = "Einkommen: " + str(text)

    def writep(self, text):
        if str(text) not in self.pricelabel.cget("text"):
            self.pricelabel["text"] = "Kaufpreis: " + str(text)

    def xtousand(self, text):
        if text == 'income':
            self.incomelabel["text"] = self.incomelabel["text"] + '000'
        elif text == 'price':
            self.pricelabel["text"] = self.pricelabel["text"] + '000'
        elif text == 'capital':
            self.capitallabel["text"] = self.capitallabel["text"] + '000'
        else:
            pass

    def main(self):
        """starts the main window and calls the mainloop method on it so it keeps displayed
        :return: None
        """

        root = Tk()
        root.configure(background='white')

        # creation of an instance
        app = Window(root)

        # mainloop
        root.mainloop()


if __name__ == '__main__':
    Window.main(Window)
