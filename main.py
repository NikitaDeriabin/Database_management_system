import tkinter as tk
from Windows.StartWindow import *

if __name__ == "__main__":
    root = tk.Tk()
    app = Main(root)
    app.pack()
    root.title("DB Manager")
    root.geometry("850x650+200+50")
    root.resizable(False, False)
    root.mainloop()