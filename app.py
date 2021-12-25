import tkinter as tk
from tkinter import ttk, Button, RIGHT, END, Listbox, messagebox
import tkinter.filedialog as fd
import PyPDF2


def upload_action(event=None):
    filenames = fd.askopenfilenames(filetypes=[("Text files", "*.pdf")], title='Choose pdfs to merge')
    for file in filenames:
        my_listbox.insert(END, file)


def merge_files():
    merger = PyPDF2.PdfFileMerger()
    lista = my_listbox.get(0, END)
    print(lista)
    for _pdf in lista:
        merger.append(PyPDF2.PdfFileReader(_pdf, 'rb'))
    # TODO Add name selection of file output
    merger.write("result.pdf")
    messagebox.showinfo("RESULT", "pdfs merged successfully")


def delete():
    selection = my_listbox.curselection()
    for index in selection[::-1]:
        my_listbox.delete(index)


def delete_all():
    my_listbox.delete(0, END)


root = tk.Tk()
root.title("PDF tool")
root.geometry("400x300")
tabControl = ttk.Notebook(root)

tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)
tabControl.add(tab1, text='merge')
tabControl.add(tab2, text='split')
tabControl.pack(expand=1, fill="both")

my_listbox = Listbox(tab1, selectmode='multiple')
my_listbox.pack(expand=1, fill="both")
my_listbox.insert(END, 'testing')
b_add = Button(tab1, text="select files", width=10, height=2, command=upload_action)
b_merge = Button(tab1, text="merge files", width=10, height=2, command=merge_files)
b_delete = Button(tab1, text="delete", width=10, height=2, command=delete)
b_delete_all = Button(tab1, text="delete_all", width=10, height=2, command=delete_all)

b_delete.pack(side=RIGHT)
b_delete_all.pack(side=RIGHT)
b_add.pack(side=RIGHT)
b_merge.pack(side=RIGHT)

# button = tk.Button(tab1, text='select PDF files', command=upload_action)
# button.pack(side=RIGHT)
root.mainloop()
