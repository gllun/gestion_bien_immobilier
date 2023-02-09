import tkinter as tk
import tkinter.font as tkFont

class App:
    def __init__(self, root):
        #setting title
        root.title("undefined")
        #setting window size
        width=600
        height=500
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        GLabel_33=tk.Label(root)
        ft = tkFont.Font(family='Times',size=38)
        GLabel_33["font"] = ft
        GLabel_33["fg"] = "#333333"
        GLabel_33["justify"] = "center"
        GLabel_33["text"] = "Gestionnaire Immobilier"
        GLabel_33.place(x=50,y=130,width=500,height=10)

        GButton_918=tk.Button(root)
        GButton_918["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        GButton_918["font"] = ft
        GButton_918["fg"] = "#000000"
        GButton_918["justify"] = "center"
        GButton_918["text"] = "Recherche de Biens"
        GButton_918.place(x=200,y=220,width=185,height=54)
        GButton_918["command"] = self.GButton_918_command

        GButton_76=tk.Button(root)
        GButton_76["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        GButton_76["font"] = ft
        GButton_76["fg"] = "#000000"
        GButton_76["justify"] = "center"
        GButton_76["text"] = "Enregistrement de Biens"
        GButton_76.place(x=200,y=320,width=186,height=55)
        GButton_76["command"] = self.GButton_76_command

    def GButton_918_command(self):
        print("command")


    def GButton_76_command(self):
        print("command")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
