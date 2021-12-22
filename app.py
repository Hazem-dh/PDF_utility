import tkinter as tk
from tkinter import ttk
import tkinter.filedialog as fd


def upload_action(event=None):
    filenames = fd.askopenfilenames(filetypes=[("Text files", "*.pdf")], title='Choose pdfs to merge')
    print('Selected:', filenames)


root = tk.Tk()
root.title("PDF tool")
root.geometry("400x300")
tabControl = ttk.Notebook(root)

tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)

tabControl.add(tab1, text='merge')
tabControl.add(tab2, text='split')
tabControl.pack(expand=1, fill="both")

button = tk.Button(tab1, text='select PDF files', command=upload_action)
button.pack()
root.mainloop()